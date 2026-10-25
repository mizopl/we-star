#!/usr/bin/env python3
"""
build_canvas.py — Wiki OS Canvas Builder (generic bootstrap template)
Generates a clean, semantically organized Obsidian Canvas from wiki/entities/*.md

Usage:
    python3 scripts/build_canvas.py [--output wiki/reports/KB_Mindmap.canvas]

Layout: radial cluster map centered on your primary entity
Edges: derived from actual [[wikilinks]] between entities

NOTE (fresh instance): the CLUSTERS list below is a minimal placeholder
example with 2 dummy entities. Any real entity NOT listed here is still
included automatically — it gets appended as a row at the bottom of the
canvas (see "unplaced" logic). Edit CLUSTERS once you have a handful of
real entities and want a hand-tuned layout instead of the auto-append grid.
"""

import json, re, uuid, argparse
from pathlib import Path

KB = Path(__file__).parent.parent
ENTITIES_DIR = KB / "wiki" / "entities"
DEFAULT_OUTPUT = KB / "wiki" / "reports" / "KB_Mindmap.canvas"

# ── Cluster definitions ────────────────────────────────────────────────────────
# Each cluster: { label, color, cx, cy, entities: [(name, x_offset, y_offset)] }
# Positions are absolute canvas coordinates.
# Color codes: 1=red 2=orange 3=yellow 4=green 5=purple 6=pink
#
# EDIT THIS to match your own domain. Entries reference entity filenames
# (without .md) in wiki/entities/. Anything not listed here still renders —
# see "unplaced" auto-layout below.

CLUSTERS = [
    {
        "label": "🏢 Core",
        "color": "4",
        "label_pos": (0, -200),
        "entities": [
            ("Example_Primary_Entity", 0, 0),
        ]
    },
    {
        "label": "📎 Related",
        "color": "5",
        "label_pos": (-1000, -400),
        "entities": [
            ("Example_Related_Entity", -1000, -200),
        ]
    },
]

NODE_W = 280
NODE_H = 90
LABEL_W = 320
LABEL_H = 50


def uid():
    return uuid.uuid4().hex[:12]


def read_entity(path: Path) -> dict:
    """Extract frontmatter + wikilinks from an entity file."""
    text = path.read_text(encoding="utf-8")

    fm = {}
    fm_match = re.search(r"^---\n(.*?)\n---", text, re.DOTALL)
    if fm_match:
        for line in fm_match.group(1).splitlines():
            if ":" in line:
                k, _, v = line.partition(":")
                fm[k.strip()] = v.strip()

    # Extract first heading as display title
    h1 = re.search(r"^# (.+)$", text, re.MULTILINE)
    title = h1.group(1) if h1 else path.stem

    # Extract all [[wikilinks]]
    links = re.findall(r"\[\[([^\]|#]+?)(?:[|#][^\]]+)?\]\]", text)
    links = [l.strip() for l in links if l.strip() != path.stem]

    return {
        "stem": path.stem,
        "title": title,
        "type": fm.get("type", "entity"),
        "confidence": fm.get("confidence", ""),
        "inbound_links": fm.get("inbound_links", "0"),
        "tags": fm.get("tags", ""),
        "links": list(dict.fromkeys(links)),  # unique, order-preserving
    }


def entity_label(info: dict) -> str:
    tag_str = info["tags"].strip("[]").replace('"', "").replace("'", "")
    tags = [t.strip() for t in tag_str.split(",")][:3]
    tag_line = " · ".join(tags) if tags else ""
    conf = info["confidence"]
    conf_str = f"  ⬤ {conf}" if conf else ""
    return f"**{info['stem'].replace('_', ' ')}**\n{tag_line}{conf_str}"


def cluster_label_text(cluster: dict) -> str:
    return cluster["label"]


def build_canvas(output_path: Path):
    # Load all entities
    entity_files = {p.stem: p for p in ENTITIES_DIR.glob("*.md")}
    entities = {stem: read_entity(p) for stem, p in entity_files.items()}

    all_stems = set(entities.keys())

    nodes = []
    edges = []
    node_ids = {}  # stem → canvas node id

    # ── Cluster label nodes ────────────────────────────────────────────────────
    for cluster in CLUSTERS:
        lx, ly = cluster["label_pos"]
        lid = "lbl_" + uid()
        nodes.append({
            "id": lid,
            "type": "text",
            "text": cluster["label"],
            "x": lx,
            "y": ly,
            "width": LABEL_W,
            "height": LABEL_H,
            "color": cluster["color"],
        })

    # ── Entity nodes ──────────────────────────────────────────────────────────
    placed = set()
    for cluster in CLUSTERS:
        for stem, ex, ey in cluster["entities"]:
            if stem not in entities:
                # Entity referenced in layout but not found — skip
                continue
            info = entities[stem]
            nid = "ent_" + uid()
            node_ids[stem] = nid
            placed.add(stem)

            # Use file node type so Obsidian opens the file on click
            rel_path = f"wiki/entities/{stem}.md"
            nodes.append({
                "id": nid,
                "type": "file",
                "file": rel_path,
                "x": ex - NODE_W // 2,
                "y": ey - NODE_H // 2,
                "width": NODE_W,
                "height": NODE_H,
                "color": cluster["color"],
            })

    # ── Any entities NOT in layout — append as a row at the bottom ───────────
    unplaced = [s for s in all_stems if s not in placed]
    if unplaced:
        for i, stem in enumerate(sorted(unplaced)):
            col = i % 4
            row = i // 4
            ex = -600 + col * 320
            ey = 1700 + row * 150
            nid = "ent_" + uid()
            node_ids[stem] = nid
            nodes.append({
                "id": nid,
                "type": "file",
                "file": f"wiki/entities/{stem}.md",
                "x": ex,
                "y": ey,
                "width": NODE_W,
                "height": NODE_H,
                "color": "6",
            })

    # ── Edges from wikilinks ──────────────────────────────────────────────────
    seen_edges = set()
    for stem, info in entities.items():
        if stem not in node_ids:
            continue
        src_id = node_ids[stem]
        for target_stem in info["links"]:
            if target_stem not in node_ids:
                continue
            # Deduplicate bidirectional edges
            edge_key = tuple(sorted([stem, target_stem]))
            if edge_key in seen_edges:
                continue
            seen_edges.add(edge_key)

            tgt_id = node_ids[target_stem]
            edges.append({
                "id": "edge_" + uid(),
                "fromNode": src_id,
                "fromSide": "right",
                "toNode": tgt_id,
                "toSide": "left",
            })

    canvas = {"nodes": nodes, "edges": edges}

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(canvas, f, ensure_ascii=False, indent=2)

    print(f"Canvas written: {output_path}")
    print(f"  Nodes: {len(nodes)} ({len([n for n in nodes if n['type']=='file'])} entity, {len([n for n in nodes if n['type']=='text'])} label)")
    print(f"  Edges: {len(edges)} (from wikilink graph)")
    print(f"  Unplaced entities appended at bottom: {unplaced or 'none'}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Build Wiki OS KB Canvas")
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    args = parser.parse_args()
    build_canvas(Path(args.output))
