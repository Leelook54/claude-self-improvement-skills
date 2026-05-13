#!/usr/bin/env python3
"""
Discover Claude Code session files for future review.
Dry-run only: finds and counts, does not read full content.
"""

import argparse
import json
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path


DEFAULT_ROOT = "/Users/qunqing/.claude"
DEFAULT_DAYS = 7


def find_session_files(root: Path, days: int) -> dict:
    """Find session files within time window."""
    result = {
        "root": str(root),
        "exists": root.exists(),
        "candidate_files_count": 0,
        "candidate_files_sample": [],
        "newest_mtime": None,
        "oldest_mtime": None,
        "warnings": [],
    }

    if not root.exists():
        result["warnings"].append(f"Root does not exist: {root}")
        return result

    cutoff = datetime.now() - timedelta(days=days)
    candidates = []

    # Search patterns
    search_patterns = [
        "**/*.jsonl",
        "**/transcript*",
        "**/session*",
        "**/.claude/projects/**/*.jsonl",
    ]

    for pattern in search_patterns:
        try:
            for f in root.glob(pattern):
                if not f.is_file():
                    continue
                # Skip non-session files
                if f.stat().st_size > 10 * 1024 * 1024:  # Skip > 10MB
                    continue
                if "memory" in f.name or "records" in f.name:
                    continue
                # Check modification time
                mtime = datetime.fromtimestamp(f.stat().st_mtime)
                if mtime >= cutoff:
                    candidates.append({
                        "path": str(f.relative_to(root)),
                        "size": f.stat().st_size,
                        "mtime": mtime.isoformat(),
                    })
        except PermissionError:
            result["warnings"].append(f"Permission denied: {pattern}")
        except Exception as e:
            result["warnings"].append(f"Error scanning {pattern}: {str(e)}")

    # Dedupe by path
    seen = set()
    unique = []
    for c in candidates:
        if c["path"] not in seen:
            seen.add(c["path"])
            unique.append(c)

    unique.sort(key=lambda x: x["mtime"], reverse=True)
    result["candidate_files_count"] = len(unique)
    result["candidate_files_sample"] = [c["path"] for c in unique[:10]]

    if unique:
        result["newest_mtime"] = unique[0]["mtime"]
        result["oldest_mtime"] = unique[-1]["mtime"]

    return result


def main():
    parser = argparse.ArgumentParser(description="Discover session files")
    parser.add_argument("--root", default=DEFAULT_ROOT, help="Root directory to search")
    parser.add_argument("--days", type=int, default=DEFAULT_DAYS, help="Days to look back")

    args = parser.parse_args()

    root = Path(args.root).expanduser().resolve()
    result = find_session_files(root, args.days)

    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
