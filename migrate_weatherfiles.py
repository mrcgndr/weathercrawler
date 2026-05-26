#!/usr/bin/env python3

import argparse
from datetime import datetime
from pathlib import Path


def _is_structured_json(root: Path, file_path: Path) -> bool:
    relative = file_path.relative_to(root)
    if len(relative.parts) < 4:
        return False

    year, month, day = relative.parts[0], relative.parts[1], relative.parts[2]
    try:
        datetime.strptime(f"{year}/{month}/{day}", "%Y/%m/%d")
    except ValueError:
        return False

    filename = relative.parts[3]
    if len(relative.parts) != 4:
        return False

    return len(filename) >= 6 and filename[:4].isdigit() and filename[4] == "_"


def _target_path(root: Path, file_path: Path) -> Path:
    if len(file_path.name) >= 6 and file_path.name[:4].isdigit() and file_path.name[4] == "_":
        relative = file_path.relative_to(root)
        date = datetime.strptime("/".join(relative.parts[:3]), "%Y/%m/%d")
        filename = file_path.name
    else:
        date = datetime.strptime(file_path.name[:8], "%Y%m%d")
        filename = f"{file_path.name[9:13]}_{file_path.name[14:]}"

    return root / date.strftime("%Y") / date.strftime("%m") / date.strftime("%d") / filename


def migrate(root_dir: str) -> int:
    root = Path(root_dir).resolve()
    moved_files = 0

    for file_path in sorted(root.rglob("*.json")):
        if _is_structured_json(root, file_path):
            continue

        try:
            target = _target_path(root, file_path)
        except ValueError:
            print(f"Skipping {file_path}: filename does not start with YYYYMMDD")
            continue

        target.parent.mkdir(parents=True, exist_ok=True)
        if file_path.resolve() == target.resolve():
            continue

        file_path.rename(target)
        moved_files += 1
        print(f"Moved {file_path} -> {target}")

    return moved_files


def main() -> None:
    parser = argparse.ArgumentParser(description="Move weather JSON files into YYYY/MM/DD subdirectories.")
    parser.add_argument("directory", help="Base directory containing weather JSON files")
    args = parser.parse_args()

    moved = migrate(args.directory)
    print(f"Migration finished. Moved {moved} files.")


if __name__ == "__main__":
    main()
