#!/usr/bin/env python3
"""
Collect records from Claude Code self-improvement records directory.
Read-only scan, outputs JSON summary.
"""

import json
import os
import sys
from pathlib import Path


DEFAULT_RECORDS_PATH = "/Users/qunqing/.claude/memory/records/"

CATEGORIES = [
    "corrections",
    "errors",
    "reviews",
    "promotions",
    "skill-candidates",
    "rejected",
]


def collect_records(records_path: str) -> dict:
    """Scan records directory and return JSON summary."""
    result = {
        "path": records_path,
        "exists": False,
        "markdown_file_count": 0,
        "categories": [],
        "files_by_category": {},
        "warnings": [],
    }

    path = Path(records_path)

    if not path.exists():
        result["warnings"].append(f"Records path does not exist: {records_path}")
        return result

    if not path.is_dir():
        result["warnings"].append(f"Records path is not a directory: {records_path}")
        return result

    result["exists"] = True

    for category in CATEGORIES:
        category_path = path / category
        files = []

        if category_path.exists() and category_path.is_dir():
            for f in category_path.iterdir():
                if f.is_file() and f.suffix == ".md":
                    files.append(str(f))
                    result["markdown_file_count"] += 1

        if files:
            result["categories"].append(category)
            result["files_by_category"][category] = files

    # Check for unexpected directories
    for item in path.iterdir():
        if item.is_dir() and item.name not in CATEGORIES:
            result["warnings"].append(f"Unexpected directory: {item.name}")

    return result


def main():
    records_path = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_RECORDS_PATH
    result = collect_records(records_path)
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
