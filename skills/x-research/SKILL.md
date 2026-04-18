---
name: x-research
description: 'Search X (Twitter) for what real people are saying. Trigger this skill whenever X or Twitter appears as a place the user wants to gather information FROM, not post TO. This includes questions about sentiment, recommendations, discussions, takes, threads, or opinions on X/Twitter about any subject. Common patterns: "on X", "on twitter", "heard on twitter", "threads on X", "practitioners on twitter recommend", "sentiment on X", checking what a specific @handle said. The subject is irrelevant -- AI, tools, databases, best practices, anything. If the user references X/Twitter as somewhere knowledge lives that they want extracted, this is the skill. Do NOT use for: composing tweets, Twitter API programming, scheduling social posts, or any task where Twitter is the destination rather than the source.'
---

# X Research

Search X/Twitter by topic using xAI Grok x_search. Produce a ranked table of practical insights from expert practitioners.

## Dependencies

- Python 3 with `httpx` library
- `XAI_API_KEY` environment variable (get from https://console.x.ai)
- `writing-clearly-and-concisely` skill (for final output)

## Workflow

### Step 1: Sharpen the question

Read `references/research-sharpener.md` and follow its process. If the question already points to specific results, skip clarification. If broad or ambiguous, ask until clear.

When the user mentions a specific X handle (e.g. @simonwillison), note it for the handle filter in Step 2.

After clarification (or if skipped), generate 3-5 search queries that approach the topic from different angles. Vary synonyms, framing, and specificity. For example, if the user asks "best MCP servers for Claude Code":
- "best MCP servers Claude Code recommendations"
- "Claude Code MCP server setup practical"
- "MCP tools AI coding workflow"
- "Claude Code extensions plugins MCP"
- "which MCP servers are worth using Claude"

### Step 2: Spawn sub-agents (one per search angle)

Create the output directory first:
```bash
rm -rf /tmp/x-research && mkdir -p /tmp/x-research
```

For each search query, spawn a sub-agent using the Agent tool. Run sub-agents in parallel.

Each sub-agent receives:
- One search query
- The user's original research question (for context)
- Date range: `--from-date` (default: 6 months ago) and `--to-date` (default: today). If the user specified a time range, convert it to dates.
- Handle filters if the user mentioned specific people: `--handles` or `--exclude-handles`
- The full content of `references/extraction-prompt.md`

Read `references/extraction-prompt.md` and include its full content in each sub-agent's prompt.

### Step 3: Synthesise results

After all sub-agents complete, read `references/synthesis-prompt.md` for the synthesis instructions.

1. Read all sub-agent output files from `/tmp/x-research/`
2. Combine, deduplicate, and rank insights
3. Use the writing-clearly-and-concisely skill to ensure the final output follows Strunk's rules
4. Format as the output table below

### Output format

```
## [Research question] -- X search, [from_date] to [to_date]

| # | Insight | Source |
|---|---------|--------|
| 1 | Specific finding with tools and names. [Tool](url) if available. | [Post](x.com/i/status/...) |
| 2 | Something an expert recommended because [reason]. | [Post](x.com/i/status/...) |

### Sources
| # | Post | Author |
|---|------|--------|
| 1 | [Post excerpt](x.com URL) | @handle |
```

### Output rules

- Every insight must trace back to a citation from Grok's response
- Specific over general: "use Cursor with Claude Opus" not "AI tools help"
- Include the why when the author gave one
- Name tools, numbers, frameworks -- things you would not get from a general AI
- Source column: clickable link to the X post
- If authors contradict each other, note it
- No executive summary. No themed groupings. No filler.
- UK English. No em dashes. Short sentences. Plain language. 4th-grade reading level.

## Edge cases

- **No results for a query angle**: sub-agent reports empty insights, orchestrator skips it
- **API key missing**: xai_search.py exits with clear error pointing to XAI_API_KEY
- **Rate limiting**: 60 RPM at tier 1. With 5 parallel sub-agents, well within limits.
- **Handle mentioned**: query strategist detects handles and passes them as --handles filter

### Step 4: Save research output

After presenting the synthesised table to the user, read `references/research-output-saver.md` and follow its process to save the output to `docs/research/`.

## Reference files

- **`references/extraction-prompt.md`** -- prompt template for sub-agents. Read and include in each sub-agent's prompt.
- **`references/synthesis-prompt.md`** -- instructions for the orchestrator synthesis step.
- **`references/research-sharpener.md`** -- clarification process for broad search queries.
- **`references/research-output-saver.md`** -- process for saving research output to docs/research/.
