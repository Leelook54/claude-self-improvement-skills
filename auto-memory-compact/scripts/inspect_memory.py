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
        "archived_notes": [],
        # v0.2 structure checks
        "dashboard_exists": False,
        "dashboard_line_count": 0,
        "pattern_index_exists": False,
        "archive_index_exists": False,
        "compact_policy_exists": False,
        "compact_plans_dir_exists": False,
        "compact_reports_dir_exists": False,
        "candidates_dir_exists": False,
        "target_structure_status": "unknown",
        "active_warning_count": 0,
        "archived_note_count": 0,
        # PreCompact snapshot checks
        "precompact_dir_exists": False,
        "precompact_snapshots_count": 0,
        "latest_precompact_snapshot": None,
    }

    if not path.exists():
        result["warnings"].append("Directory does not exist")
        return result

    # Check MEMORY.md
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

    # Check SELF_IMPROVEMENT_DASHBOARD.md
    dashboard = path / "SELF_IMPROVEMENT_DASHBOARD.md"
    if dashboard.exists():
        result["dashboard_exists"] = True
        with open(dashboard, "r", encoding="utf-8") as f:
            lines = f.readlines()
            result["dashboard_line_count"] = len(lines)
            if len(lines) > 120:
                result["warnings"].append("Dashboard exceeds 120 lines")

    # Scan all markdown files
    for md_file in path.rglob("*.md"):
        if md_file.name not in ["MEMORY.md", "SELF_IMPROVEMENT_DASHBOARD.md"]:
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

    # v0.2 structure checks
    records_path = path / "records"

    # Pattern index
    pattern_index = records_path / "patterns" / "PATTERN_INDEX.md"
    result["pattern_index_exists"] = pattern_index.exists()

    # Archive index
    archive_index = path / "archive" / "summaries" / "ARCHIVE_INDEX.md"
    result["archive_index_exists"] = archive_index.exists()

    # Compact structure
    compact_path = path / "compact"
    result["compact_policy_exists"] = (compact_path / "COMPACT_POLICY.md").exists()
    result["compact_plans_dir_exists"] = (compact_path / "plans").is_dir()
    result["compact_reports_dir_exists"] = (compact_path / "reports").is_dir()

    # Candidates structure
    result["candidates_dir_exists"] = (records_path / "candidates").is_dir()

    # Determine target structure status
    # Core v0.2 nodes that must exist
    v02_mandatory = [
        pattern_index.exists(),
        result["candidates_dir_exists"],
        result["compact_plans_dir_exists"],
        result["compact_reports_dir_exists"],
    ]

    if all(v02_mandatory):
        result["target_structure_status"] = "v0.2"
    elif not any(v02_mandatory):
        result["target_structure_status"] = "v0.1"
    else:
        result["target_structure_status"] = "partial-v0.2"

    # Check for default_load: true in records
    if records_path.exists():
        for md_file in records_path.rglob("*.md"):
            try:
                with open(md_file, "r", encoding="utf-8") as f:
                    content = f.read(1024)
                if "default_load: true" in content or "default_load:true" in content:
                    rel_path = md_file.relative_to(records_path)
                    result["warnings"].append(f"default_load: true found in {rel_path}")
            except Exception:
                pass

    # PreCompact snapshot checks
    precompact_path = path / "compact" / "precompact"
    result["precompact_dir_exists"] = precompact_path.is_dir()
    if precompact_path.is_dir():
        snapshots = sorted(precompact_path.glob("*_precompact-snapshot.md"))
        result["precompact_snapshots_count"] = len(snapshots)
        if snapshots:
            latest = snapshots[-1]
            result["latest_precompact_snapshot"] = str(latest.relative_to(path))

    # Set counts
    result["active_warning_count"] = len(result["warnings"])
    result["archived_note_count"] = len(result["archived_notes"])

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
