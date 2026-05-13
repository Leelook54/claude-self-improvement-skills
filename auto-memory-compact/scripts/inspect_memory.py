#!/usr/bin/env python3
"""Inspect memory directory and output JSON report."""

import json
import os
import sys
from pathlib import Path


def inspect_memory(memory_path: str) -> dict:
    """Inspect a memory directory and return JSON report."""
    path = Path(memory_path).expanduser().resolve()
    result = {
        "path": str(path),
        "exists": path.exists(),
        "memory_md_exists": False,
        "memory_md_line_count": 0,
        "markdown_file_count": 0,
        "topic_files": [],
        "warnings": [],
        "archived_notes": []
    }

    if not path.exists():
        result["warnings"].append("Directory does not exist")
        return result

    memory_md = path / "MEMORY.md"
    if memory_md.exists():
        result["memory_md_exists"] = True
        with open(memory_md, "r", encoding="utf-8") as f:
            lines = f.readlines()
            result["memory_md_line_count"] = len(lines)
            if len(lines) > 150:
                result["warnings"].append("MEMORY.md exceeds 150 lines (cache hygiene warning)")
            elif len(lines) > 100:
                result["warnings"].append("MEMORY.md exceeds 100 lines (cache hygiene note)")

    for md_file in path.rglob("*.md"):
        if md_file.name != "MEMORY.md":
            result["markdown_file_count"] += 1
            rel_path = md_file.relative_to(path)
            result["topic_files"].append(str(rel_path))

            is_archive = str(rel_path).startswith("archive/")
            if md_file.stat().st_size > 50 * 1024:
                msg = f"Large topic file: {rel_path} (>50KB)"
                if is_archive:
                    result["archived_notes"].append(msg)
                else:
                    result["warnings"].append(msg)
            elif md_file.stat().st_size > 20 * 1024:
                msg = f"Archived file size note: {rel_path} (>20KB)" if is_archive else f"Topic file size note: {rel_path} (>20KB)"
                if is_archive:
                    result["archived_notes"].append(msg)
                else:
                    result["warnings"].append(msg)

    return result


def main():
    if len(sys.argv) < 2:
        print(json.dumps({"error": "Usage: inspect_memory.py <memory_path>"}))
        sys.exit(1)

    memory_path = sys.argv[1]
    result = inspect_memory(memory_path)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
