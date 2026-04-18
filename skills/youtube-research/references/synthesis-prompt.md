# Synthesis Prompt

Instructions for the orchestrator after all sub-agents complete.

## Your task

Combine insights from all sub-agents into a single ranked table.

## Steps

1. Read all JSON files from `/tmp/yt-research/`
2. Collect every insight across all videos into one list
3. Remove duplicates: if the same insight appears in multiple videos, keep the version with the clearest explanation and best timestamp
4. Rank every insight by scoring on three criteria:
   - **Relevance** (0-3): how directly does this answer the user's research question? 3 = directly answers it. 0 = tangentially related.
   - **Specificity** (0-3): does it name tools, numbers, steps? 3 = very specific with names and numbers. 0 = vague generality.
   - **Uniqueness** (0-3): would you only learn this from watching this video? 3 = creator's personal experience or testing. 0 = common knowledge.
   - Total score = relevance + specificity + uniqueness. Sort descending.
5. Format as the output table

## Output format

```
## [Research question] -- [X] videos analysed from [Channel Name](channel URL)

| # | Insight | Watch |
|---|---------|-------|
| 1 | Insight text. [Tool](url) if link available. | [MM:SS](youtube URL&t=Ns) |
| 2 | Next insight. | [MM:SS](youtube URL&t=Ns) |

### Videos analysed

| Video | Date | Duration |
|---|---|---|
| [Title](youtube URL) | D Mon YYYY | MM:SS |
```

## Formatting rules

- Insight column: plain text. Embed links inline when a tool/resource has a URL from the video description. Use markdown link format: [Tool Name](url).
- Watch column: show only the timestamp as a clickable link. Format: `[MM:SS](https://youtube.com/watch?v=ID&t=Ns)` where N is the timestamp in seconds.
- Video titles in the source index: clickable links to the full video.
- Dates: D Mon YYYY format (e.g. 3 Mar 2026).
- Number the insights starting from 1.

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
- The table IS the output. Nothing before it except the heading. Nothing after it except the source index.
