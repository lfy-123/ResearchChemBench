#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
GROBID_REPO="$ROOT/third_party/grobid"
GROBID_VERSION="0.9.0"

command -v git >/dev/null || {
  echo "git is required." >&2
  exit 1
}

if [[ -n "${GROBID_JAVA_HOME:-}" ]]; then
  JAVA_HOME="$GROBID_JAVA_HOME"
elif [[ -n "${JAVA_HOME:-}" ]]; then
  JAVA_HOME="$JAVA_HOME"
elif command -v conda >/dev/null; then
  JAVA_HOME="$(conda info --base)"
else
  echo "OpenJDK 21 is required. Set GROBID_JAVA_HOME or JAVA_HOME." >&2
  exit 1
fi
export JAVA_HOME
export PATH="$JAVA_HOME/bin:$PATH"

java_version="$(java -version 2>&1 | sed -n '1s/.*version "\([0-9][0-9]*\).*/\1/p')"
if [[ -z "$java_version" || "$java_version" -lt 21 ]]; then
  echo "GROBID requires OpenJDK 21 or newer; found: $(java -version 2>&1 | head -1)" >&2
  exit 1
fi

mkdir -p "$ROOT/third_party"
if [[ ! -d "$GROBID_REPO/.git" ]]; then
  git clone --branch "$GROBID_VERSION" --depth 1 \
    https://github.com/grobidOrg/grobid.git "$GROBID_REPO"
fi

if ! git -C "$GROBID_REPO" diff --quiet || \
   ! git -C "$GROBID_REPO" diff --cached --quiet; then
  echo "GROBID checkout has local changes; refusing to switch versions." >&2
  exit 1
fi
git -C "$GROBID_REPO" fetch --depth 1 origin "refs/tags/$GROBID_VERSION:refs/tags/$GROBID_VERSION"
git -C "$GROBID_REPO" checkout --detach "$GROBID_VERSION"

(cd "$GROBID_REPO" && ./gradlew :grobid-service:classes)
"${PIPELINE_PYTHON:-python}" "$ROOT/scripts/prepare_model_cache.py"

echo
echo "GROBID $GROBID_VERSION is built with $(java -version 2>&1 | head -1)."
echo "The pipeline will start and stop the local service automatically."
