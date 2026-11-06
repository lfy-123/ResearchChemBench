#!/usr/bin/env bash
set -euo pipefail
project_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
version=release-20261102.0
target_dir="$project_dir/.software_cache/shared/gvisor/$version"
if [[ -x "$target_dir/runsc" && -x "$target_dir/gvisor-bin/gvisor_sentry" ]]; then
  "$target_dir/runsc" --version
  exit 0
fi
download_dir="$(mktemp -d)"
trap 'rm -rf "$download_dir"' EXIT
curl -fL "https://storage.googleapis.com/gvisor/releases/release/$version/x86_64/gvisor.tar.bz2" -o "$download_dir/gvisor.tar.bz2"
printf '%s  %s\n' '2e6671bb2d033b871c5811ab57e16ac570988b0e0054c525f911cfaf191bab3ca4efb08e0a98daa4b9e7d248f9e5776ef2ef2f8a6b82d829646a42924c98bb05' "$download_dir/gvisor.tar.bz2" | sha512sum -c -
tar -xjf "$download_dir/gvisor.tar.bz2" -C "$download_dir"
mkdir -p "$(dirname "$target_dir")"
mv -T "$download_dir/gvisor" "$target_dir"
"$target_dir/runsc" --version
