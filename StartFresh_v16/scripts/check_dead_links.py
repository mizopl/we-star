"""Check for dead wikilinks and orphan entities in wiki/entities."""
import os, re
from pathlib import Path

entities_dir = str(Path(__file__).parent.parent / "wiki" / "entities")
# Recursive: Obsidian resolves [[links]] by basename, so subfolders count too.
entity_files = sorted(str(p.relative_to(entities_dir)) for p in Path(entities_dir).rglob('*.md'))
entity_set = set(Path(f).stem for f in entity_files)

dead_links = []
inbound_count = {e: 0 for e in entity_set}

for fname in entity_files:
    src = Path(fname).stem
    with open(os.path.join(entities_dir, fname)) as f:
        content = f.read()
    links = re.findall(r'\[\[([^\]|#]+?)(?:[|#][^\]]+)?\]\]', content)
    for link in links:
        target = link.strip()
        if target in entity_set:
            if target != src:
                inbound_count[target] += 1
        else:
            dead_links.append((fname, target))

print('=== DEAD LINKS ===')
if dead_links:
    for src, tgt in dead_links:
        print(f'  {src} -> [[{tgt}]]')
else:
    print('  None found.')

print()
print('=== ORPHANS (0 inbound entity links) ===')
orphans = [e for e, c in inbound_count.items() if c == 0]
if orphans:
    for o in orphans:
        print(f'  {o}.md')
else:
    print('  None found.')
