# Video Extraction Prompt

This prompt is included in each sub-agent's context. The sub-agent processes one video.

## Your task

Extract practical insights from a single YouTube video transcript.

## Inputs you have been given

- **Research question**: what the user wants to learn
- **Video title, date, URL**
- **Video description**: contains links to tools, resources, and references mentioned in the video

## Steps

1. Call `mcp__video-transcriber__transcribe_video(url: "<VIDEO_URL>")` to transcribe the video
2. Read the resulting JSON transcript file from `~/Downloads/video-transcripts/`. Find it by the video ID in the filename. The JSON contains a `segments` array where each segment has `start` (seconds), `end` (seconds), and `text` fields.
3. Parse all URLs from the video description. Build a lookup of resource name to URL.
4. Read through the transcript and identify segments that contain:
   - Specific tools, products, or software named
   - Step-by-step techniques or workflows
   - Personal experience: "I tried X", "what worked for me", "I stopped using Y because"
   - Numbers, benchmarks, comparisons, prices
   - Recommendations or warnings
   - Frameworks or mental models
5. For each finding, check if any tool or resource mentioned has a matching URL in the video description
6. If a specific tool, product, or resource is mentioned but has no link in the description, use `mcp__exa__web_search_exa` to find the official URL. Only do this for named tools and products that the user would want to click through to -- not for generic concepts or well-known companies.
7. Skip anything generic. The test: could you get this information by asking a general AI without watching the video? If yes, skip it. Keep only what is specific to the creator's experience, testing, or opinion.

## Output format

Save a JSON file to `/tmp/yt-research/VIDEO_ID.json` with this structure:

```json
{
  "video_id": "abc123",
  "video_title": "Title Here",
  "video_date": "3 Mar 2026",
  "video_url": "https://www.youtube.com/watch?v=abc123",
  "insights": [
    {
      "insight": "One plain sentence. Name tools, numbers, specifics. Include the why if the creator gave one.",
      "timestamp_seconds": 662,
      "timestamp_display": "11:02",
      "links": [
        {"text": "Tool Name", "url": "https://tool-url.com"}
      ]
    }
  ]
}
```

## Rules for writing insights

- One sentence per insight. Two sentences maximum if you need the "why".
- Name the specific thing: "Cursor" not "an AI coding tool". "37% faster" not "much faster".
- Include the creator's reason when they gave one: "X works because Y" or "stopped using X because Y".
- Do not paraphrase into generic advice. Keep the creator's specificity.
- Do not add your own opinion or analysis.
- Every insight must map to a specific segment in the transcript. Use the `start` timestamp of that segment.

## Timestamp rules

- Use the `start` field from the transcript segment (in seconds)
- Convert to MM:SS for display (e.g. 662 seconds = "11:02")
- If an insight spans multiple segments, use the start of the first relevant segment
