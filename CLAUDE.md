# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Local-first toolset for publishing private podcasts using static RSS feeds and object storage (e.g., Cloudflare R2). Privacy is achieved via unguessable URLs, not authentication.

## Architecture

```
Local machine (authoring + publishing)
  ├── episodes (mp3)
  ├── metadata.yaml
  └── RSS generator
          │
          ▼
Object storage (delivery)
  ├── feed.xml
  └── audio/*.mp3
```

GitHub stores tooling only. No audio files, real metadata, generated feeds, or credentials in this repo.

## Planned Components

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
