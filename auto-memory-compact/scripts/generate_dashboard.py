#!/usr/bin/env python3
"""
Generate Self-Improvement Dashboard markdown.
Default: output to stdout only (dry-run).
Use --write to write to SELF_IMPROVEMENT_DASHBOARD.md.
"""

import argparse
import json
import sys
from pathlib import Path


DEFAULT_MEMORY_DIR = "/Users/qunqing/.claude/memory"
DEFAULT_VERSION = "v0.2"


def count_files_in_dir(dir_path: Path) -> int:
    """Count .md files in directory."""
    if not dir_path.exists() or not dir_path.is_dir():
        return 0
    return len([f for f in dir_path.iterdir() if f.is_file() and f.suffix == ".md"])


def get_latest_file(dir_path: Path, pattern: str = "*.md") -> str:
    """Get name of latest modified file matching pattern."""
    if not dir_path.exists() or not dir_path.is_dir():
        return "none"
    files = list(dir_path.glob(pattern))
    if not files:
        return "none"
    latest = max(files, key=lambda f: f.stat().st_mtime)
    return latest.name


def parse_memory_info(memory_path: Path) -> dict:
    """Parse memory directory for dashboard info."""
    info = {
        "inbox_count": 0,
        "errors_count": 0,
        "reviews_count": 0,
        "promotions_count": 0,
        "skill_candidates_count": 0,
        "pattern_count": 0,
        "active_warnings": 0,
        "archived_notes": 0,
        "target_status": "unknown",
        "last_review": "none",
        "last_compact": "none",
    }

    # Inbox
    inbox = memory_path / "inbox"
    info["inbox_count"] = count_files_in_dir(inbox)

    # Records
    records = memory_path / "records"
    if records.exists():
        info["errors_count"] = count_files_in_dir(records / "errors")
        info["reviews_count"] = count_files_in_dir(records / "reviews")

        # Promotions (v0.1 style)
        promos = records / "promotions"
        info["promotions_count"] = count_files_in_dir(promos)

        # Candidates (v0.2 style)
        candidates = records / "candidates"
        if candidates.exists():
            info["promotions_count"] += count_files_in_dir(candidates / "promotions")
            info["skill_candidates_count"] = count_files_in_dir(candidates / "skills")

        # Patterns
        patterns = records / "patterns"
        info["pattern_count"] = count_files_in_dir(patterns)

    # Latest review
    reviews_dir = records / "reviews" if records.exists() else None
    if reviews_dir and reviews_dir.exists():
        files = [f for f in reviews_dir.glob("*.md") if "formal-self-improvement-review" in f.name or "self-improvement-system" in f.name]
        if files:
            latest = max(files, key=lambda f: f.stat().st_mtime)
            info["last_review"] = latest.stem[:17]  # Truncate timestamp

    # Target structure status
    inspect_script = Path(__file__).parent.parent / "scripts" / "inspect_memory.py"
    if inspect_script.exists():
        import subprocess
        try:
            result = subprocess.run(
                [sys.executable, str(inspect_script), str(memory_path)],
                capture_output=True, text=True, timeout=10
            )
            if result.returncode == 0:
                data = json.loads(result.stdout)
                info["target_status"] = data.get("target_structure_status", "unknown")
                info["active_warnings"] = data.get("active_warning_count", 0)
                info["archived_notes"] = data.get("archived_note_count", 0)
        except Exception:
            pass

    return info


def generate_dashboard(version: str, memory_dir: str) -> str:
    """Generate dashboard markdown content."""
    memory_path = Path(memory_dir).expanduser().resolve()
    info = parse_memory_info(memory_path)

    lines = [
        "# Self-Improvement Dashboard",
        "",
        "## System",
        f"- Version: {version}",
        f"- Last review: {info['last_review']}",
        f"- Target structure: {info['target_status']}",
        "",
        "## Status",
        f"- Inbox count: {info['inbox_count']}",
        f"- Errors count: {info['errors_count']}",
        f"- Active patterns: {info['pattern_count']}",
        f"- Proposed promotions: {info['promotions_count']}",
        f"- Skill candidates: {info['skill_candidates_count']}",
        f"- Reviews: {info['reviews_count']}",
        "",
        "## Health",
        f"- Active warnings: {info['active_warnings']}",
        f"- Archived notes: {info['archived_notes']}",
        "",
        "## Next Actions",
        "- Review inbox corrections",
        "- Check unresolved errors",
        "- Update pattern index if needed",
        "- Run compact if warnings present",
        "",
        "## Warning",
        "This dashboard is for human orientation only. It is NOT active rules.",
    ]

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Generate Self-Improvement Dashboard")
    parser.add_argument("--memory-dir", default=DEFAULT_MEMORY_DIR, help="Memory directory path")
    parser.add_argument("--version", default=DEFAULT_VERSION, help="System version")
    parser.add_argument("--write", action="store_true", help="Write to SELF_IMPROVEMENT_DASHBOARD.md")

    args = parser.parse_args()

    dashboard_content = generate_dashboard(args.version, args.memory_dir)

    if args.write:
        dashboard_path = Path(args.memory_dir).expanduser().resolve() / "SELF_IMPROVEMENT_DASHBOARD.md"
        with open(dashboard_path, "w", encoding="utf-8") as f:
            f.write(dashboard_content)
        print(f"Written to {dashboard_path}", file=sys.stderr)
    else:
        print(dashboard_content)


if __name__ == "__main__":
    main()
