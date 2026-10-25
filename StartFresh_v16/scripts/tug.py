#!/usr/bin/env python3
"""Tug-of-war deliberation for BRAIN's DECIDE phase (CONSTITUTION v13 §13): an IMPLEMENT / DON'T IMPLEMENT gate.

One hypothesis H is on the table. Advocate IMPLEMENT argues that H should be carried out now. Advocate SEARCH
argues "don't implement H; keep searching" and must put a concrete, better hypothesis H' on the table (a pure
"no" without a better H' is not allowed). If SEARCH wins, H' goes to the next gate (`chain`): H -> H' -> H'' ...
until an IMPLEMENT wins or the chain hits its limit (deadlock: BRAIN index or the human decides).
Both advocates are fresh `agy -p` calls with no tools (`--agent tug-advocate`) and the system prompt from
.agents/agents/tug-advocate.md. Every bout has two halves of three rounds:
    half 1: B critiques A -> A responds -> B critiques the response
    half 2: A critiques B -> B responds -> A critiques the response
then both declare a verdict (LOST / WON / HOLD) separately. A decision exists only when one says LOST and the
other WON. Otherwise the next bout starts. Each advocate then sees the full PUBLIC transcript plus ONLY ITS OWN
<private> notes, never the counterpart's, and must analyse the earlier rounds. After MAX bouts with no decision the
result is DEADLOCK and BRAIN's index (or the human) decides.

Referee (mechanical, no LLM): enforces the format and 1200-char public limit, and marks REPEAT when a public text is
too similar to one of the same side's earlier texts. Everything is stored in <PROOFER_HOME>/tug/<name>/.

Usage:
  tug.py new NAME --question "..." --hypothesis "H" --evidence FILE [FILE...]
  tug.py run NAME [--max-bouts 3] [--model MODEL]                 one gate
  tug.py chain NAME [--max-links 3] [--max-bouts 3] [--model M]   gate, and on SEARCH wins gate H' ... until IMPLEMENT
  tug.py show NAME
"""
import json
import os
import random
import re
import subprocess
import sys
import time
from pathlib import Path

HOME = Path(os.environ.get("PROOFER_HOME", Path(__file__).resolve().parent.parent))
ROOT = HOME / "tug"
AGENT = Path(os.environ.get("TUG_AGENT", Path.home() / "Desktop/PROOFER/.agents/agents/tug-advocate.md"))
AGY = os.environ.get("AGY_BIN", str(Path.home() / ".local/bin/agy"))
PUBLIC_MAX = 1200
EVIDENCE_MAX = 24000


def now():
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def system_prompt():
    body = AGENT.read_text(encoding="utf-8")
    return re.sub(r"^---.*?---\s*", "", body, flags=re.S)


def toks(s):
    return {w for w in re.findall(r"[a-z0-9]+", s.lower()) if len(w) > 2}


def sim(a, b):
    ta, tb = toks(a), toks(b)
    return len(ta & tb) / len(ta | tb) if ta and tb else 0.0


def call(prompt, model):
    """One advocate turn via Antigravity CLI (`agy -p --agent tug-advocate`). Usage limits stop the gate
    (resume later); a safety-filter false positive or another API error is retried once, then retried on
    FALLBACK_MODEL (the switch is recorded in the turn)."""
    tries = [model, model, os.environ.get("TUG_FALLBACK_MODEL", "gemini-3.8-flash-high")]
    err = ""
    ROOT.mkdir(parents=True, exist_ok=True)
    for m in tries:
        # --agent tug-advocate keeps Antigravity's default context and appends the text-only advocate definition
        # (tools: []), avoiding X7 safety-filter refusals on cipher-topic gates while saving tool-schema tokens.
        cmd = [AGY, "--agent", "tug-advocate", "--disable-slash-commands", "-p", prompt,
               "--print-timeout", "0s", "--output-format", "json"] + (["--model", m] if m else [])
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=900, cwd=str(HOME.parent))
        try:
            # Find the trailing JSON object line in stdout in case CLI warnings precede it
            lines = [ln.strip() for ln in r.stdout.splitlines() if ln.strip().startswith("{")]
            out = json.loads(lines[-1] if lines else r.stdout)
            text = out.get("response") if "response" in out else out.get("result", "")
            is_err = out.get("is_error") or (out.get("status") not in (None, "SUCCESS"))
            if is_err or not text:
                raise ValueError(text or r.stderr[:300] or r.stdout[:300])
            return text, m
        except (ValueError, json.JSONDecodeError) as e:
            err = (str(e) + " " + r.stdout[-300:] + " " + r.stderr[-300:]).strip()
            if re.search(r"usage limit|session limit|rate limit|quota|resource_exhausted|429|resets \d", err, re.I):
                sys.exit(f"TUG_LIMIT: {err[:200]}")
    if re.search(r"safeguards|usage policy|aup|safety", err, re.I):
        return None, "API_REFUSED"            # the caller records a HOLD; the gate continues or deadlocks
    sys.exit(f"TUG_CALL_FAILED: {err[:300]}")


