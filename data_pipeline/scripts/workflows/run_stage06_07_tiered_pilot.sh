#!/usr/bin/env bash
set -uo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
pipeline_root="$(cd "${script_dir}/../.." && pwd)"
source_run="${pipeline_root}/runs/stage00-05-qualityfix-published-since-20260101-20260814T201641"
config_path="${pipeline_root}/config.example.json"
output_root=""
harness="codex"
max_parallel=2

usage() {
  printf '%s\n' \
    "Usage: $0 [options]" \
    "" \
    "Run a fixed six-paper Stage06/07 pilot: two papers from each manual suitability tier." \
    "" \
    "Options:" \
    "  --source-run PATH     Historical Stage00-05 run" \
    "  --output-root PATH    Pilot output directory" \
    "  --config PATH         Pipeline config JSON" \
    "  --harness NAME        codex, opencode, or claude (default: codex)" \
    "  --max-parallel N      Concurrent papers (default: 2)" \
    "  -h, --help            Show this help"
}

while (($#)); do
  case "$1" in
    --source-run)
      source_run="$2"
      shift 2
      ;;
    --output-root)
      output_root="$2"
      shift 2
      ;;
    --config)
      config_path="$2"
      shift 2
      ;;
    --harness)
      harness="$2"
      shift 2
      ;;
    --max-parallel)
      max_parallel="$2"
      shift 2
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      printf 'Unknown argument: %s\n' "$1" >&2
      usage >&2
      exit 2
      ;;
  esac
done

case "$harness" in
  codex|opencode|claude) ;;
  *)
    printf 'Unsupported harness: %s\n' "$harness" >&2
    exit 2
    ;;
esac
if [[ ! "$max_parallel" =~ ^[1-9][0-9]*$ ]]; then
  printf 'max-parallel must be a positive integer: %s\n' "$max_parallel" >&2
  exit 2
fi
if [[ ! -d "$source_run" ]]; then
  printf 'Historical source run does not exist: %s\n' "$source_run" >&2
  exit 2
fi
if [[ ! -f "$config_path" ]]; then
  printf 'Config file does not exist: %s\n' "$config_path" >&2
  exit 2
fi

python_bin="${pipeline_root}/.envs/researchchem-data-pipeline/bin/python"
if [[ ! -x "$python_bin" ]]; then
  python_bin="$(command -v python3)"
fi
if [[ "$harness" == "codex" ]] && ! command -v codex >/dev/null 2>&1; then
  printf 'Codex executable is unavailable.\n' >&2
  exit 2
fi

if [[ -z "$output_root" ]]; then
  output_root="${pipeline_root}/runs/stage06-07-tiered-pilot-$(date -u +%Y%m%dT%H%M%SZ)"
fi
mkdir -p "$output_root/papers"
output_root="$(cd "$output_root" && pwd)"
source_run="$(cd "$source_run" && pwd)"
config_path="$(cd "$(dirname "$config_path")" && pwd)/$(basename "$config_path")"

export PATH="$(dirname "$python_bin"):${PATH}"
export PYTHONPATH="${pipeline_root}${PYTHONPATH:+:${PYTHONPATH}}"

write_root_status() {
  local state="$1" started_at="$2" finished_at="${3:-}" failed_count="${4:-}"
  "$python_bin" - \
    "${output_root}/run_status.json" "$state" "$started_at" "$finished_at" \
    "$failed_count" "$source_run" "$config_path" "$harness" "$max_parallel" "$$" <<'PY'
import json
import os
import sys
from pathlib import Path

(
    destination,
    state,
    started_at,
    finished_at,
    failed_count,
    source_run,
    config_path,
    harness,
    max_parallel,
    supervisor_pid,
) = sys.argv[1:]
payload = {
    "state": state,
    "started_at": started_at,
    "updated_at": finished_at or started_at,
    "source_run": source_run,
    "config": config_path,
    "harness": harness,
    "max_parallel": int(max_parallel),
    "supervisor_pid": int(supervisor_pid),
    "paper_count": 6,
}
if finished_at:
    payload["finished_at"] = finished_at
if failed_count:
    payload["failed_count"] = int(failed_count)
path = Path(destination)
temporary = path.with_name(f".{path.name}.{os.getpid()}.tmp")
temporary.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
os.replace(temporary, path)
PY
}

write_paper_status() {
  local destination="$1" state="$2" started_at="$3" finished_at="${4:-}"
  local exit_code="${5:-}" tier="$6" doi="$7" paper_id="$8"
  "$python_bin" - \
    "$destination" "$state" "$started_at" "$finished_at" "$exit_code" \
    "$tier" "$doi" "$paper_id" "$harness" <<'PY'
import json
import os
import sys
from pathlib import Path

destination, state, started_at, finished_at, exit_code, tier, doi, paper_id, harness = sys.argv[1:]
payload = {
    "state": state,
    "started_at": started_at,
    "updated_at": finished_at or started_at,
    "tier": tier,
    "doi": doi,
    "paper_id": paper_id,
    "harness": harness,
}
if finished_at:
    payload["finished_at"] = finished_at
if exit_code:
    payload["exit_code"] = int(exit_code)
path = Path(destination)
temporary = path.with_name(f".{path.name}.{os.getpid()}.tmp")
temporary.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
os.replace(temporary, path)
PY
}

