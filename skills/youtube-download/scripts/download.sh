#!/usr/bin/env bash
set -euo pipefail

# Portable wrapper for download.py
# Works on any machine with python3 and yt-dlp installed.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
exec python3 "$SCRIPT_DIR/download.py" "$@"
