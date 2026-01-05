# Product Requirements Document (PRD)

## static-podcast-publisher

### Version

v1.0

### Owner

Krisztian Gyuris

### Status

Approved for implementation

---

## 1. Overview

**static-podcast-publisher** is a local-first toolset for publishing private podcasts using **static RSS feeds** and **object storage (e.g. Cloudflare R2)**.

The system intentionally avoids:

* Backend services
* Authentication layers
* CI-based publishing
* Podcast hosting platforms

GitHub is used **only** for tooling (public) and **optionally** for cold backup (private).
Podcast delivery happens exclusively via object storage.

---

## 2. Problem Statement

Most podcast hosting solutions:

* Require public feeds or accounts
* Add unnecessary complexity
* Centralize control and content
* Do not align with private or internal publishing needs

Podcast apps also **do not support authentication**, which makes traditional “private hosting” misleading.

A simpler, more honest approach is needed:

* Full author control
* Predictable publishing
* Maximum achievable privacy
* Minimal infrastructure

---

## 3. Goals & Non-Goals

### Goals

* Generate a **valid static podcast RSS feed**
* Publish audio files and RSS to **object storage**
* Support **private or semi-private podcasts** via unguessable URLs
* Keep publishing **manual and explicit**
* Ensure **zero dependency** on GitHub for delivery

### Non-Goals

* No authentication or authorization
* No dynamic RSS endpoints
* No listener analytics
* No monetization features
* No podcast discovery or directories
* No guaranteed secrecy beyond URL obscurity

---

## 4. Target User

* Technical individual (developer, founder, educator)
* Publishing a private or internal podcast
* Values control, simplicity, and transparency
* Comfortable running scripts locally

---

## 5. High-Level Architecture

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

Optional:

```
Private GitHub repo (cold backup)
  ├── episodes
  └── metadata.yaml
```

---

## 6. Key Design Principles

1. **Local-first**
   Publishing happens from the author’s machine.

2. **Static-only**
   RSS and audio files are static artifacts.

3. **Single public surface**
   Only object storage URLs are public.

4. **Optional backup**
   GitHub backup is optional and never required.

5. **Manual over automated**
   No CI/CD pipelines by default.

---

## 7. Functional Requirements

### FR-1: RSS Feed Generation

* Generate a valid RSS 2.0 feed
* Support required podcast fields:

  * title
  * description
  * language
  * pubDate
  * enclosure (audio URL, type, length)
* Feed must be deterministic and reproducible

### FR-2: Metadata Input

* Accept episode and podcast metadata from a local file (YAML)
* Metadata must be human-editable and versionable

### FR-3: Audio Handling

* Audio files are referenced, not embedded
* Audio files are uploaded as-is to object storage
* File names must remain stable

### FR-4: Publishing

* Upload RSS feed and audio files to object storage
* Support S3-compatible storage (Cloudflare R2 primary target)
* Publishing must be explicit (manual command)

### FR-5: URL Privacy Model

* Support publishing under an **unguessable folder path**
* Feed and audio must share the same base path
* Allow easy rotation by changing the folder name

---

## 8. Non-Functional Requirements

### NFR-1: Podcast App Compatibility

* Must work with Apple Podcasts, Overcast, Pocket Casts, etc.
* Must support HTTP byte-range requests via storage provider

### NFR-2: Safety

* No secrets stored in GitHub
* No automated publishing without user intent
* No dependency on CI availability

### NFR-3: Portability

* Storage provider can be swapped (R2 ↔ S3)
* Feed can be regenerated from metadata at any time

---

## 9. Repository Structure (Public Tool Repo)

```
static-podcast-publisher/
├── generate_feed.py
├── publish.sh
├── schema.yaml
├── examples/
│   └── metadata.sample.yaml
├── README.md
└── LICENSE
```

This repository **must not** contain:

* Audio files
* Real metadata
* Generated feeds
* Credentials

---

## 10. Optional Backup Strategy (Out of Scope, Supported)

* Audio files and metadata may be backed up to a **private GitHub repository**
* Backup is manual and optional
* No automation or publishing from backup repo
* No system dependency on the backup

---

## 11. Risks & Mitigations

| Risk                            | Mitigation                         |
| ------------------------------- | ---------------------------------- |
| Feed URL leaked                 | Rotate folder, re-publish          |
| Storage outage                  | Local copy + GitHub backup         |
| User error                      | Manual publishing + clear workflow |
| False expectation of “security” | Explicit documentation             |

---

## 12. Success Criteria

* A user can publish a private podcast without any backend
* Feed works in major podcast apps
* Publishing is predictable and reversible
* No accidental exposure via GitHub or CI
* Setup can be explained in under 5 minutes

---

## 13. Open Questions (Future)

* Per-user feed generation (static variants)
* Episode-level access rotation
* Optional helper CLI
* Multi-podcast support

---

## 14. Decision Summary

> **GitHub is for tools and backup.
> Object storage is for delivery.
> The local machine is the control plane.**

This PRD intentionally favors **clarity and safety over automation**.