# tier|slot|doi|paper_id|slug|selection rationale
selections=(
  'high_priority|01|10.1002/anie.202525581|paper_6904a9c8c09855cc|gallaphosphene-mechanism|Complete labeled intermediates and transition states'
  'high_priority|02|10.1002/anie.202525044|paper_5286f393dfa5a49a|helitwistacene-conformers|Complete conformer coordinates and thermochemical target'
  'conditional|01|10.1016/j.cej.2025.171477|paper_98946f2af94e53f9|salen-cof-periodic|Periodic coordinates exist but model mapping and spin require resolution'
  'conditional|02|10.1016/j.cclet.2025.111042|paper_6a0e549ed50c8b49|fusadiene-nmr|NMR workflow is promising but asset and software recovery are required'
  'unsuitable_current_candidate|01|10.1002/anie.202518099|paper_10679580b3d561b4|ni111-surface|Exact slab and adsorption structures are missing'
  'unsuitable_current_candidate|02|10.1016/j.cclet.2025.111928|paper_23e9206ce48858f7|selenium-radical-mechanism|Charge and multiplicity assignments are not supported'
)

manifest_path="${output_root}/selection.tsv"
if [[ ! -f "$manifest_path" ]]; then
  printf 'tier\tslot\tdoi\tpaper_id\tworkspace\trationale\n' >"$manifest_path"
  for selection in "${selections[@]}"; do
    IFS='|' read -r tier slot doi paper_id slug rationale <<<"$selection"
    printf '%s\t%s\t%s\t%s\t%s\t%s\n' \
      "$tier" "$slot" "$doi" "$paper_id" "papers/${tier}-${slot}-${slug}" "$rationale" \
      >>"$manifest_path"
  done
fi

run_started_at="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
write_root_status "RUNNING" "$run_started_at"

run_one() {
  local selection="$1"
  local tier slot doi paper_id slug rationale paper_root status_file log_file exit_code
  local paper_started_at paper_finished_at
  IFS='|' read -r tier slot doi paper_id slug rationale <<<"$selection"
  paper_root="${output_root}/papers/${tier}-${slot}-${slug}"
  status_file="${paper_root}/run_status.json"
  log_file="${paper_root}/runner.log"
  mkdir -p "$paper_root"

  if [[ -s "${paper_root}/late_stage_run_summary.json" ]]; then
    paper_started_at="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
    write_paper_status \
      "$status_file" "COMPLETED" "$paper_started_at" "$paper_started_at" "0" \
      "$tier" "$doi" "$paper_id"
    printf '[%s] skip completed %s %s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)" "$tier" "$doi" >>"$log_file"
    return 0
  fi

  paper_started_at="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
  write_paper_status \
    "$status_file" "RUNNING" "$paper_started_at" "" "" "$tier" "$doi" "$paper_id"
  printf '[%s] start tier=%s doi=%s paper_id=%s harness=%s\n' \
    "$(date -u +%Y-%m-%dT%H:%M:%SZ)" "$tier" "$doi" "$paper_id" "$harness" >>"$log_file"

  (
    cd "$pipeline_root"
    "$python_bin" -m src.cli run-stage06-07 \
      --source-run "$source_run" \
      --paper "$paper_id" \
      --output "$paper_root" \
      --config "$config_path" \
      --harness "$harness"
  ) >>"$log_file" 2>&1
  exit_code=$?

  paper_finished_at="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
  if ((exit_code == 0)); then
    write_paper_status \
      "$status_file" "COMPLETED" "$paper_started_at" "$paper_finished_at" "$exit_code" \
      "$tier" "$doi" "$paper_id"
  else
    write_paper_status \
      "$status_file" "FAILED" "$paper_started_at" "$paper_finished_at" "$exit_code" \
      "$tier" "$doi" "$paper_id"
  fi
  printf '[%s] finish tier=%s doi=%s exit_code=%s\n' \
    "$(date -u +%Y-%m-%dT%H:%M:%SZ)" "$tier" "$doi" "$exit_code" >>"$log_file"
  return 0
}

printf '[%s] supervisor started pid=%s output=%s\n' \
  "$(date -u +%Y-%m-%dT%H:%M:%SZ)" "$$" "$output_root"

active=0
for selection in "${selections[@]}"; do
  run_one "$selection" &
  active=$((active + 1))
  if ((active >= max_parallel)); then
    wait -n || true
    active=$((active - 1))
  fi
done
wait || true

failed=0
for selection in "${selections[@]}"; do
  IFS='|' read -r tier slot doi paper_id slug rationale <<<"$selection"
  status_file="${output_root}/papers/${tier}-${slot}-${slug}/run_status.json"
  paper_state="$($python_bin - "$status_file" <<'PY'
import json
import sys
from pathlib import Path

try:
    print(json.loads(Path(sys.argv[1]).read_text(encoding="utf-8")).get("state", ""))
except (OSError, ValueError):
    print("")
PY
)"
  if [[ "$paper_state" != "COMPLETED" ]]; then
    failed=$((failed + 1))
  fi
done

run_finished_at="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
if ((failed == 0)); then
  write_root_status "COMPLETED" "$run_started_at" "$run_finished_at" "$failed"
else
  write_root_status "COMPLETED_WITH_FAILURES" "$run_started_at" "$run_finished_at" "$failed"
fi
printf '[%s] supervisor finished failed=%s\n' \
  "$(date -u +%Y-%m-%dT%H:%M:%SZ)" "$failed"
