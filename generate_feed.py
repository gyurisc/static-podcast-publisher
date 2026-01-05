#!/usr/bin/env python3
"""Generate RSS 2.0 podcast feed from YAML metadata."""

import sys
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from email.utils import format_datetime
from pathlib import Path

import yaml

INPUT_PATH = Path("input/metadata.yaml")
OUTPUT_PATH = Path("output/feed.xml")


def to_rfc822(iso_date, episode_id):
    """Convert ISO-8601 date string to RFC-822 format."""
    try:
        dt = datetime.fromisoformat(iso_date.replace("Z", "+00:00"))
    except ValueError:
        sys.exit(f"Error: Episode '{episode_id}' has invalid date: {iso_date}")
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return format_datetime(dt, usegmt=True)


def build_feed(metadata):
    """Build RSS XML from metadata."""
    # Validate structure
    podcast = metadata.get("podcast")
    if not isinstance(podcast, dict):
        sys.exit("Error: 'podcast' must be a mapping")

    episodes = metadata.get("episodes", [])
    if not isinstance(episodes, list):
        sys.exit("Error: 'episodes' must be a list")

    # Helper to get required podcast field
    def req(field):
        val = podcast.get(field)
        if not val:
            sys.exit(f"Error: Missing podcast.{field}")
        return val

    base_url = req("base_url").rstrip("/")

    # Build RSS structure
    rss = ET.Element("rss", {"version": "2.0"})
    channel = ET.SubElement(rss, "channel")

    ET.SubElement(channel, "title").text = req("title")
    ET.SubElement(channel, "link").text = base_url
    ET.SubElement(channel, "description").text = req("description")
    ET.SubElement(channel, "language").text = req("language")
    ET.SubElement(channel, "lastBuildDate").text = format_datetime(
        datetime.now(timezone.utc), usegmt=True
    )
    ET.SubElement(channel, "generator").text = "static-podcast-publisher"

    # Sort episodes by pub_date descending (newest first)
    sorted_episodes = sorted(
        episodes,
        key=lambda e: e.get("pub_date", ""),
        reverse=True,
    )

    # Add episodes
    for ep in sorted_episodes:
        # Helper to get required episode field
        ep_id = ep.get("id", "?")

        def ep_req(field):
            val = ep.get(field)
            if not val:
                sys.exit(f"Error: Episode '{ep_id}' missing field: {field}")
            return val

        ep_id = ep_req("id")  # Re-validate id exists
        ep_title = ep_req("title")
        ep_desc = ep_req("description")
        ep_file = ep_req("file")
        ep_date = ep_req("pub_date")

        item = ET.SubElement(channel, "item")
        ET.SubElement(item, "title").text = ep_title
        ET.SubElement(item, "description").text = ep_desc
        ET.SubElement(item, "pubDate").text = to_rfc822(ep_date, ep_id)

        guid = ET.SubElement(item, "guid")
        guid.text = ep_id
        guid.set("isPermaLink", "false")

        ET.SubElement(
            item,
            "enclosure",
            {
                "url": f"{base_url}/audio/{ep_file}",
                "type": "audio/mpeg",
                "length": "0",
            },
        )

    return rss


def main():
    # Load metadata
    if not INPUT_PATH.exists():
        sys.exit(f"Error: {INPUT_PATH} not found")

    try:
        metadata = yaml.safe_load(INPUT_PATH.read_text(encoding="utf-8"))
    except yaml.YAMLError as e:
        sys.exit(f"Error: Invalid YAML: {e}")

    # Build feed
    rss = build_feed(metadata)

    # Write output
    try:
        OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    except OSError as e:
        sys.exit(f"Error: Cannot create output directory: {e}")

    ET.indent(rss, space="  ")
    try:
        ET.ElementTree(rss).write(OUTPUT_PATH, encoding="utf-8", xml_declaration=True)
    except OSError as e:
        sys.exit(f"Error: Cannot write {OUTPUT_PATH}: {e}")

    print(f"Feed generated: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
