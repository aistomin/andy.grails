#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
PLAYWRIGHT_DIR="${SCRIPT_DIR}/playwright"

if ! command -v npm >/dev/null 2>&1; then
  echo "npm is required to run the E2E tests. Please install Node.js/npm first." >&2
  exit 1
fi

cd "${PLAYWRIGHT_DIR}"

echo "Installing Playwright dependencies (npm install)…"
npm install

echo "Ensuring Playwright browsers are installed…"
npx playwright install

echo "Running Playwright tests…"
npm test

