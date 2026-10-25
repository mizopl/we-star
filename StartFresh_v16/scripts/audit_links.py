"""Audit wikilink inbound counts vs frontmatter values."""
import os, re
from pathlib import Path

entities_dir = str(Path(__file__).parent.parent / "wiki" / "entities")
entity_names = {f.replace('.md', '') for f in os.listdir(entities_dir) if f.endswith('.md')}

inbound_occ = {e: 0 for e in entity_names}
inbound_files = {e: set() for e in entity_names}

for fname in os.listdir(entities_dir):
    if not fname.endswith('.md'):
        continue
    src = fname.replace('.md', '')
    content = open(os.path.join(entities_dir, fname)).read()
    links = re.findall(r'\[\[([^\]]+)\]\]', content)
    seen_in_file = set()
    for link in links:
        if link in inbound_occ:
            inbound_occ[link] += 1
            if link != src:
                inbound_files[link].add(src)

fm_vals = {}
for fname in os.listdir(entities_dir):
    if not fname.endswith('.md'):
        continue
    content = open(os.path.join(entities_dir, fname)).read()
    m = re.search(r'inbound_links:\s*(\d+)', content)
    fm_vals[fname.replace('.md', '')] = int(m.group(1)) if m else -1

mismatches = []
for e in sorted(entity_names):
    occ = inbound_occ[e]
    fm = fm_vals[e]
    if fm != occ:
        mismatches.append((e, fm, occ))

if mismatches:
    print("FRONTMATTER MISMATCHES (entity: stored -> actual):")
    for e, fm, occ in mismatches:
        print(f"  {e}: {fm} -> {occ}")
else:
    print("All frontmatter inbound_links values are accurate.")

print()
print("Full counts:")
for e in sorted(entity_names):
    print(f"  {e}: occ={inbound_occ[e]}, unique_files={len(inbound_files[e])}, fm={fm_vals[e]}")
