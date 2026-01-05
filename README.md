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

## Local directories

This project expects the following local directories, which are intentionally
excluded from version control:

- `input/`  
  Contains podcast metadata and local episode references.

- `output/`  
  Generated RSS feed and publish-ready audio structure.

Both directories are created and managed locally.
