# youtube-download Skill

**Location:** `skills/youtube-download/`
**Created:** 2026-03-22
**Status:** Active

## Overview

Portable YouTube downloader skill for GitHub Copilot CLI and Claude Code. Downloads videos, Shorts, and transcripts using `yt-dlp`.

## Files

| File | Purpose |
|------|---------|
| `SKILL.md` | Copilot CLI / Claude Code skill definition |
| `scripts/download.py` | Core logic — videos, Shorts, and transcripts |
| `scripts/download.sh` | Portable shell wrapper |

## Ported From

Originally based on the original source `youtube-shorts` skill. Key changes:

| Aspect | VM Version | Portable Version |
|--------|-----------|-----------------|
| Scope | Shorts only | Full videos + Shorts + transcripts |
| Paths | Hardcoded VM paths | Portable (`~/Downloads/youtube/`) |
| Drive upload | Yes (VM integration) | Removed |
| Gmail draft | Yes (VM integration) | Removed |
| Python env | VM-specific venv | System Python 3 |
| Transcript | Not supported | `--transcript`, `--transcript-only`, `--lang` flags |

## Prerequisites

- `yt-dlp` (`brew install yt-dlp` on macOS)
- Python 3.9+

## Usage

### Download a video

```bash
./scripts/download.sh --url "https://www.youtube.com/watch?v=VIDEO_ID"
```

### Download a YouTube Short

```bash
./scripts/download.sh --url "https://www.youtube.com/shorts/SHORT_ID"
```

### Download transcript only

```bash
./scripts/download.sh --url "https://www.youtube.com/watch?v=VIDEO_ID" --transcript-only
```

### Download video + transcript

```bash
./scripts/download.sh --url "https://www.youtube.com/watch?v=VIDEO_ID" --transcript
```

### Custom output directory

```bash
./scripts/download.sh --url "https://www.youtube.com/watch?v=VIDEO_ID" --out-dir ~/Desktop/videos
```

### Non-English transcript

```bash
./scripts/download.sh --url "https://www.youtube.com/watch?v=VIDEO_ID" --transcript --lang es
```

## Options

| Flag | Default | Description |
|------|---------|-------------|
| `--url` | (required) | YouTube URL (video, Short, or youtu.be link) |
| `--out-dir` | `~/Downloads/youtube` | Output directory |
| `--transcript` | off | Also download transcript alongside video |
| `--transcript-only` | off | Download transcript only, skip video |
| `--lang` | `en` | Preferred transcript language |
| `--dry-run` | off | Print commands without executing |

## Output

- **Videos** saved as `.mp4` in the output directory
- **Transcripts** saved as `.transcript.txt` (plain text, timestamps stripped)
- **Logs** saved as `.ytdl.log.txt` for debugging

## Deployment

### GitHub Copilot CLI (global)

```bash
mkdir -p ~/.copilot/skills
ln -s <path-to-repo>/skills/youtube-download ~/.copilot/skills/youtube-download
```

### Claude Code

```bash
ln -s <path-to-repo>/skills/youtube-download ~/.claude/skills/youtube-download
```

## Testing

Transcript download verified — successfully downloaded and converted subtitles to plain text.

## Notes

- Cookie-free by default (some age-restricted videos may fail)
- Transcripts use auto-generated captions if manual ones are unavailable
- Output filenames include the video ID for deduplication
