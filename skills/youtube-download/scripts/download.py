#!/usr/bin/env python3
"""Download YouTube videos and/or transcripts via yt-dlp.

Portable version — no hardcoded paths, works on any machine with yt-dlp.
"""

from __future__ import annotations

import argparse
import re
import shlex
import subprocess
from datetime import datetime, timezone
from pathlib import Path


def utc_stamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def safe_slug(url: str) -> str:
    s = re.sub(r"https?://", "", url.strip())
    s = re.sub(r"[^a-zA-Z0-9._-]+", "_", s)
    s = re.sub(r"_+", "_", s).strip("_")
    return (s[:80] or "video").lower()


def run(cmd: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run(
        cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True
    )


def download_video(url: str, out_dir: Path, stamp: str, slug: str) -> Path | None:
    out_tpl = str(out_dir / f"{slug}-{stamp}-%(id)s.%(ext)s")
    cmd = [
        "yt-dlp",
        "--no-playlist",
        "--restrict-filenames",
        "-f", "bv*+ba/b",
        "--merge-output-format", "mp4",
        "-o", out_tpl,
        url,
    ]
    print("CMD:", " ".join(shlex.quote(x) for x in cmd))

    log_path = out_dir / f"{slug}-{stamp}.ytdl.log.txt"
    res = run(cmd)
    log_path.write_text(res.stdout, encoding="utf-8", errors="replace")

    if res.returncode != 0:
        print("ERROR: yt-dlp failed; see log:", log_path)
        return None

    mp4s = sorted(
        out_dir.glob(f"{slug}-{stamp}-*.mp4"),
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    )
    if not mp4s:
        mp4s = sorted(
            out_dir.glob(f"{slug}-{stamp}-*"),
            key=lambda p: p.stat().st_mtime,
            reverse=True,
        )
    if not mp4s:
        print("WARN: download OK but output file not found; see log:", log_path)
        return None

    print("OK: downloaded:", mp4s[0])
    return mp4s[0]


def download_transcript(
    url: str, out_dir: Path, stamp: str, slug: str, lang: str
) -> Path | None:
    # Write subtitle to a temp file, then convert to plain text
    sub_tpl = str(out_dir / f"{slug}-{stamp}-%(id)s")
    cmd = [
        "yt-dlp",
        "--no-playlist",
        "--skip-download",
        "--write-subs",
        "--write-auto-subs",
        "--sub-lang", lang,
        "--sub-format", "vtt",
        "--convert-subs", "srt",
        "-o", sub_tpl,
        url,
    ]
    print("CMD:", " ".join(shlex.quote(x) for x in cmd))

    log_path = out_dir / f"{slug}-{stamp}.transcript.log.txt"
    res = run(cmd)
    log_path.write_text(res.stdout, encoding="utf-8", errors="replace")

    if res.returncode != 0:
        print("ERROR: transcript download failed; see log:", log_path)
        return None

    # Find the .srt file
    srt_files = sorted(
        out_dir.glob(f"{slug}-{stamp}-*.srt"),
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    )
    if not srt_files:
        # Try .vtt as fallback
        srt_files = sorted(
            out_dir.glob(f"{slug}-{stamp}-*.vtt"),
            key=lambda p: p.stat().st_mtime,
            reverse=True,
        )

    if not srt_files:
        print("WARN: no subtitle file found; see log:", log_path)
        return None

    # Convert SRT/VTT to plain text
    raw = srt_files[0].read_text(encoding="utf-8", errors="replace")
    lines = _srt_to_text(raw)
    txt_path = out_dir / f"{slug}-{stamp}-{srt_files[0].stem.split('-')[-1]}.transcript.txt"
    txt_path.write_text(lines, encoding="utf-8")

    # Clean up the raw subtitle file
    srt_files[0].unlink(missing_ok=True)

    print("OK: transcript saved:", txt_path)
    return txt_path


def _srt_to_text(srt_content: str) -> str:
    """Strip SRT/VTT timestamps and indices, return plain text."""
    lines = []
    seen = set()
    for line in srt_content.splitlines():
        line = line.strip()
        # Skip sequence numbers, timestamps, VTT headers
        if not line:
            continue
        if re.match(r"^\d+$", line):
            continue
        if re.match(r"^[\d:.,\-> ]+$", line):
            continue
        if line.startswith("WEBVTT") or line.startswith("Kind:") or line.startswith("Language:"):
            continue
        # Strip HTML tags (yt-dlp sometimes includes <c> tags)
        clean = re.sub(r"<[^>]+>", "", line)
        clean = clean.strip()
        if clean and clean not in seen:
            seen.add(clean)
            lines.append(clean)
    return "\n".join(lines)


def main() -> None:
    ap = argparse.ArgumentParser(
        description="Download YouTube videos and/or transcripts"
    )
    ap.add_argument("--url", required=True, help="YouTube URL")
    ap.add_argument(
        "--out-dir",
        default=str(Path.home() / "Downloads" / "youtube"),
        help="Output directory (default: ~/Downloads/youtube)",
    )
    ap.add_argument(
        "--transcript", action="store_true", help="Also download transcript"
    )
    ap.add_argument(
        "--transcript-only",
        action="store_true",
        help="Download transcript only, skip video",
    )
    ap.add_argument(
        "--lang", default="en", help="Transcript language (default: en)"
    )
    ap.add_argument("--dry-run", action="store_true", help="Print commands only")
    args = ap.parse_args()

    out_dir = Path(args.out_dir).expanduser()
    out_dir.mkdir(parents=True, exist_ok=True)

    stamp = utc_stamp()
    slug = safe_slug(args.url)

    print("OUT_DIR:", out_dir)
    print("URL:", args.url)

    if args.dry_run:
        print("DRY_RUN: skipping execution")
        return

    if args.transcript_only:
        download_transcript(args.url, out_dir, stamp, slug, args.lang)
    else:
        download_video(args.url, out_dir, stamp, slug)
        if args.transcript:
            download_transcript(args.url, out_dir, stamp, slug, args.lang)


if __name__ == "__main__":
    main()
