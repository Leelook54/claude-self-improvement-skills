---
name: self-improvement-review
description: Analyze local self-improvement memory records, user corrections, tool errors, review reports, and compact reports to identify repeated friction patterns, proposed rule/config updates, and skill extraction candidates. Use when the user asks to review agent behavior, find recurring mistakes, improve workflows, extract reusable skills, or prepare self-improvement recommendations.
---

# Self Improvement Review

## Purpose

- Review low-frequency self-improvement evidence records
- Detect repeated friction patterns
- Identify recurring user corrections and tool-error patterns
- Produce promotion candidates without applying them
- Produce skill extraction candidates for reusable multi-step workflows
- Check cache hygiene and default-context bloat risk
- Keep global CLAUDE.md and Claude Code auto memory unchanged unless the user explicitly approves a separate apply step

## Safety Rules

- Do not write to global `~/.claude/CLAUDE.md`
- Do not write to project `CLAUDE.md`
- Do not modify Claude Code official auto memory
- Do not modify `/Users/qunqing/.claude/memory/MEMORY.md`
- Do not treat `records/` as active rules
- Do not promote one-off corrections
- Do not convert dynamic session state into default-loaded context
- Do not apply recommendations automatically

## Workflow

1. Identify target records under `/Users/qunqing/.claude/memory/records/`
2. Collect corrections, errors, reviews, compact reports, promotions, skill-candidates, and rejected records
3. Classify recurring patterns
4. Cross-check whether a recommendation already exists in `records/promotions/` or `records/skill-candidates/`
5. Generate a review report under `records/reviews/`
6. Generate promotion candidate files only when evidence is repeated and stable
7. Generate skill candidate files only for reusable multi-step workflows
8. Output verification summary

## References

- Read `references/review-taxonomy.md` when classifying evidence
- Read `references/promotion-policy.md` before proposing CLAUDE.md or config changes
- Read `references/skill-extraction-policy.md` before proposing a new skill
- Read `references/cache-hygiene-review.md` when reviewing default context and cache hit friendliness
- Read `references/report-template.md` when writing review reports
- Read `references/record-schema.md` for unified frontmatter and state machine
- Read `references/pattern-lifecycle.md` for friction pattern detection and lifecycle
- Read `references/do-not-remember-policy.md` before writing to long-term memory
- Read `references/session-review-policy.md` for session transcript evidence extraction
