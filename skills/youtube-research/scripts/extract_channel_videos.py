#!/usr/bin/env python3
"""
Extract video metadata from YouTube using yt-dlp.

Supports three modes:
  1. Channel:  python3 extract_channel_videos.py "https://www.youtube.com/@handle" --months 3
  2. Search:   python3 extract_channel_videos.py --search "best way to use claude code skills" --limit 20
  3. Video:    python3 extract_channel_videos.py "https://www.youtube.com/watch?v=abc123"

Output: JSON array of {id, title, upload_date, url, duration, description}.
Excludes Shorts (under 120 seconds) automatically.
"""

import argparse
import json
import re
import subprocess
import sys
from datetime import datetime, timedelta


def compute_dateafter(months: int) -> str:
    """Return YYYYMMDD string for N months ago."""
    cutoff = datetime.now() - timedelta(days=months * 30)
    return cutoff.strftime("%Y%m%d")


def format_date(yyyymmdd: str) -> str:
    """Convert 20260315 to 15 Mar 2026."""
    try:
        dt = datetime.strptime(yyyymmdd, "%Y%m%d")
        return dt.strftime("%-d %b %Y")
    except ValueError:
        return yyyymmdd


def is_short(duration: str) -> bool:
    """Return True if video is under 120 seconds (a Short)."""
    try:
        parts = duration.split(":")
        if len(parts) == 1:
            return int(parts[0]) < 120
        elif len(parts) == 2:
            return int(parts[0]) * 60 + int(parts[1]) < 120
        return False
    except ValueError:
        return False


def detect_mode(source: str, search: str) -> str:
    """Detect whether input is a channel, video, or search query."""
    if search:
        return "search"
    if re.match(r"https?://(www\.)?youtube\.com/watch\?v=", source):
        return "video"
    if re.match(r"https?://(www\.)?youtu\.be/", source):
        return "video"
    return "channel"


def extract_videos(source: str, mode: str, months: int = 6, limit: int = 0) -> list[dict]:
    """Extract video metadata from YouTube."""
    sep = "\x1f"
    print_fmt = f"%(id)s{sep}%(title)s{sep}%(upload_date)s{sep}%(duration_string)s{sep}%(description)s"

    if mode == "search":
        search_limit = limit if limit > 0 else 20
        cmd = [
            "yt-dlp",
            "--no-download",
            "--print", print_fmt,
            "--ignore-errors",
            f"ytsearch{search_limit}:{source}",
        ]
    elif mode == "video":
        cmd = [
            "yt-dlp",
            "--no-download",
            "--print", print_fmt,
            "--ignore-errors",
            source,
        ]
    else:
        cmd = [
            "yt-dlp",
            "--no-download",
            "--print", print_fmt,
            "--dateafter", compute_dateafter(months),
            "--ignore-errors",
            source,
        ]
        if limit > 0:
            cmd.extend(["--playlist-end", str(limit)])

    result = subprocess.run(cmd, capture_output=True, text=True)

    videos = []
    for line in result.stdout.strip().splitlines():
        parts = line.split(sep, 4)
        if len(parts) == 5:
            vid_id, title, date, duration, description = parts
            if is_short(duration):
                continue
            videos.append({
                "id": vid_id,
                "title": title,
                "upload_date": format_date(date),
                "upload_date_raw": date,
                "url": f"https://www.youtube.com/watch?v={vid_id}",
                "duration": duration,
                "description": description,
            })

    return videos


def main():
    parser = argparse.ArgumentParser(description="Extract YouTube video metadata")
    parser.add_argument("source", nargs="?", default="",
                        help="YouTube channel URL, video URL, or omit for --search mode")
    parser.add_argument("--search", "-s", default="",
                        help="Search YouTube for this query instead of scraping a channel")
    parser.add_argument("--months", type=int, default=6,
                        help="How many months back to look for channel mode (default: 6)")
    parser.add_argument("--limit", type=int, default=0,
                        help="Max videos: channel mode (0=no limit), search mode (default 20)")
    parser.add_argument("--output", "-o",
                        help="Output JSON file path (default: stdout)")
    args = parser.parse_args()

    source = args.search if args.search else args.source
    if not source:
        parser.error("Provide a URL or use --search 'query'")

    mode = detect_mode(args.source, args.search)
    print(f"Mode: {mode}", file=sys.stderr)

    videos = extract_videos(source, mode, months=args.months, limit=args.limit)

    output = json.dumps(videos, indent=2, ensure_ascii=False)

    if args.output:
        with open(args.output, "w") as f:
            f.write(output)
        print(f"Saved {len(videos)} videos to {args.output}", file=sys.stderr)
    else:
        print(output)

    print(f"Total: {len(videos)} videos found", file=sys.stderr)


if __name__ == "__main__":
    main()
