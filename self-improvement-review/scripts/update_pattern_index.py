#!/usr/bin/env python3
"""
Update pattern index for friction patterns.
Default: dry-run, output JSON only.
Use --write to create/update PATTERN_INDEX.md.
"""

import argparse
import json
import sys
from pathlib import Path


DEFAULT_PATTERNS_DIR = "/Users/qunqing/.claude/memory/records/patterns"


def parse_pattern_frontmatter(file_path: Path) -> dict:
    """Parse pattern frontmatter."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read(2048)
        if content.startswith("---"):
            parts = content.split("---", 2)
            if len(parts) >= 3:
                fm = {}
                for line in parts[2].split("\n")[:30]:
                    if ":" in line:
                        key, _, value = line.partition(":")
                        fm[key.strip()] = value.strip()
                return fm
    except Exception:
        pass
    return {}


def is_pattern_topic_file(f: Path) -> bool:
    """Check if file is a pattern topic file (not index or meta)."""
    # Skip index and meta files
    skip_names = {"PATTERN_INDEX.md", "README.md"}
    if f.name in skip_names:
        return False
    # Check frontmatter type
    fm = parse_pattern_frontmatter(f)
    fm_type = fm.get("type", "")
    # Skip pattern_index type files
    if fm_type == "pattern_index":
        return False
    return True


def scan_patterns(patterns_dir: Path) -> dict:
    """Scan patterns directory and return JSON summary."""
    result = {
        "patterns_dir": str(patterns_dir),
        "exists": patterns_dir.exists(),
        "pattern_count": 0,
        "patterns": [],
        "would_write_index_path": str(patterns_dir / "PATTERN_INDEX.md"),
        "warnings": [],
    }

    if not patterns_dir.exists():
        result["warnings"].append(f"Patterns directory does not exist: {patterns_dir}")
        return result

    if not patterns_dir.is_dir():
        result["warnings"].append(f"Patterns path is not a directory: {patterns_dir}")
        return result

    all_md_files = [f for f in patterns_dir.iterdir() if f.is_file() and f.suffix == ".md"]
    pattern_files = sorted([f for f in all_md_files if is_pattern_topic_file(f)])
    result["pattern_count"] = len(pattern_files)

    for f in pattern_files:
        fm = parse_pattern_frontmatter(f)
        pattern_info = {
            "file": f.name,
            "pattern_key": fm.get("pattern_key", f.stem),
            "title": fm.get("title", f.stem),
            "status": fm.get("status", "unknown"),
            "type": fm.get("type", "unknown"),
            "severity": fm.get("severity", "unknown"),
        }
        result["patterns"].append(pattern_info)

    return result


def generate_index_content(patterns: list) -> str:
    """Generate PATTERN_INDEX.md content."""
    lines = [
        "# Pattern Index",
        "",
        f"**Total patterns**: {len(patterns)}",
        "",
        "## Patterns",
        "",
    ]

    if not patterns:
        lines.append("*No patterns found.*")
    else:
        for p in patterns:
            lines.append(f"### {p['pattern_key']}")
            lines.append(f"- **Title**: {p['title']}")
            lines.append(f"- **Status**: {p['status']}")
            lines.append(f"- **Type**: {p['type']}")
            lines.append(f"- **Severity**: {p['severity']}")
            lines.append(f"- **File**: `{p['file']}`")
            lines.append("")

    lines.extend([
        "---",
        "",
        "## Status Legend",
        "- `needs_evidence`: Single occurrence, not yet a pattern",
        "- `active`: Recurring, needs attention",
        "- `resolved`: Resolution in place",
        "- `stale`: Not seen recently",
        "- `superseded`: Replaced by newer pattern",
        "- `rejected`: False positive or low value",
        "",
        "## Warning",
        "This index is for reference only. It is NOT active rules.",
    ])

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Update pattern index")
    parser.add_argument("--patterns-dir", default=DEFAULT_PATTERNS_DIR, help="Patterns directory path")
    parser.add_argument("--write", action="store_true", help="Write PATTERN_INDEX.md")

    args = parser.parse_args()

    patterns_dir = Path(args.patterns_dir).expanduser().resolve()
    result = scan_patterns(patterns_dir)

    if args.write:
        index_path = patterns_dir / "PATTERN_INDEX.md"
        index_content = generate_index_content(result["patterns"])
        with open(index_path, "w", encoding="utf-8") as f:
            f.write(index_content)
        print(f"Written to {index_path}", file=sys.stderr)

    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
