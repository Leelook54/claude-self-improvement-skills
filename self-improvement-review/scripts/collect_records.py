#!/usr/bin/env python3
"""
Collect records from Claude Code self-improvement records directory.
Read-only scan, outputs JSON summary.
Supports both v0.1 and v0.2 directory structures.
"""

import json
import os
import sys
import re
from pathlib import Path
from datetime import datetime


# v0.1 root-level categories
V01_CATEGORIES = [
    "corrections",
    "errors",
    "reviews",
    "promotions",
    "skill-candidates",
    "rejected",
]

# v0.2 categories from root level
V02_ROOT_CATEGORIES = [
    "patterns",
    "resolved",
]

# v0.2 candidates subdirectories mapping
V02_CANDIDATES_MAP = {
    "promotions": "promotions",
    "skills": "skill-candidates",
    "capabilities": "capability-requests",
}


def derive_records_path() -> str:
    """Derive records path with priority: CLAUDE_RECORDS_DIR, project memory records, fallback."""
    # 1. Env var
    if "CLAUDE_RECORDS_DIR" in os.environ:
        return os.environ["CLAUDE_RECORDS_DIR"]

    cwd = os.getcwd()
    home = str(Path.home())

    # 2. Project memory records: ~/.claude/projects/<project>/memory/records/
    if cwd.startswith(home):
        project_key = cwd[len(home):].lstrip("/").replace("/", "-")
        if project_key:
            project_records = os.path.join(home, ".claude", "projects", project_key, "memory", "records")
            return project_records

    # 3. Fallback
    return os.path.join(home, ".claude", "memory", "records")


