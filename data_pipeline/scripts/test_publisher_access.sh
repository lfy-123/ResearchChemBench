#!/usr/bin/env bash

set -uo pipefail

MODE="current"
SETUP_PROXY_URL="${SETUP_PROXY_URL:-http://deploy.i.h.pjlab.org.cn/infra/scripts/setup_proxy.sh}"
CLOSEAI_PROXY_URL="${CLOSEAI_PROXY_URL:-http://closeai-proxy.pjlab.org.cn:23128}"
AUTH_PROXY_URL="${PUBLISHER_TEST_AUTH_PROXY:-}"

usage() {
    cat <<'EOF'
Usage: test_publisher_access.sh [--mode MODE]

Test publisher pages and supplementary attachment endpoints with bounded
1 KiB requests. MODE is one of:

  current   Keep the current proxy environment (default)
  none      Disable all HTTP/HTTPS proxies
  setup     Source the PJLab setup_proxy.sh script
  closeai   Use closeai-proxy.pjlab.org.cn:23128
  auth      Use the proxy in PUBLISHER_TEST_AUTH_PROXY
  all       Run none, setup, closeai, and auth when configured

Examples:
  ./data_pipeline/scripts/test_publisher_access.sh --mode none
  ./data_pipeline/scripts/test_publisher_access.sh --mode setup
  PUBLISHER_TEST_AUTH_PROXY='http://user:password@host:port/' \
    ./data_pipeline/scripts/test_publisher_access.sh --mode auth
  ./data_pipeline/scripts/test_publisher_access.sh --mode all
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        --mode)
            [[ $# -ge 2 ]] || { echo "--mode requires a value" >&2; exit 2; }
            MODE="$2"
            shift 2
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        *)
            echo "Unknown argument: $1" >&2
            usage >&2
            exit 2
            ;;
    esac
done

redact_proxy() {
    local value="${1:-}"
    if [[ -z "$value" ]]; then
        printf '<unset>'
        return
    fi
    printf '%s' "$value" | sed -E 's#(https?://)[^/@]+@#\1***@#'
}

test_url() {
    local name="$1"
    local url="$2"
    local output
    local status

    echo
    echo "===== ${name} ====="
    output=$(curl -sS -L \
        --range 0-1023 \
        --connect-timeout 10 \
        --max-time 30 \
        --user-agent 'ResearchChemBench/1.0 publisher-access-test' \
        -o /dev/null \
        -w $'http_code=%{http_code}\nremote_ip=%{remote_ip}\ncontent_type=%{content_type}\nsize_download=%{size_download}\ntime_connect=%{time_connect}\ntime_total=%{time_total}\nfinal_url=%{url_effective}\n' \
        "$url" 2>&1)
    status=$?
    printf 'curl_exit=%s\n%s\n' "$status" "$output"
}

run_suite() {
    echo
    echo "############################################################"
    echo "mode=${1}"
    echo "http_proxy=$(redact_proxy "${http_proxy:-${HTTP_PROXY:-}}")"
    echo "https_proxy=$(redact_proxy "${https_proxy:-${HTTPS_PROXY:-}}")"
    echo "no_proxy=${no_proxy:-${NO_PROXY:-<unset>}}"
    echo "############################################################"

    test_url "Crossref connectivity" \
        "https://api.crossref.org/works/10.1016/j.checat.2023.100826"
    test_url "Wiley article" \
        "https://onlinelibrary.wiley.com/doi/10.1002/anie.202502890"
    test_url "Wiley supplementary file" \
        "https://onlinelibrary.wiley.com/action/downloadSupplement?doi=10.1002%2Fanie.202502890&file=anie202502890-sup-0001-SuppMat.pdf"
    test_url "ACS article" \
        "https://pubs.acs.org/doi/10.1021/jacs.4c08163"
    test_url "ACS Figshare API" \
        "https://api.figshare.com/v2/articles?resource_doi=10.1021%2Fjacs.4c08163"
    test_url "RSC article" \
        "https://pubs.rsc.org/en/content/articlelanding/2024/sc/d4sc03832k"
    test_url "Elsevier supplementary file" \
        "https://ars.els-cdn.com/content/image/1-s2.0-S2667109323004062-mmc1.pdf"
}

run_mode() (
    local requested_mode="$1"
    case "$requested_mode" in
        current)
            ;;
        none)
            unset http_proxy https_proxy HTTP_PROXY HTTPS_PROXY all_proxy ALL_PROXY
            export no_proxy='*'
            export NO_PROXY='*'
            ;;
        setup)
            # shellcheck disable=SC1090
            source <(curl -sSL "$SETUP_PROXY_URL") >/dev/null
            ;;
        closeai)
            export http_proxy="$CLOSEAI_PROXY_URL"
            export https_proxy="$CLOSEAI_PROXY_URL"
            unset HTTP_PROXY HTTPS_PROXY all_proxy ALL_PROXY
            ;;
        auth)
            if [[ -z "$AUTH_PROXY_URL" ]]; then
                echo "PUBLISHER_TEST_AUTH_PROXY is required for --mode auth" >&2
                return 2
            fi
            export http_proxy="$AUTH_PROXY_URL"
            export https_proxy="$AUTH_PROXY_URL"
            unset HTTP_PROXY HTTPS_PROXY all_proxy ALL_PROXY
            ;;
        *)
            echo "Unsupported mode: $requested_mode" >&2
            return 2
            ;;
    esac
    run_suite "$requested_mode"
)

case "$MODE" in
    all)
        run_mode none
        run_mode setup
        run_mode closeai
        if [[ -n "$AUTH_PROXY_URL" ]]; then
            run_mode auth
        else
            echo
            echo "Skipping auth mode: PUBLISHER_TEST_AUTH_PROXY is not set."
        fi
        ;;
    current|none|setup|closeai|auth)
        run_mode "$MODE"
        ;;
    *)
        echo "Unsupported mode: $MODE" >&2
        usage >&2
        exit 2
        ;;
esac
