#!/usr/bin/env python3
"""PreToolUse hook: protect CLAUDE.md and settings.json from accidental writes."""

import json
import os
import sys


def get_paths_from_input(tool_name, tool_input):
    """Extract all file paths from tool_input based on tool_name."""
    paths = []

    if tool_name in ("Edit", "Write"):
        # Single path fields
        for field in ("file_path", "path", "notebook_path"):
            if field in tool_input and tool_input[field]:
                paths.append(tool_input[field])
    elif tool_name == "MultiEdit":
        # edits array
        edits = tool_input.get("edits", [])
        for edit in edits:
            for field in ("file_path", "path"):
                if field in edit and edit[field]:
                    paths.append(edit[field])

    return paths


def is_protected_path(path, plugin_root):
    """Check if a path is protected."""
    if not path:
        return False

    # Resolve to absolute for consistent comparison
    abs_path = os.path.abspath(os.path.expanduser(path))
    abs_plugin_root = os.path.abspath(plugin_root) if plugin_root else None

    # Protected exact paths
    protected_exact = (
        os.path.abspath(os.path.expanduser("~/.claude/CLAUDE.md")),
        os.path.abspath(os.path.expanduser("~/.claude/settings.json")),
        os.path.abspath(os.path.expanduser("~/.claude/settings.local.json")),
    )

    if abs_path in protected_exact:
        return True

    # Any basename CLAUDE.md is protected (any project CLAUDE.md)
    if os.path.basename(abs_path) == "CLAUDE.md":
        return True

    # Any path ending with /.claude/settings.json
    if abs_path.endswith("/.claude/settings.json"):
        return True

    # Any path ending with /.claude/settings.local.json
    if abs_path.endswith("/.claude/settings.local.json"):
        return True

    # Allow: plugin/skills/**/SKILL.md — these are distributed skill copies
    if abs_plugin_root and abs_path.startswith(abs_plugin_root + "/skills/"):
        if abs_path.endswith("/SKILL.md") or abs_path.endswith("\\SKILL.md"):
            return False  # explicitly not protected

    return False


def is_allowed_path(path, plugin_root):
    """Check if a path is explicitly allowed."""
    if not path:
        return True  # no path = no file write = allow

    abs_path = os.path.abspath(os.path.expanduser(path))
    basename = os.path.basename(abs_path)

    # Explicitly allowed basenames
    if basename in ("README.md", "SKILL.md"):
        return True

    # Allowed subdirectories
    if "/references/" in abs_path.replace("\\", "/") and abs_path.endswith(".md"):
        return True

    if "/scripts/" in abs_path.replace("\\", "/") and abs_path.endswith(".py"):
        return True

    # Allowed: plugin/** 普通文档 (non-protected files in plugin dir)
    abs_plugin_root = os.path.abspath(plugin_root) if plugin_root else None
    if abs_plugin_root and abs_path.startswith(abs_plugin_root):
        # plugin dir files that aren't SKILL.md in skills are allowed
        # (but we already returned False for SKILL.md above via is_protected)
        return True

    return False


def main():
    plugin_root = os.environ.get("CLAUDE_PLUGIN_ROOT", "")

    # Read stdin JSON
    try:
        stdin_data = sys.stdin.read()
        if not stdin_data:
            # Empty stdin, allow
            sys.exit(0)

        payload = json.loads(stdin_data)
    except json.JSONDecodeError as e:
        # Bad JSON: short stderr, exit 0 (don't block normal flow)
        sys.stderr.write(f"JSON parse error: {e}")
        sys.exit(0)

    # Extract tool info
    tool_name = payload.get("tool_name", "")
    tool_input = payload.get("tool_input", {})

    # Only intercept Edit/Write/MultiEdit
    if tool_name not in ("Edit", "Write", "MultiEdit"):
        sys.exit(0)

    # Get all paths from tool_input
    paths = get_paths_from_input(tool_name, tool_input)

    # Check each path
    for p in paths:
        if is_protected_path(p, plugin_root):
            deny()
            return  # already output and exited

        if not is_allowed_path(p, plugin_root):
            # Not protected and not explicitly allowed
            # For paths that don't match any rule, allow by default
            # (this preserves normal file editing)
            pass

    # All paths passed checks
    sys.exit(0)


def deny():
    """Output deny JSON and exit."""
    output = {
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": "Protected memory/config file write requires explicit maintenance flow."
        }
    }
    print(json.dumps(output))
    sys.exit(0)


if __name__ == "__main__":
    main()
