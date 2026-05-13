# Cache Hygiene

## Default Load Stability

Default loaded files should be short and stable.

## Checks

- No dates, temporary status, queue state, or session-specific notes in default-loaded prefixes
- MEMORY.md should preferably stay under 100 lines
- Warning above 150 lines
- Long procedures should become skills
- records/ should not be injected into normal prompts
- Dynamic content should be loaded only on explicit review/compact tasks

## Warning Thresholds

| Metric | Acceptable | Warning | Critical |
|--------|-----------|---------|----------|
| MEMORY.md lines | <100 | 100-150 | >150 |
| Topic file size | <20KB | 20-50KB | >50KB |
| records/ in default load | 0 | - | >0 |
