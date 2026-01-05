# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Local-first toolset for publishing private podcasts using static RSS feeds and object storage (e.g., Cloudflare R2). Privacy is achieved via unguessable URLs, not authentication.

## Requirements

- Python 3.10+
- S3-compatible object storage (Cloudflare R2 recommended)

## Architecture

```
Local machine
├── input/
│   └── metadata.yaml
├── generate_feed.py
└── output/
    ├── feed.xml
    └── audio/
```

The `input/` and `output/` directories are local-only (gitignored). GitHub stores tooling only—no audio files, real metadata, generated feeds, or credentials.

## Commands

```bash
# Setup local directories
mkdir -p input output/audio

# Copy sample metadata
cp examples/metadata.sample.yaml input/metadata.yaml

# Generate RSS feed
python generate_feed.py

# Upload to storage (after manual verification of output/feed.xml)
./publish.sh
```

## Components

- `generate_feed.py` - RSS 2.0 feed generator from YAML metadata
- `publish.sh` - Upload script for S3-compatible storage
- `schema.yaml` - Metadata schema definition
- `examples/metadata.sample.yaml` - Sample metadata file

## Design Constraints

- **Static-only**: RSS and audio files are static artifacts
- **Manual publishing**: No CI/CD pipelines; explicit user commands only
- **Local-first**: All authoring and publishing from author's machine
- **No secrets in repo**: Storage credentials never committed
- **Deterministic feeds**: Same metadata produces same RSS output
