import os

WIKI_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "wiki")

print("[START] Scanning Wiki nodes for broken 'raw/' path citations...")
for root, _, files in os.walk(WIKI_DIR):
    for f in files:
        if f.endswith(".md") or f.endswith(".xml"):
            path = os.path.join(root, f)
            with open(path, "r", encoding="utf-8") as file:
                content = file.read()
                
            # Replace target patterns specifically to avoid maiming real words
            if "raw/" in content and ".raw/" not in content:
                new_content = content.replace('origin_source="raw/', 'origin_source=".raw/')
                new_content = new_content.replace('[../../raw/', '[../../.raw/')
                new_content = new_content.replace('["raw/', '[".raw/')
                new_content = new_content.replace(': [../raw/', ': [../.raw/')  # Handle direct sibling links
                
                with open(path, "w", encoding="utf-8") as file:
                    file.write(new_content)
                print(f"[REPAIRED] Fixed pointers in: {f}")

print("[COMPLETE] All global citations have been safely redirected to the hidden /.raw/ vault.")
