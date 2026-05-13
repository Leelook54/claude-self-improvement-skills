#!/usr/bin/env python3
"""
Discover Claude Code session files for future review.
Dry-run only: finds and counts, does not read full content.
v0.2.2: explicit include/exclude patterns, targets only real session JSONL.
"""

import argparse
import json
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path


DEFAULT_ROOT = "/Users/qunqing/.claude"
DEFAULT_DAYS = 7

# v0.2.2 explicit include patterns (relative to root)
INCLUDE_PATTERNS = [
    "projects/**/*.jsonl",
    "sessions/**/*.jsonl",
    "history.jsonl",
]

# v0.2.2 explicit exclude patterns (relative to root)
EXCLUDE_PATTERNS = [
    "plugins/**",
    "skills/**",
    "cache/**",
    "**/node_modules/**",
    "**/*.js",
    "**/*.ts",
    "**/*.map",
    "**/*.sh",
    "references/*.md",
]


def match_exclude(path_str: str) -> bool:
    """Check if path matches any exclude pattern."""
    path_obj = Path(path_str)
    for pattern in EXCLUDE_PATTERNS:
        # Handle glob patterns
        if "**" in pattern:
            # Convert glob to prefix/suffix match
            prefix = pattern.replace("**/", "").replace("**", "")
            if pattern.startswith("**/"):
                # Suffix match: **/node_modules/** -> ends with node_modules/
                suffix = prefix.rstrip("/")
                if path_str.endswith(suffix) or suffix in path_str.split("/"):
                    return True
            elif "/" not in pattern.lstrip("*"):
                # Extension match: *.js, *.ts
                if path_obj.match(pattern):
                    return True
            else:
                # path prefix match: plugins/**, skills/**
                prefix = pattern.rstrip("/").replace("/**", "")
                if path_str.startswith(prefix + "/") or path_str == prefix:
                    return True
        else:
            # Literal or simple glob
            if path_obj.match(pattern):
                return True
    return False


def find_session_files(root: Path, days: int) -> dict:
    """Find session files within time window using explicit include/exclude."""
    result = {
        "root": str(root),
        "exists": root.exists(),
        "include_patterns": INCLUDE_PATTERNS,
        "exclude_patterns": EXCLUDE_PATTERNS,
        "candidate_files_count": 0,
        "excluded_count": 0,
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
    excluded = []

    # Phase 1: collect from explicit include patterns
    for pattern in INCLUDE_PATTERNS:
        try:
            for f in root.glob(pattern):
                if not f.is_file():
                    continue
                # Skip files > 10MB
                if f.stat().st_size > 10 * 1024 * 1024:
                    continue
                rel_path = str(f.relative_to(root))
                # Apply excludes
                if match_exclude(rel_path):
                    excluded.append(rel_path)
                    continue
                mtime = datetime.fromtimestamp(f.stat().st_mtime)
                if mtime >= cutoff:
                    candidates.append({
                        "path": rel_path,
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
    result["excluded_count"] = len(excluded)
    result["candidate_files_sample"] = [c["path"] for c in unique[:10]]

    if unique:
        result["newest_mtime"] = unique[0]["mtime"]
        result["oldest_mtime"] = unique[-1]["mtime"]

    return result


def main():
    parser = argparse.ArgumentParser(description="Discover session files (v0.2.2)")
    parser.add_argument("--root", default=DEFAULT_ROOT, help="Root directory to search")
    parser.add_argument("--days", type=int, default=DEFAULT_DAYS, help="Days to look back")
    parser.add_argument("--dry-run", action="store_true", help="No-op flag")

    args = parser.parse_args()

    root = Path(args.root).expanduser().resolve()
    result = find_session_files(root, args.days)
    result["dry_run"] = args.dry_run

    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
