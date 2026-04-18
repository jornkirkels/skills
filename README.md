# skills

A small collection of agent skills for Claude Code and compatible agents.

## Skills

### x-research

Search X (Twitter) by topic using xAI Grok's `x_search` tool. Spawns parallel sub-agents across different search angles and returns a ranked table of practical insights with clickable post links.

Requires:
- Python 3 with the `httpx` library
- `XAI_API_KEY` environment variable (get one at https://console.x.ai)

### youtube-research

Turn a YouTube channel URL, search query, or video URL into a ranked table of practical insights with clickable video timestamps. Runs transcription on each video in parallel and extracts specifics only.

Requires:
- `yt-dlp` (via Homebrew or pip)
- A video transcription MCP tool (e.g. `mcp__video-transcriber__transcribe_video`)

### brainstorm

Reach shared understanding with the user through a structured interview. Resolves every decision in order, then returns a confirmed summary. Useful as a building block called by other skills when intent is unclear.

## Install

Install individually via the skills CLI:

```
npx skills add x-research
npx skills add youtube-research
npx skills add brainstorm
```

Or clone this repo into your `.claude/skills/` folder.

## Companion skill

The research skills call `writing-clearly-and-concisely` for final output formatting. Install it separately if you want the full behaviour:

```
npx skills add writing-clearly-and-concisely
```

## License

MIT
