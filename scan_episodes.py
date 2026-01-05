#!/usr/bin/env python3
"""Scan audio files and generate metadata.yaml stub."""

import sys
from pathlib import Path
from datetime import datetime, timezone

AUDIO_DIR = Path("input/audio")
OUTPUT_PATH = Path("input/metadata.yaml")


def main():
    if not AUDIO_DIR.exists():
        sys.exit(f"Error: {AUDIO_DIR} not found. Create it and add your mp3 files.")

    mp3_files = sorted(AUDIO_DIR.glob("*.mp3"))
    if not mp3_files:
        sys.exit(f"Error: No .mp3 files found in {AUDIO_DIR}")

    if OUTPUT_PATH.exists() and "--force" not in sys.argv:
        sys.exit(f"Error: {OUTPUT_PATH} already exists. Use --force to overwrite.")

    # Generate YAML content
    today = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    lines = [
        'podcast:',
        '  title: "TODO: Your Podcast Title"',
        '  description: "TODO: Your podcast description"',
        '  language: "en-us"',
        '  base_url: "TODO: https://your-bucket.example.com/podcast-folder"',
        '',
        'episodes:',
    ]

    for mp3 in mp3_files:
        ep_id = mp3.stem  # filename without extension
        lines.extend([
            f'  - id: "{ep_id}"',
            f'    title: "TODO: {ep_id}"',
            f'    file: "{mp3.name}"',
            '    description: "TODO: Add description"',
            f'    pub_date: "{today}"  # TODO: Set actual date',
            '',
        ])

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text("\n".join(lines), encoding="utf-8")

    print(f"Found {len(mp3_files)} audio files")
    print(f"Generated: {OUTPUT_PATH}")
    print("Edit the file to fill in TODO fields, then run: python generate_feed.py")


if __name__ == "__main__":
    main()
