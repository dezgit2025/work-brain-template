---
name: youtube-download
description: Download YouTube videos and transcripts using yt-dlp. Use when the user wants to download a YouTube video to MP4, extract subtitles/transcripts as text, or save a YouTube Short. Supports full videos, Shorts, playlists (single video), and transcript-only mode.
---

# YouTube Download

Download YouTube videos and/or transcripts locally using `yt-dlp`.

## Prerequisites

- `yt-dlp` installed (`brew install yt-dlp` on Mac)
- Python 3.9+

## Usage

### Download a video

```bash
./scripts/download.sh \
  --url "https://www.youtube.com/watch?v=VIDEO_ID"
```

### Download a YouTube Short

```bash
./scripts/download.sh \
  --url "https://www.youtube.com/shorts/SHORT_ID"
```

### Download transcript only (no video)

```bash
./scripts/download.sh \
  --url "https://www.youtube.com/watch?v=VIDEO_ID" \
  --transcript-only
```

### Download video + transcript

```bash
./scripts/download.sh \
  --url "https://www.youtube.com/watch?v=VIDEO_ID" \
  --transcript
```

### Specify output directory

```bash
./scripts/download.sh \
  --url "https://www.youtube.com/watch?v=VIDEO_ID" \
  --out-dir ~/Desktop/videos
```

### Specify language for transcript

```bash
./scripts/download.sh \
  --url "https://www.youtube.com/watch?v=VIDEO_ID" \
  --transcript --lang es
```

## Output

- **Videos** → `~/Downloads/youtube/<slug>-<timestamp>-<id>.mp4`
- **Transcripts** → `~/Downloads/youtube/<slug>-<timestamp>-<id>.transcript.txt`
- **Logs** → `~/Downloads/youtube/<slug>-<timestamp>.ytdl.log.txt`

## Options

| Flag | Default | Description |
|------|---------|-------------|
| `--url` | (required) | YouTube URL (video, Short, or youtu.be link) |
| `--out-dir` | `~/Downloads/youtube` | Output directory |
| `--transcript` | off | Also download transcript alongside video |
| `--transcript-only` | off | Download transcript only, skip video |
| `--lang` | `en` | Preferred transcript language |
| `--dry-run` | off | Print commands without executing |

## Notes

- Cookie-free by default (some age-restricted videos may fail)
- Transcripts use auto-generated captions if manual ones are unavailable
- Output files include the video ID for deduplication