def parse_frontmatter(file_path: Path) -> dict:
    """Parse frontmatter from markdown file. Returns empty dict if not found."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read(2048)
        if content.startswith("---"):
            parts = content.split("---", 2)
            if len(parts) >= 3:
                fm = {}
                for line in parts[2].split("\n")[:50]:
                    if ":" in line:
                        key, _, value = line.partition(":")
                        fm[key.strip()] = value.strip()
                return fm
    except Exception:
        pass
    return {}


def collect_records(records_path: str) -> dict:
    """Scan records directory and return JSON summary."""
    result = {
        "path": records_path,
        "exists": False,
        "markdown_file_count": 0,
        "categories": [],
        "files_by_category": {},
        "warnings": [],
        "status_counts": {},
        "type_counts": {},
        "candidate_counts": {},
        "pattern_count": 0,
        "unresolved_errors_count": 0,
        "compatibility_mode": "unknown",
        "dry_run": False,
    }

    path = Path(records_path)

    if not path.exists():
        result["warnings"].append(f"Records path does not exist: {records_path}")
        return result

    if not path.is_dir():
        result["warnings"].append(f"Records path is not a directory: {records_path}")
        return result

    result["exists"] = True

    # Detect compatibility mode
    has_v01 = (path / "corrections").exists()
    has_v02 = any((path / d).exists() for d in V02_ROOT_CATEGORIES + ["candidates"])
    has_v02_candidates = (path / "candidates").exists()

    if has_v01 and has_v02:
        result["compatibility_mode"] = "mixed"
    elif has_v02 or has_v02_candidates:
        result["compatibility_mode"] = "v0.2"
    else:
        result["compatibility_mode"] = "v0.1"

    # Phase 1: Root-level categories (v0.1 + v0.2 root)
    all_root_categories = V01_CATEGORIES + V02_ROOT_CATEGORIES

    for category in all_root_categories:
        category_path = path / category
        files = []

        if category_path.exists() and category_path.is_dir():
            for f in sorted(category_path.iterdir()):
                if f.is_file() and f.suffix == ".md":
                    files.append(str(f))
                    result["markdown_file_count"] += 1

                    # Check frontmatter
                    fm = parse_frontmatter(f)
                    if fm:
                        # Check for default_load: true
                        if fm.get("default_load", "false") != "false":
                            result["warnings"].append(f"{f.name}: default_load is not false")
                        # Check promotion candidate
                        if fm.get("type") == "promotion_candidate":
                            if fm.get("promote_requires_user_approval", "true") != "true":
                                result["warnings"].append(f"{f.name}: promotion_candidate missing promote_requires_user_approval: true")

        if files:
            result["categories"].append(category)
            result["files_by_category"][category] = files

    # Phase 2: candidates/ subdirectories (v0.2)
    candidates_path = path / "candidates"
    if candidates_path.exists() and candidates_path.is_dir():
        for subdir, target in V02_CANDIDATES_MAP.items():
            sub_path = candidates_path / subdir
            if sub_path.exists():
                files = []
                for f in sorted(sub_path.iterdir()):
                    if f.is_file() and f.suffix == ".md":
                        files.append(str(f))
                        result["markdown_file_count"] += 1

                        # Check frontmatter
                        fm = parse_frontmatter(f)
                        if fm:
                            if fm.get("default_load", "false") != "false":
                                result["warnings"].append(f"{f.name}: default_load is not false")
                            if fm.get("type") == "promotion_candidate":
                                if fm.get("promote_requires_user_approval", "true") != "true":
                                    result["warnings"].append(f"{f.name}: promotion_candidate missing promote_requires_user_approval: true")

                if files:
                    if target not in result["categories"]:
                        result["categories"].append(target)
                        result["files_by_category"][target] = []
                    result["files_by_category"][target].extend(files)

    # Phase 3: Legacy candidates (v0.1 style at root)
    legacy_candidates = ["capability-requests"]
    for legacy in legacy_candidates:
        legacy_path = path / legacy
        if legacy_path.exists() and legacy_path.is_dir():
            files = []
            for f in sorted(legacy_path.iterdir()):
                if f.is_file() and f.suffix == ".md":
                    files.append(str(f))
                    result["markdown_file_count"] += 1
            if files:
                if legacy not in result["categories"]:
                    result["categories"].append(legacy)
                    result["files_by_category"][legacy] = files

    # Calculate status_counts and type_counts
    result["status_counts"] = {cat: len(result["files_by_category"].get(cat, [])) for cat in result["categories"]}
    result["type_counts"] = dict(result["status_counts"])

    # Calculate candidate_counts
    for subdir, target in V02_CANDIDATES_MAP.items():
        sub_path = candidates_path / subdir if candidates_path.exists() else None
        if sub_path and sub_path.exists():
            count = len([f for f in sub_path.iterdir() if f.is_file() and f.suffix == ".md"])
            result["candidate_counts"][subdir] = count
        else:
            result["candidate_counts"][subdir] = 0

    # Calculate pattern_count
    patterns_path = path / "patterns"
    if patterns_path.exists():
        result["pattern_count"] = len([f for f in patterns_path.iterdir() if f.is_file() and f.suffix == ".md"])

    # Calculate unresolved_errors_count
    errors_count = len(result["files_by_category"].get("errors", []))
    resolved_count = len(result["files_by_category"].get("resolved", []))
    result["unresolved_errors_count"] = max(0, errors_count - resolved_count)

    # Check for unexpected directories
    unexpected = []
    expected_dirs = set(V01_CATEGORIES + V02_ROOT_CATEGORIES + ["candidates"] + list(V02_CANDIDATES_MAP.keys()))
    for item in path.iterdir():
        if item.is_dir() and item.name not in expected_dirs:
            unexpected.append(item.name)
    if unexpected:
        result["warnings"].append(f"Unexpected directories: {', '.join(unexpected)}")

    return result


def main():
    records_path = None
    dry_run = False

    args = sys.argv[1:]
    i = 0
    while i < len(args):
        arg = args[i]
        if arg in ("-h", "--help"):
            print("Usage: collect_records.py [--records-dir <path>] [--dry-run] [<records_path>]")
            print("  --records-dir <path> : explicit path via flag")
            print("  --dry-run            : no-op flag (read-only)")
            print("  <records_path>       : legacy positional argument")
            print("  (no args)            : auto-derive path")
            sys.exit(0)
        elif arg == "--records-dir" and i + 1 < len(args):
            records_path = args[i + 1]
            i += 2
        elif arg == "--dry-run":
            dry_run = True
            i += 1
        elif not arg.startswith("-"):
            records_path = arg
            i += 1
        else:
            print(json.dumps({"error": f"Unknown argument: {arg}"}))
            sys.exit(1)

    if records_path is None:
        records_path = derive_records_path()

    result = collect_records(records_path)
    result["dry_run"] = dry_run
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
