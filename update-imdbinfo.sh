#!/bin/sh
# Restarts the web container if a newer imdbinfo is available on PyPI.
# Restarting triggers entrypoint.sh, which runs `pip install -U imdbinfo`.
#
# Safe to run frequently from a host crontab, e.g. every 10 minutes. The flock
# keeps a slow restart from overlapping with the next tick:
#   */10 * * * * /usr/bin/flock -n /tmp/pizzaypeli-update-imdbinfo.lock /path/to/pizzaypeli/update-imdbinfo.sh >>/path/to/pizzaypeli/cronlog/pizzaypeli-update.log 2>&1
#
# Two things keep this from turning into a restart-every-10-minutes loop:
#   - it only upgrades forwards, so a yanked release (INSTALLED ahead of LATEST)
#     is left alone rather than "fixed" on every run;
#   - if a restart doesn't actually install the new version - entrypoint.sh
#     keeps the container up even when `pip install -U` fails - it backs off for
#     COOLDOWN_SECONDS before retrying that same version.
#
# It stays quiet unless something happens, so an empty log means everything is
# up to date. Weeks of silence while imdbinfo keeps releasing means the cron
# entry itself is missing - check `crontab -l`.

set -eu

cd "$(dirname "$0")"

# Remembers the last upgrade we attempted, so a restart that doesn't actually
# install the new version can't re-trigger on every run. See the cooldown below.
STATE_FILE="${TMPDIR:-/tmp}/pizzaypeli-update-imdbinfo.state"
COOLDOWN_SECONDS=21600  # 6 hours

# Bail if the web container isn't running.
if ! docker compose ps --status running --services 2>/dev/null | grep -qx web; then
    echo "$(date -Is): web container is not running, skipping"
    exit 0
fi

# `pip index versions` reports both INSTALLED and LATEST; compare them.
# (The subcommand is marked experimental but has been stable since pip 21.2.)
output=$(docker compose exec -T web pip index versions imdbinfo 2>/dev/null) || output=''
installed=$(echo "$output" | awk '/INSTALLED:/ {print $2}')
latest=$(echo "$output" | awk '/LATEST:/ {print $2}')

if [ -z "$installed" ] || [ -z "$latest" ]; then
    echo "$(date -Is): could not parse pip output (installed='$installed' latest='$latest')" >&2
    exit 1
fi

[ "$installed" = "$latest" ] && exit 0

# Only upgrade forwards. A yanked release can leave INSTALLED ahead of LATEST,
# and a plain `!=` would then restart the container on every single run.
newest=$(printf '%s\n%s\n' "$installed" "$latest" | sort -V | tail -1)
if [ "$newest" != "$latest" ]; then
    echo "$(date -Is): installed imdbinfo $installed is newer than PyPI's $latest (yanked?), leaving alone"
    exit 0
fi

# entrypoint.sh keeps the container running even when `pip install -U` fails
# (no network, PyPI down), which would leave us restarting every 10 minutes
# forever. If we already tried this exact version and it didn't take, wait out
# the cooldown before trying again.
now=$(date +%s)
if [ -f "$STATE_FILE" ]; then
    last_version=$(awk '{print $1}' "$STATE_FILE")
    last_attempt=$(awk '{print $2}' "$STATE_FILE")
    case "$last_attempt" in
        ''|*[!0-9]*) last_attempt=0 ;;
    esac
    if [ "$last_version" = "$latest" ] && [ $((now - last_attempt)) -lt "$COOLDOWN_SECONDS" ]; then
        echo "$(date -Is): upgrade to imdbinfo $latest already attempted and still not installed (currently $installed), waiting out cooldown" >&2
        exit 0
    fi
fi

echo "$latest $now" > "$STATE_FILE"
echo "$(date -Is): imdbinfo $installed -> $latest, restarting web"
docker compose restart web
