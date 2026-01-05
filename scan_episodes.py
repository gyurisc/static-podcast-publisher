#!/usr/bin/env python3
"""Scan audio files and generate/update metadata.yaml."""

import sys
from pathlib import Path
from datetime import datetime, timezone

import yaml

AUDIO_DIR = Path("input/audio")
OUTPUT_PATH = Path("input/metadata.yaml")


def main():
    if not AUDIO_DIR.exists():
        sys.exit(f"Error: {AUDIO_DIR} not found. Create it and add your mp3 files.")

    mp3_files = sorted(AUDIO_DIR.glob("*.mp3"))
    if not mp3_files:
        sys.exit(f"Error: No .mp3 files found in {AUDIO_DIR}")

    today = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    # Load existing metadata or create new
    if OUTPUT_PATH.exists():
        metadata = yaml.safe_load(OUTPUT_PATH.read_text(encoding="utf-8")) or {}
        existing_files = {ep.get("file") for ep in metadata.get("episodes", [])}
    else:
        metadata = {
            "podcast": {
                "title": "TODO: Your Podcast Title",
                "description": "TODO: Your podcast description",
                "language": "en-us",
                "base_url": "TODO: https://your-bucket.example.com/podcast-folder",
            },
            "episodes": [],
        }
        existing_files = set()

    # Find new mp3 files
    new_files = [mp3 for mp3 in mp3_files if mp3.name not in existing_files]

    if not new_files:
        print(f"No new audio files found. All {len(mp3_files)} files already in metadata.")
        return

    # Append new episodes
    for mp3 in new_files:
        ep_id = mp3.stem
        metadata["episodes"].append({
            "id": ep_id,
            "title": f"TODO: {ep_id}",
            "file": mp3.name,
            "description": "TODO: Add description",
            "pub_date": today,
        })

    # Write updated metadata
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(
        yaml.dump(metadata, default_flow_style=False, allow_unicode=True, sort_keys=False),
        encoding="utf-8",
    )

    action = "Updated" if existing_files else "Generated"
    print(f"Found {len(new_files)} new audio files (of {len(mp3_files)} total)")
    print(f"{action}: {OUTPUT_PATH}")
    print("Edit the file to fill in TODO fields, then run: python generate_feed.py")


if __name__ == "__main__":
    main()
