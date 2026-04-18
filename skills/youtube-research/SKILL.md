---
name: youtube-research
description: "Use whenever YouTube content needs to be accessed, watched, analysed, or searched. You MUST invoke this skill if the user's message contains: a youtube.com or youtu.be URL, a YouTube channel handle (@handle), a YouTube creator's name, or a request to find/search YouTube videos. This is the ONLY skill with yt-dlp and video transcription capabilities. Without it, you cannot access YouTube video content at all. Covers: video analysis, channel research, and topic search across YouTube. Skip for: writing video scripts for YouTube, or research on non-YouTube platforms."
---

# YouTube Channel Research

Turn a YouTube channel URL and a research question into a ranked table of practical insights with clickable video timestamps.

## Dependencies

- `yt-dlp` (installed via Homebrew or pip)
- `mcp__video-transcriber__transcribe_video` MCP tool
- `writing-clearly-and-concisely` skill (for final output)

## Workflow

### Step 1: Extract video list

The script supports three input modes. Detect which one the user provided:

**Channel mode** -- user gives a youtube.com/@handle URL:
```bash
python3 .claude/skills/youtube-research/scripts/extract_channel_videos.py "<CHANNEL_URL>" --months <N> --output /tmp/yt-research-videos.json
```

**Search mode** -- user asks a question without a specific channel:

First, assess whether the question is specific enough to search directly. Read `references/research-sharpener.md` and follow its process. If the question is broad or ambiguous, ask a maximum of 2 clarifying questions with concrete multiple-choice options before proceeding. Skip clarification if the question is already specific.

After clarification (or if skipped), generate 3-5 different search queries that approach the topic from different angles. YouTube search is keyword-sensitive, so varying the phrasing finds different videos. For example, if the user asks "how to run multiple Claude Code agents", generate:
- "claude code multiple agents parallel"
- "claude code agent teams workflow"
- "run parallel AI coding agents claude"
- "claude code multi-agent setup tutorial"

Run each query separately:
```bash
python3 .claude/skills/youtube-research/scripts/extract_channel_videos.py --search "<QUERY_1>" --limit 10 --output /tmp/yt-research-q1.json
python3 .claude/skills/youtube-research/scripts/extract_channel_videos.py --search "<QUERY_2>" --limit 10 --output /tmp/yt-research-q2.json
```

Merge all results, deduplicate by video ID, and present the combined list to the user. This finds videos that a single query would miss.

**Single video mode** -- user gives a youtube.com/watch URL:
```bash
python3 .claude/skills/youtube-research/scripts/extract_channel_videos.py "<VIDEO_URL>" --output /tmp/yt-research-videos.json
```

Parameters:
- `--search "query"` -- search YouTube instead of scraping a channel
- `--months N` -- how far back to look in channel mode (default: 6)
- `--limit N` -- max videos: channel mode (0 = no limit), search mode (default 20)
- `--output PATH` -- save JSON to file

Each entry contains: `id`, `title`, `upload_date`, `url`, `duration`, `description`. Shorts (under 2 minutes) are excluded automatically.

Present the video list as a table with clickable titles. Format dates as D Mon YYYY (e.g. 3 Mar 2026).

| Video | Date | Duration |
|---|---|---|
| [Title](video URL) | 3 Mar 2026 | 12:04 |

Flag livestreams (over 2 hours). For channel and search modes, recommend 10-20 videos based on relevance to the research question. Let the user adjust. For single video mode, skip to Step 3.

### Step 2: Confirm video selection

Ask the user which videos to analyse. If they asked about a specific topic, filter by title keywords and recommend the most relevant subset.

### Step 3: Spawn sub-agents (one per video)

For each selected video, spawn a sub-agent using the Agent tool. Run sub-agents in parallel.

Each sub-agent receives:
- The user's research question
- Video title, date, URL
- The full video description (with links)
- The extraction prompt from `references/extraction-prompt.md`

Read `references/extraction-prompt.md` and include its full content in each sub-agent's prompt. The sub-agent must:
1. Call `mcp__video-transcriber__transcribe_video` to transcribe the video
2. Read the resulting JSON transcript file (contains `segments` with `start` timestamps)
3. Parse links from the video description
4. Extract practical insights with timestamps and matching links
5. Return structured JSON

Tell each sub-agent to save its output to `/tmp/yt-research/VIDEO_ID.json`.

### Step 4: Synthesise results

After all sub-agents complete, read `references/synthesis-prompt.md` for the synthesis instructions.

1. Read all sub-agent output files from `/tmp/yt-research/`
2. Combine, deduplicate, and rank insights
3. Use the writing-clearly-and-concisely skill to ensure the final output follows Strunk's rules: active voice, concrete language, no needless words, no AI writing patterns
4. Format as the output table below

### Output format

```
## [Research question] -- [X] videos analysed from [Channel Name](channel URL)

| # | Insight | Watch |
|---|---------|-------|
| 1 | Specific finding with tools and numbers named. | [4:23](youtube URL with &t=) |
| 2 | Something creator tried. Did not work because [reason]. | [11:02](youtube URL with &t=) |

### Videos analysed

| Video | Date | Duration |
|---|---|---|
| [Title](youtube URL) | 3 Mar 2026 | 12:04 |
```

### Output rules

- Every insight must trace back to something explicitly said in the transcript
- Specific over general: "use Cursor with Claude Opus" not "AI tools help"
- Include the why when the creator gave one
- Name tools, numbers, frameworks -- things you would not get from a general AI
- When a tool/resource has a link in the video description, embed it in the insight
- Watch column: timestamp clickable to the exact moment in the video
- Video titles in source index: clickable links to the full video
- If the creator contradicts themselves across videos, note it
- No executive summary. No themed groupings. No filler.
- UK English. No em dashes. Short sentences. Plain language. 4th-grade reading level.

### Step 5: Save research output

After presenting the synthesised table to the user, read `references/research-output-saver.md` and follow its process to save the output to `docs/research/`.

## Edge cases

- **Members-only videos**: yt-dlp skips these. Mention to user if many were skipped.
- **YouTube Shorts**: Under 60 seconds. Flag separately, ask if they should be included.
- **Large channels**: Over 180 videos in range. Suggest narrowing date range or title filtering.
- **Livestreams**: Over 2 hours. Flag and confirm before transcribing.

## Reference files

- **`references/extraction-prompt.md`** -- prompt template for sub-agents. Read and include in each sub-agent's prompt.
- **`references/synthesis-prompt.md`** -- instructions for the orchestrator synthesis step.
- **`references/research-sharpener.md`** -- clarification process for broad search queries. Used by search mode only.
- **`references/research-output-saver.md`** -- process for saving research output to docs/research/.
