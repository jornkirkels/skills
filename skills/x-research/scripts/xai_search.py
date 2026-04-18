#!/usr/bin/env python3
"""
Search X/Twitter via the xAI Responses API using Grok's x_search tool.

Usage:
  python3 xai_search.py --query "AI agents"
  python3 xai_search.py --query "Claude Code" --from-date 2026-01-01 --to-date 2026-03-23
  python3 xai_search.py --query "LLM tooling" --handles anthropic,openai --output results.json

Requires XAI_API_KEY environment variable. Get one at https://console.x.ai
Output: JSON with query, from_date, to_date, response_text, citations, usage.
"""

import argparse
import json
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path

import httpx

API_URL = "https://api.x.ai/v1/responses"
MODEL = "grok-4-1-fast-non-reasoning"


def build_prompt(query: str) -> str:
    """Build the search prompt from the query text."""
    parts = [f"Search X for: {query}"]
    parts.append("Return the most relevant posts with full text and links.")
    return "\n".join(parts)


def build_tool_config(from_date: str, to_date: str,
                      handles: list[str] | None,
                      exclude_handles: list[str] | None) -> dict:
    """Build the x_search tool definition with server-side filters."""
    config = {
        "type": "x_search",
        "x_search": {
            "from_date": from_date,
            "to_date": to_date,
        },
    }
    if handles:
        config["x_search"]["allowed_x_handles"] = [h.lstrip("@") for h in handles]
    if exclude_handles:
        config["x_search"]["excluded_x_handles"] = [h.lstrip("@") for h in exclude_handles]
    return config


def parse_response(data: dict) -> tuple[str, list[str], dict]:
    """Extract text, deduplicated citation URLs, and usage from the API response."""
    text_parts = []
    urls = set()

    for item in data.get("output", []):
        if item.get("type") != "message":
            continue
        for block in item.get("content", []):
            if block.get("type") != "output_text":
                continue
            text_parts.append(block.get("text", ""))
            for annotation in block.get("annotations", []):
                if annotation.get("type") == "url_citation":
                    url = annotation.get("url")
                    if url:
                        urls.add(url)

    response_text = "\n".join(text_parts)
    citations = sorted(urls)
    usage = data.get("usage", {})
    return response_text, citations, usage


def search(query: str, from_date: str, to_date: str,
           handles: list[str] | None, exclude_handles: list[str] | None,
           api_key: str) -> dict:
    """Call the xAI Responses API with x_search tool."""
    prompt = build_prompt(query)
    tool_config = build_tool_config(from_date, to_date, handles, exclude_handles)
    print(f"Searching X: {query}", file=sys.stderr)

    payload = {
        "model": MODEL,
        "tools": [tool_config],
        "input": prompt,
    }

    try:
        with httpx.Client(timeout=60) as client:
            resp = client.post(
                API_URL,
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json",
                },
                json=payload,
            )
            resp.raise_for_status()
            data = resp.json()
    except httpx.HTTPStatusError as e:
        code = e.response.status_code
        if code == 401:
            msg = "Authentication failed. Check your XAI_API_KEY."
        elif code == 429:
            msg = "Rate limit exceeded. Wait a moment and try again."
        elif code >= 500:
            msg = "xAI API is currently unavailable. Try again later."
        else:
            msg = f"API request failed: {e.response.text}"
        print(f"Error {code}: {msg}", file=sys.stderr)
        sys.exit(1)

    response_text, citations, usage = parse_response(data)
    print(f"Done. {len(citations)} citations found.", file=sys.stderr)

    return {
        "query": query,
        "from_date": from_date,
        "to_date": to_date,
        "response_text": response_text,
        "citations": citations,
        "usage": usage,
    }


def main():
    today = datetime.now().strftime("%Y-%m-%d")
    six_months_ago = (datetime.now() - timedelta(days=180)).strftime("%Y-%m-%d")

    parser = argparse.ArgumentParser(description="Search X/Twitter via xAI Responses API")
    parser.add_argument("--query", "-q", required=True,
                        help="Search terms")
    parser.add_argument("--from-date", default=six_months_ago,
                        help=f"Start date YYYY-MM-DD (default: {six_months_ago})")
    parser.add_argument("--to-date", default=today,
                        help=f"End date YYYY-MM-DD (default: {today})")
    parser.add_argument("--handles",
                        help="Comma-separated list of handles to include (max 10)")
    parser.add_argument("--exclude-handles",
                        help="Comma-separated list of handles to exclude")
    parser.add_argument("--output", "-o",
                        help="Output JSON file path (default: stdout)")
    args = parser.parse_args()

    api_key = os.environ.get("XAI_API_KEY")
    if not api_key:
        print("Error: XAI_API_KEY environment variable not set.", file=sys.stderr)
        print("Get an API key at https://console.x.ai", file=sys.stderr)
        sys.exit(1)

    handles = [h.strip() for h in args.handles.split(",")] if args.handles else None
    exclude_handles = [h.strip() for h in args.exclude_handles.split(",")] if args.exclude_handles else None

    if handles and len(handles) > 10:
        print("Error: --handles accepts a maximum of 10 handles.", file=sys.stderr)
        sys.exit(1)

    if exclude_handles and len(exclude_handles) > 10:
        print("Error: --exclude-handles accepts a maximum of 10 handles.", file=sys.stderr)
        sys.exit(1)

    result = search(
        query=args.query,
        from_date=args.from_date,
        to_date=args.to_date,
        handles=handles,
        exclude_handles=exclude_handles,
        api_key=api_key,
    )

    output = json.dumps(result, indent=2, ensure_ascii=False)

    if args.output:
        path = Path(args.output)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(output)
        print(f"Saved to {args.output}", file=sys.stderr)
    else:
        print(output)


if __name__ == "__main__":
    main()
