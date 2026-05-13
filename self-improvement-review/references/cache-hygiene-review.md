# Cache Hygiene Review Checklist

## Review Items

1. Default loaded files are short and stable (MEMORY.md <100 lines, ideal <50 lines)
2. No dynamic dates, session state, or queue status leaking into default context
3. MEMORY.md exceeds 100 lines, 150 lines is warning threshold
4. `records/` being read by regular tasks
5. Long workflows that should be skill-ified
6. Frequently changing prompt prefixes

## Risk Level Definition

| Level | Condition |
|-------|-----------|
| low | No obvious bloat risk |
| medium | 1-2 items at risk |
| high | 3+ items at risk or MEMORY.md >150 lines |
