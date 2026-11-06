#!/usr/bin/env bash
# Sourced by the small-molecule launchers; install exact versions without
# replacing global executables used by other evaluations.
eval_cli_matches() {
  local cli=$1 executable=$2 version=$3 output
  [[ -x $executable ]] || return 1
  output=$(timeout 30 "$executable" --version 2>/dev/null) || return 1
  case "$cli" in
    codex) [[ $output == "codex-cli $version" ]] ;;
    claude) [[ $output == "$version (Claude Code)" ]] ;;
    gemini) [[ $output == "$version" ]] ;;
  esac
}

ensure_eval_cli() {
  local cli=$1 package=$2 version=$3 executable prefix
  prefix="$ROOT/.envs/eval-cli/$cli-$version"
  executable="$prefix/node_modules/.bin/$cli"
  if eval_cli_matches "$cli" "$executable" "$version"; then
    printf '%s\n' "$executable"
    return
  fi
  executable=$(type -P "$cli" || true)
  if eval_cli_matches "$cli" "$executable" "$version"; then
    realpath -s "$executable"
    return
  fi
  executable="$prefix/node_modules/.bin/$cli"
  mkdir -p "$prefix" || return 2
  (
    # Multiple paper launches may need the same installation at once.
    flock -x 9 || exit 2
    if ! eval_cli_matches "$cli" "$executable" "$version"; then
      echo "Installing $package@$version into $prefix" >&2
      npm install --prefix "$prefix" --no-audit --no-fund --save-exact "$package@$version" >&2 || exit 2
    fi
    if ! eval_cli_matches "$cli" "$executable" "$version"; then
      echo "Required $cli version $version could not be verified; evaluation stopped." >&2
      exit 2
    fi
  ) 9>"$prefix/install.lock" || return 2
  printf '%s\n' "$executable"
}

ensure_eval_cli_versions() {
  local codex claude gemini
  export DISABLE_AUTOUPDATER=1
  # ARCHE uses its own bundled Codex regardless of PATH. Do not let a PATH
  # version check silently approve a different runtime.
  if [[ $AGENT == arche ]]; then
    "$PYTHON" - "$ROOT" "$CODEX_CLI_VERSION" <<'PY' || return 2
import json, runpy, sys
from pathlib import Path
config = runpy.run_path(str(Path(sys.argv[1]) / "custom_agents/Arche-Harness/src/chemistry_multiagent/harness/config.py"))
version = json.loads(config["CODEX_PACKAGE_MANIFEST"].read_text())["version"]
if version != sys.argv[2]:
    raise SystemExit(f"ARCHE bundles Codex {version}, but {sys.argv[2]} is required. "
                     "Its bundled runtime must be upgraded before this launcher can run ARCHE.")
PY
  fi
  codex=$(ensure_eval_cli codex @openai/codex "$CODEX_CLI_VERSION") || return 2
  claude=$(ensure_eval_cli claude @anthropic-ai/claude-code "$CLAUDE_CODE_VERSION") || return 2
  gemini=$(ensure_eval_cli gemini @google/gemini-cli "$GEMINI_CLI_VERSION") || return 2
  export PATH="$(dirname "$codex"):$(dirname "$claude"):$(dirname "$gemini"):$PATH"
  export RCB_CODEX_EXECUTABLE="$codex" RCB_CLAUDE_EXECUTABLE="$claude" RCB_GEMINI_EXECUTABLE="$gemini"
}