def parse(text):
    priv = re.search(r"<private>(.*?)</private>", text, re.S)
    pub = re.search(r"<public>(.*?)</public>", text, re.S)
    ver = re.search(r"<verdict>(.*?)</verdict>", text, re.S)
    fc = re.search(r"<forecast>(.*?)</forecast>", text, re.S)
    return (priv.group(1).strip() if priv else "",
            pub.group(1).strip() if pub else "",
            ver.group(1).strip() if ver else "",
            fc.group(1).strip() if fc else "")


class Tug:
    def __init__(self, name):
        self.d = ROOT / name
        self.meta = json.loads((self.d / "meta.json").read_text())
        self.log = [json.loads(l) for l in (self.d / "turns.jsonl").read_text().splitlines() if l.strip()] \
            if (self.d / "turns.jsonl").exists() else []

    def append(self, rec):
        rec["ts"] = now()
        self.log.append(rec)
        with open(self.d / "turns.jsonl", "a", encoding="utf-8") as f:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
        self.render()

    def public_transcript(self):
        out = []
        for r in self.log:
            if r["kind"] == "verdict":
                out.append(f"[bout {r['bout']}] {r['side']} VERDICT: {r['verdict'].get('verdict')} — {r['verdict'].get('decisive', '')}")
            else:
                flag = " [REFEREE: REPEAT]" if r.get("repeat") else ""
                flag += " [REFEREE: OVER LENGTH, TRUNCATED]" if r.get("truncated") else ""
                out.append(f"[bout {r['bout']} · {r['kind']}] {r['side']}{flag}:\n{r['public']}")
        return "\n\n".join(out) or "(no turns yet)"

    def own_private(self, side):
        return "\n\n".join(f"[bout {r['bout']} · {r['kind']}] {r['private']}" for r in self.log
                           if r["side"] == side and r.get("private")) or "(none yet)"

    def brief(self, side):
        m = self.meta
        mine, theirs = (m["a"], m["b"]) if side == "A" else (m["b"], m["a"])
        return (f"DECISION QUESTION: {m['question']}\n\nYOU ARE ADVOCATE {side}. YOUR OPTION: {mine}\n"
                f"COUNTERPART'S OPTION: {theirs}\n\nEVIDENCE PACK:\n{m['evidence']}\n")

    def turn(self, side, bout, kind, instruction, model):
        for r in self.log:                       # resume: this exact turn already happened
            if (r["bout"], r["side"], r["kind"]) == (bout, side, kind):
                return r
        prompt = (self.brief(side) + "\n=== PUBLIC TRANSCRIPT SO FAR ===\n" + self.public_transcript()
                  + "\n\n=== YOUR OWN PRIVATE NOTES FROM EARLIER TURNS (the counterpart never saw these) ===\n"
                  + self.own_private(side) + f"\n\n=== YOUR TASK NOW (bout {bout}, {kind}) ===\n" + instruction)
        text, used = call(prompt, model)
        if text is None:                          # refused on every model: never invent content
            text = ("<private>(no output: API_REFUSED on all models)</private>\n<public>(REFEREE: this turn was refused by the "
                    "API safety filter on every model; no argument was made)</public>\n<verdict>{\"verdict\": \"HOLD\", "
                    "\"decisive\": \"REFEREE: API_REFUSED\", \"confidence\": 0}</verdict>")
        priv, pub, ver, fc = parse(text)
        rec = {"bout": bout, "side": side, "kind": kind, "private": priv, "model": used or "default"}
        if fc:
            try:
                rec["forecast"] = json.loads(fc)
            except json.JSONDecodeError:
                rec["forecast"] = {"raw": fc[:300]}
        if kind == "verdict":
            try:
                rec["verdict"] = json.loads(ver)
            except json.JSONDecodeError:
                rec["verdict"] = {"verdict": "HOLD", "decisive": "REFEREE: unparseable verdict", "raw": ver[:300]}
            if rec["verdict"].get("verdict") not in ("LOST", "WON", "HOLD"):
                rec["verdict"]["verdict"] = "HOLD"
        else:
            rec["truncated"] = len(pub) > PUBLIC_MAX
            rec["public"] = pub[:PUBLIC_MAX] or "(REFEREE: no <public> block)"
            prev = [r["public"] for r in self.log if r["side"] == side and r.get("public")]
            rec["repeat"] = any(sim(rec["public"], p) > 0.6 for p in prev)
        self.append(rec)
        return rec

    def render(self):
        m = self.meta
        lines = [f"# Tug: {m['name']}", "", f"**Question:** {m['question']}", "", f"**Hypothesis H:** {m.get('hypothesis', '')}",
                 "", f"- **A ({m.get('role_a', '')})**", f"- **B ({m.get('role_b', '')})**",
                 f"- status: **{m.get('status', 'open')}** {m.get('winner_role', '')} {m.get('better_hypothesis', '')}",
                 f"- parent gate: {m.get('parent', '') or '—'}", "", "## Public transcript", "",
                 self.public_transcript(), ""]
        (self.d / "transcript.md").write_text("\n".join(lines), encoding="utf-8")

    def save_meta(self):
        (self.d / "meta.json").write_text(json.dumps(self.meta, indent=1, ensure_ascii=False))


