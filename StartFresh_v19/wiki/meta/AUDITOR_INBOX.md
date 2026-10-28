# 📬 `AUDITOR_INBOX.md` — Asynchronous Steering & Coaching Mailbox (`MONITOR` / `AUDITOR` $\to$ `PROOFER`)

> **How this file works (`Law K10` Safe Multi-Thread Communication):**
> - **`MONITOR` (Thread 2)** and **`AUDITOR` (Thread 3)** write strategic feedback, `Law M2` representation pivots, `Law M1` surrogate suggestions, and epistemic audit notes here so they never collide with code files being edited by **`PROOFER` (Thread 1)**.
> - **`PROOFER` (Thread 1)** reads this file at the start of every cycle, executes any high-priority directives or fixes, and acknowledges them in `wiki/meta/hot.md`.

---

## 🟢 Active Directives for `PROOFER` (Worker Thread)

- **[Status: Clean Boot]** No pending corrective directives yet. Remember on Cycle 1:
  1. Keep `wiki/meta/hot.md` updated and ensure `PROJECT_CHARTER.md` defines the exact target and verification oracle (`< 5s`).
  2. Before running long tree/combinatorial searches, log an atomic micro-bet via `python3 scripts/micro_bet.py predict <target> <H_key> <p> "<claim>" --by proofer_main` ($p \le 0.65$) and wire your hypothesis into `graphs/main.jsonl` via `python3 scripts/rgraph.py`.
