import os
import sys
import hashlib
import shutil

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DIR = os.path.join(BASE_DIR, ".raw")
DUPE_DIR = os.path.join(RAW_DIR, "duplicates")

os.makedirs(DUPE_DIR, exist_ok=True)

def calculate_checksum(filepath, chunk_size=8192):
    """Calculates the MD5 hash of a file's binary contents securely."""
    file_hash = hashlib.md5()
    try:
        with open(filepath, "rb") as f:
            chunk = f.read(chunk_size)
            while chunk:
                file_hash.update(chunk)
                chunk = f.read(chunk_size)
        return file_hash.hexdigest()
    except Exception as e:
        print(f"[ERR] Hash failed for {filepath}: {e}")
        return None

def dedupe_directory(target_path):
    """Scans a directory recursively to archive byte-for-byte duplicated files."""
    if not os.path.exists(target_path):
        return

    print(f"[{target_path}] Commencing The Archivist Deduplication Sweep...")
    seen_hashes = {}
    dupes_found = 0

    for root, _, files in os.walk(target_path):
        # Ignore our internal utility folders
        if "archive" in root or "duplicates" in root:
            continue
            
        for file in files:
            if file.startswith('.'):
                continue
                
            file_path = os.path.join(root, file)
            file_hash = calculate_checksum(file_path)
            
            if not file_hash:
                continue

            if file_hash in seen_hashes:
                original_path = seen_hashes[file_hash]
                print(f"[DUPE] Found exact replicate: '{file}' mirrors '{os.path.basename(original_path)}'")
                
                # Move the duplicate safely into the duplicate folder
                safe_dupe_name = f"{file_hash[:6]}_{file}"
                destination = os.path.join(DUPE_DIR, safe_dupe_name)
                
                try:
                    shutil.move(file_path, destination)
                    dupes_found += 1
                except Exception as e:
                    print(f"    -> [ERR] Could not quarantine duplicate: {e}")
            else:
                seen_hashes[file_hash] = file_path

    print(f"[DEDUPE COMPLETE] The Archivist isolated {dupes_found} redundant payloads out of {len(seen_hashes) + dupes_found} active raw files.")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        target = sys.argv[1]
    else:
        target = RAW_DIR
    dedupe_directory(target)