def cmd_new(argv):
    name = argv[0]
    opts, files, key = {}, [], None
    for x in argv[1:]:
        if x.startswith("--"):
            key = x
        elif key == "--evidence":
            files.append(x)
        else:
            opts[key] = x
    d = ROOT / name
    d.mkdir(parents=True, exist_ok=False)
    ev, total = [], 0
    for i, f in enumerate(files, 1):
        t = Path(f).read_text(encoding="utf-8", errors="replace")
        t = t[: max(0, (EVIDENCE_MAX - total) // max(1, len(files) - i + 1))]
        total += len(t)
        ev.append(f"[E{i}] {f}\n{t}")
    h = opts["--hypothesis"]
    sides = [("IMPLEMENT", f"IMPLEMENT the hypothesis now: {h}"),
             ("SEARCH", f"DO NOT IMPLEMENT it; keep searching. You must put on the table a concrete, better "
                        f"hypothesis H' (what to do instead, why it beats H, its forecast). Hypothesis under test: {h}")]
    if random.random() < 0.5:            # which letter holds which role must not leak a preference
        sides.reverse()
    meta = {"name": name, "question": opts["--question"], "hypothesis": h,
            "a": sides[0][1], "b": sides[1][1], "role_a": sides[0][0], "role_b": sides[1][0],
            "evidence": "\n\n".join(ev), "evidence_files": files, "created": now(), "status": "open",
            "parent": opts.get("--parent", "")}
    (d / "meta.json").write_text(json.dumps(meta, indent=1, ensure_ascii=False))
    print(f"created {d} (A = {sides[0][0]} | B = {sides[1][0]})")


H = {
    "opening": "Make your opening case for YOUR option (forecast with probability and date, citations).",
    "critique": "Critique the COUNTERPART's case: challenge its strongest point; flag uncited claims as UNSUPPORTED.",
    "response": "Respond to the critique of YOUR case: concede what is right, rebut what is not, with citations.",
    "critique2": "Critique the counterpart's RESPONSE: what did it leave unanswered? Is anything in it unsupported?",
    "verdict": ("Give your verdict on the whole bout. First analyse the rounds so far in <private>: which arguments "
                "moved you, which did not, and why. Then output the <verdict> line."),
}
H_REPLAY = ("This is a REPLAY bout because the last bout ended without a LOST/WON pair. Before arguing, analyse in "
            "<private> the previous rounds: what was left unanswered, where you were wrong, what the counterpart "
            "actually established. Do not repeat answered arguments. ")


def cmd_run(argv):
    name, maxb, model = argv[0], 3, os.environ.get("TUG_MODEL", "")
    if "--max-bouts" in argv:
        maxb = int(argv[argv.index("--max-bouts") + 1])
    if "--model" in argv:
        model = argv[argv.index("--model") + 1]
    t = Tug(name)
    done_bouts = max([r["bout"] for r in t.log if r["kind"] == "verdict"], default=0)   # completed bouts only
    if t.meta.get("status") in ("decided", "deadlock"):
        return t.meta.get("winner_role", "DEADLOCK")
    for bout in range(max(1, done_bouts + (1 if sum(1 for r in t.log if r["kind"] == "verdict" and r["bout"] == done_bouts) == 2 else 0)), maxb + 1):
        pre = H_REPLAY if bout > 1 else ""
        if bout == 1:
            for s in ("A", "B"):
                t.turn(s, bout, "opening", H["opening"], model)
        first = ("B", "A") if bout % 2 else ("A", "B")      # alternate who attacks first
        for att, dfd in (first, first[::-1]):
            t.turn(att, bout, "critique", pre + H["critique"], model)
            t.turn(dfd, bout, "response", pre + H["response"], model)
            t.turn(att, bout, "critique2", pre + H["critique2"], model)
        va = t.turn("A", bout, "verdict", H["verdict"], model)["verdict"]["verdict"]
        vb = t.turn("B", bout, "verdict", H["verdict"], model)["verdict"]["verdict"]
        if {va, vb} == {"LOST", "WON"}:
            winner = "A" if va == "WON" else "B"
            role = t.meta["role_" + winner.lower()]
            t.meta.update(status="decided", winner=winner, winner_role=role, bouts=bout, decided=now())
            if role == "SEARCH":
                last = [r for r in t.log if r["side"] == winner and r["kind"] == "verdict"][-1]["verdict"]
                t.meta["better_hypothesis"] = last.get("better_hypothesis", "")
            fcs = [r["forecast"] for r in t.log if r["side"] == winner and r.get("forecast")]
            if fcs and "p" in fcs[-1]:      # §13.6: the winner's forecast becomes a ledger bet
                f = fcs[-1]
                r = subprocess.run([sys.executable, str(Path(__file__).with_name("postdict.py")), "predict",
                                    f"tug/{t.meta['name']}", str(f["p"]), f"{role} winner: {f.get('claim', '')} (by {f.get('by', '?')})"],
                                   capture_output=True, text=True, env={**os.environ, "PROOFER_HOME": str(HOME)})
                t.meta["bet"] = r.stdout.strip()
            t.save_meta(); t.render()
            print(f"TUG_DECIDED: {role}" + (f" -> H' = {t.meta.get('better_hypothesis', '')}" if role == "SEARCH" else "")
                  + f" (bout {bout})")
            return role
        print(f"bout {bout}: A={va} B={vb} -> replay" if bout < maxb else f"bout {bout}: A={va} B={vb}")
    t.meta.update(status="deadlock", bouts=maxb, decided=now())
    t.save_meta(); t.render()
    print("TUG_DEADLOCK: fall back to BRAIN index or the human")
    return "DEADLOCK"


def cmd_chain(argv):
    name, links = argv[0], 3
    if "--max-links" in argv:
        links = int(argv[argv.index("--max-links") + 1])
    rest = [x for i, x in enumerate(argv[1:]) if not (x == "--max-links" or (i > 0 and argv[i] == "--max-links"))]
    cur = name
    for link in range(1, links + 1):
        role = cmd_run([cur] + rest)
        t = Tug(cur)
        if role != "SEARCH":
            print(f"TUG_CHAIN_END: {role} at link {link} ({cur}); hypothesis: {t.meta['hypothesis']}")
            return
        nxt = f"{name}-h{link + 1}"
        h2 = t.meta.get("better_hypothesis") or "(SEARCH won without stating H'; escalate to the human)"
        if not t.meta.get("better_hypothesis"):
            print("TUG_CHAIN_END: SEARCH won without a concrete H' -> human"); return
        cmd_new([nxt, "--question", t.meta["question"], "--hypothesis", h2, "--parent", cur,
                 "--evidence", *t.meta["evidence_files"]])
        cur = nxt
    print(f"TUG_CHAIN_END: link limit {links} reached; last hypothesis {Tug(cur).meta['hypothesis']} -> BRAIN index or human")


def cmd_show(argv):
    t = Tug(argv[0])
    print((t.d / "transcript.md").read_text() if (t.d / "transcript.md").exists() else json.dumps(t.meta, indent=1))


if __name__ == "__main__":
    c, a = (sys.argv[1] if len(sys.argv) > 1 else ""), sys.argv[2:]
    {"new": cmd_new, "run": cmd_run, "chain": cmd_chain, "show": cmd_show}.get(c, lambda _: sys.exit(__doc__))(a)
