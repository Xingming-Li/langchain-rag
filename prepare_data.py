from pathlib import Path
import re

root = Path.cwd()

for md_file in root.rglob("*.md"):
    # Skip files already in the root directory
    if md_file.parent == root:
        continue

    # Normalize filename
    new_name = md_file.name.lower()
    new_name = re.sub(r"\s+", "_", new_name)

    target = root / new_name

    # Handle name collisions by appending a counter
    if target.exists():
        stem = target.stem
        suffix = target.suffix
        counter = 1
        while True:
            candidate = root / f"{stem}_{counter}{suffix}"
            if not candidate.exists():
                target = candidate
                break
            counter += 1

    md_file.rename(target)
