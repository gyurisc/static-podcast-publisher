# static-podcast-publisher

Local-first tools for publishing private podcasts using static RSS and object storage.

⚠️ **This repository does NOT host podcast content or audio files.  
It contains tooling only.**

---

## What this is

This project provides a small set of scripts and conventions to:

- Generate a **static podcast RSS feed**
- Publish audio files to **object storage** (e.g. Cloudflare R2)
- Keep publishing **manual, predictable, and private**

It is designed for:
- Private or semi-private podcasts
- No backend services
- No authentication layers
- No CI-based publishing
- No podcast hosting platforms

---

## What this is NOT

- ❌ A podcast hosting service
- ❌ A backend or API
- ❌ A GitHub Pages setup
- ❌ A place to store audio or feeds
- ❌ A “secure” or authenticated feed (podcast apps don’t support that)

Privacy is achieved via **unguessable URLs**, not authentication.

---

## Architecture (high level)

```

Local machine
├── input/
│   └── metadata.yaml
├── generate_feed.py
└── output/
├── feed.xml
└── audio/

```

Podcast apps only ever access files hosted on **object storage**.  
GitHub is used for **tooling only**, not delivery.

---

## Local directories

This project expects the following local directories, which are intentionally
excluded from version control:

- `input/`  
  Contains podcast metadata and local episode references.

- `output/`  
  Generated RSS feed and publish-ready audio structure.

Both directories are created and managed locally.

---

## Repository contents

```

.
├── generate_feed.py        # Generates a static RSS feed
├── publish.sh              # Optional helper to upload output to storage
├── schema.yaml             # Metadata schema (reference)
├── examples/
│   └── metadata.sample.yaml
├── README.md
└── LICENSE

````

This repository must **never** contain:
- Real podcast metadata
- Audio files
- Generated RSS feeds
- Credentials or secrets

---

## Requirements

- Python 3.10+
- Object storage that supports HTTP range requests  
  (Cloudflare R2 recommended, S3-compatible alternatives work)
- A podcast app that supports static RSS feeds

---

## Basic workflow

1. Create local directories:
   ```bash
   mkdir -p input output/audio
````

2. Add your metadata:

   ```bash
   cp examples/metadata.sample.yaml input/metadata.yaml
   ```

3. Generate the RSS feed:

   ```bash
   python generate_feed.py
   ```

4. Verify `output/feed.xml` locally.

5. Upload `output/` to object storage (manually or via `publish.sh`).

6. Subscribe to the feed using the storage URL.

Publishing is always **explicit and manual**.

---

## Privacy model

Podcast privacy is achieved via:

* Static RSS feeds
* Unguessable base URLs
* Manual rotation if a feed is ever leaked

This is the **maximum achievable privacy** within the podcast ecosystem.
No authentication or authorization is involved.

---

## Optional backup strategy

Audio files and metadata may optionally be backed up to a **private GitHub repository**.

Important:

* Backup is manual
* No publishing happens from GitHub
* No system depends on the backup repo

If the backup repo is deleted, nothing breaks.

---

## Design principles

* Static over dynamic
* Manual over automated
* Tools over platforms
* Predictability over convenience
* Boring is good

---

## License
MIT