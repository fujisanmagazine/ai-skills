#!/bin/sh
# Runs a command with the Fujisan documentation credentials loaded from a local env file.
# The credentials never reach argv, shell history, or this script's output.
set -eu

env_file="${APIDOC_ENV_FILE:-$HOME/.config/fujisan/apidoc.env}"

if [ "$#" -eq 0 ]; then
  echo "usage: scripts/with-apidoc-creds.sh <command> [args...]" >&2
  exit 2
fi

if [ ! -f "$env_file" ]; then
  echo "error: $env_file not found. Create it with APIDOC_BASIC_USERNAME and APIDOC_BASIC_PASSWORD, then run: chmod 600 $env_file" >&2
  exit 2
fi

# GNU coreutils: -c is the format and -f is --file-system.
# BSD/macOS: -f is the format and -c is an illegal option.
# Probe -c first and discard that output. On GNU, -f still prints filesystem
# details for a real path and exits non-zero, so a -f-first `||` fallback
# concatenates those details with the permission bits.
if stat -c '%a' "$env_file" >/dev/null 2>&1; then
  mode=$(stat -c '%a' "$env_file")
else
  mode=$(stat -f '%OLp' "$env_file")
fi
case "$mode" in
  600|400) ;;
  *)
    echo "error: $env_file is mode $mode and is readable beyond its owner. Run: chmod 600 $env_file" >&2
    exit 2
    ;;
esac

set -a
. "$env_file"
set +a

for name in APIDOC_BASIC_USERNAME APIDOC_BASIC_PASSWORD; do
  eval "value=\${$name:-}"
  if [ -z "$value" ]; then
    echo "error: $name is not set in $env_file" >&2
    exit 2
  fi
done

exec "$@"
