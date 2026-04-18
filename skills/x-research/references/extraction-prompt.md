# X Post Extraction Prompt

This prompt is included in each sub-agent's context. The sub-agent processes the results of one x_search query.

## Your task

Extract practical insights from a Grok x_search response about X/Twitter posts.

## Inputs you have been given

- **Research question**: what the user wants to learn
- **Search query**: the specific angle used for this search
- **Search results**: Grok's synthesised response text and citation URLs

## Steps

1. Call the xai_search.py script with your assigned query and date range:
   ```bash
   python3 .claude/skills/x-research/scripts/xai_search.py --query "<YOUR_QUERY>" --from-date "<FROM>" --to-date "<TO>" --output /tmp/x-research/query_<N>.json
   ```
   If handle filters were provided, add `--handles` or `--exclude-handles` flags.

2. Read the output JSON file. It contains `response_text` (Grok's synthesis) and `citations` (list of X post URLs).

3. Parse the response text and extract individual insights. Each insight should:
   - State one specific, practical finding
   - Name tools, products, numbers, or techniques mentioned
   - Include the reason if the author gave one
   - Map to the closest citation URL from the citations list

4. Skip anything generic. The test: could you get this information by asking a general AI without reading X posts? If yes, skip it. Keep only what is specific to real practitioners sharing experience.

5. Save your output to `/tmp/x-research/query_<N>.json` (overwriting the raw search output) with this structure:

## Output format

```json
{
  "query": "the search query used",
  "insights": [
    {
      "insight": "One plain sentence. Name tools, numbers, specifics. Include the why if given.",
      "source_url": "https://x.com/i/status/...",
      "author": "@handle (if identifiable from the response)"
    }
  ]
}
```

## Rules for writing insights

- One sentence per insight. Two sentences maximum if you need the "why".
- Name the specific thing: "Cursor" not "an AI coding tool". "37% faster" not "much faster".
- Include the author's reason when they gave one: "X works because Y" or "stopped using X because Y".
- Do not paraphrase into generic advice. Keep the author's specificity.
- Do not add your own opinion or analysis.
- If the author handle is visible in the response text or citation URL, include it.
