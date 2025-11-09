#!/usr/bin/env bash
# Format Python source code safely and consistently.
# Stops immediately if any command fails.

set -euo pipefail

echo "[1/2] Formatting code with Ruff..."
ruff format .

echo "[2/2] Organizing imports with Ruff..."
ruff check . --select I --fix

echo "[✓] Code formatted successfully."

