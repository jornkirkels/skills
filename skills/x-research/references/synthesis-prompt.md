# Synthesis Prompt

Instructions for the orchestrator after all sub-agents complete.

## Your task

Combine insights from all sub-agents into a single ranked table.

## Steps

1. Read all JSON files from `/tmp/x-research/`
2. Collect every insight across all query results into one list
3. Remove duplicates: if the same insight appears from multiple query angles (same source URL or same core claim), keep the version with the clearest explanation
4. Rank every insight by scoring on three criteria:
   - **Relevance** (0-3): how directly does this answer the user's research question? 3 = directly answers it. 0 = tangentially related.
   - **Specificity** (0-3): does it name tools, numbers, steps? 3 = very specific with names and numbers. 0 = vague generality.
   - **Uniqueness** (0-3): would you only learn this from reading X posts? 3 = practitioner's personal experience or testing. 0 = common knowledge.
   - Total score = relevance + specificity + uniqueness. Sort descending.
5. Format as the output table

## Output format

```
## [Research question] -- X search, [from_date] to [to_date]

| # | Insight | Source |
|---|---------|--------|
| 1 | Insight text. [Tool](url) if link available. | [Post](x.com URL) |
| 2 | Next insight. | [Post](x.com URL) |

### Sources
| # | Post | Author |
|---|------|--------|
| 1 | [Post excerpt](x.com URL) | @handle |
```

## Formatting rules

- Insight column: plain text. Embed tool/resource links inline using markdown: [Tool Name](url).
- Source column: show "Post" as a clickable link to the X post URL.
- Number the insights starting from 1.
- Sources table: list every unique X post referenced, with author handle if known.

## Writing rules

Use the writing-clearly-and-concisely skill to ensure:
- Active voice
- Definite, specific, concrete language
- No needless words
- No AI writing patterns: no "leveraging", "delving", "robust", "crucial", "comprehensive", "streamline"
- UK English throughout
- No em dashes (use "not", "but", or split into two sentences)
- Short sentences. 4th-grade reading level.
- No executive summary. No themed groupings. No filler sentences.
- The table IS the output. Nothing before it except the heading. Nothing after it except the sources index.
