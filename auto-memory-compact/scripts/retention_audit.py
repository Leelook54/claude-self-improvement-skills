#!/usr/bin/env python3
"""
Retention audit for Claude Code self-improvement memory.
Read-only scan, outputs JSON summary.
Identifies file accumulation and overwrite risk.
"""

import argparse
import json
import os
import sys
from pathlib import Path
from datetime import datetime


DEFAULT_MEMORY_DIR = "/Users/qunqing/.claude/memory"

# Fixed-name slug patterns that risk overwriting
FIXED_NAME_SLUGS = [
    "smoke-test",
    "dry-run",
    "review",
    "compact",
    "cleanup",
]


def scan_memory(memory_dir: str) -> dict:
    """Scan memory directory and return JSON audit summary."""
    result = {
        "memory_dir": memory_dir,
        "exists": False,
        "total_files": 0,
        "total_markdown_files": 0,
        "total_dirs": 0,
        "total_size_bytes": 0,
        "active_records_files": 0,
        "archive_raw_files": 0,
        "archive_summaries_files": 0,
        "records_errors_count": 0,
        "records_reviews_count": 0,
        "records_candidates_count": 0,
        "records_patterns_topic_count": 0,
        "records_patterns_index_exists": False,
        "compact_plans_count": 0,
        "compact_reports_count": 0,
        "dashboard_exists": False,
        "dashboard_size_bytes": 0,
        "duplicate_basename_groups": {},
        "fixed_name_overwrite_risk": [],
        "retention_warnings": [],
        "compact_recommended": False,
        "recommended_actions": [],
    }

    path = Path(memory_dir)
    if not path.exists():
        result["retention_warnings"].append("Memory directory does not exist")
        return result

    result["exists"] = True

    # Collect all files with metadata
    all_files = []
    basename_count = {}

    for root, dirs, files in os.walk(path):
        result["total_dirs"] += len(dirs)
        for fname in files:
            full_path = os.path.join(root, fname)
            rel_path = os.path.relpath(full_path, path)
            size = os.path.getsize(full_path)
            mtime = os.path.getmtime(full_path)

            result["total_files"] += 1
            result["total_size_bytes"] += size

            if fname.endswith(".md"):
                result["total_markdown_files"] += 1
                all_files.append({
                    "path": rel_path,
                    "basename": fname,
                    "size": size,
                    "mtime": mtime,
                })
                basename_count[fname] = basename_count.get(fname, 0) + 1

            # Count by directory
            if "records/errors" in rel_path:
                result["records_errors_count"] += 1
                result["active_records_files"] += 1
            elif "records/reviews" in rel_path:
                result["records_reviews_count"] += 1
                result["active_records_files"] += 1
            elif "records/candidates" in rel_path:
                result["records_candidates_count"] += 1
            elif "records/patterns" in rel_path:
                if fname == "PATTERN_INDEX.md":
                    result["records_patterns_index_exists"] = True
                elif not fname.startswith("PATTERN_INDEX"):
                    result["records_patterns_topic_count"] += 1
            elif "archive/raw" in rel_path:
                result["archive_raw_files"] += 1
            elif "archive/summaries" in rel_path:
                result["archive_summaries_files"] += 1
            elif "compact/plans" in rel_path:
                result["compact_plans_count"] += 1
            elif "compact/reports" in rel_path:
                result["compact_reports_count"] += 1

    # Dashboard
    dashboard_path = path / "SELF_IMPROVEMENT_DASHBOARD.md"
    if dashboard_path.exists():
        result["dashboard_exists"] = True
        result["dashboard_size_bytes"] = dashboard_path.stat().st_size

    # Duplicate basename groups (count > 1)
    result["duplicate_basename_groups"] = {
        bn: cnt for bn, cnt in basename_count.items() if cnt > 1
    }

    # Fixed-name overwrite risk
    for f in all_files:
        bn = f["basename"]
        if any(slug in bn for slug in FIXED_NAME_SLUGS):
            # Check if has HHMMSS timestamp
            if not any(c.isdigit() and len(c) == 6 for c in bn.split("_")):
                result["fixed_name_overwrite_risk"].append(f["path"])

    # Retention warnings
    if result["total_files"] > 500:
        result["retention_warnings"].append(f"total_files={result['total_files']} > 500")
    if result["records_errors_count"] > 30:
        result["retention_warnings"].append(f"records/errors={result['records_errors_count']} > 30")
    if result["records_reviews_count"] > 25:
        result["retention_warnings"].append(f"records/reviews={result['records_reviews_count']} > 25")
    if result["archive_raw_files"] > 300:
        result["retention_warnings"].append(f"archive/raw={result['archive_raw_files']} > 300")

    # Compact recommended
    result["compact_recommended"] = any([
        result["total_files"] > 500,
        result["records_errors_count"] > 30,
        result["records_reviews_count"] > 25,
        result["archive_raw_files"] > 300,
        result["fixed_name_overwrite_risk"],
    ])

    # Recommended actions
    if result["total_files"] > 500:
        result["recommended_actions"].append("Consider running compact to archive raw noise")
    if result["fixed_name_overwrite_risk"]:
        result["recommended_actions"].append(f"Use YYYYMMDD_HHMMSS naming for {len(result['fixed_name_overwrite_risk'])} fixed-name reports")
    if result["records_reviews_count"] > 25:
        result["recommended_actions"].append("Archive superseded review reports")
    if result["archive_raw_files"] > 300:
        result["recommended_actions"].append("Summarize archive/raw structure in ARCHIVE_INDEX")

    return result


def main():
    parser = argparse.ArgumentParser(description="Retention audit for memory directory")
    parser.add_argument("--memory-dir", default=DEFAULT_MEMORY_DIR, help="Memory directory path")

    args = parser.parse_args()
    memory_dir = Path(args.memory_dir).expanduser().resolve()
    result = scan_memory(str(memory_dir))
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()