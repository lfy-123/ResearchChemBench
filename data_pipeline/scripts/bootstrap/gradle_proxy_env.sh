#!/usr/bin/env bash

# Gradle runs inside a JVM and does not automatically honor conventional
# http_proxy/https_proxy variables. Translate an already-configured proxy into
# JVM system properties while leaving direct-network environments unchanged.
proxy_url="${https_proxy:-${HTTPS_PROXY:-${http_proxy:-${HTTP_PROXY:-}}}}"
if [[ -n "$proxy_url" ]]; then
  proxy_address="${proxy_url#*://}"
  proxy_host="${proxy_address%%:*}"
  proxy_port="${proxy_address##*:}"
  if [[ -n "$proxy_host" && "$proxy_port" =~ ^[0-9]+$ ]]; then
    export GRADLE_OPTS="${GRADLE_OPTS:-} -Dhttp.proxyHost=$proxy_host -Dhttp.proxyPort=$proxy_port -Dhttps.proxyHost=$proxy_host -Dhttps.proxyPort=$proxy_port"
  fi
fi

unset proxy_url proxy_address proxy_host proxy_port
