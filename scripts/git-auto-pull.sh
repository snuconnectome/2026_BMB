#!/usr/bin/env bash
# =============================================================================
# git-auto-pull.sh - Auto-pull changes from origin with conflict handling
# =============================================================================
#
# PURPOSE:
#   Pulls latest changes from origin. If local uncommitted changes conflict,
#   stashes them, pulls, then re-applies the stash.
#
# USAGE:
#   ./scripts/git-auto-pull.sh              # run once
#   ./scripts/git-auto-pull.sh --dry-run    # show what would happen
#
# SETUP ON MAC (launchd, every 5 minutes):
#   1. Copy the plist (printed by --install-launchd) to ~/Library/LaunchAgents/
#   2. launchctl load ~/Library/LaunchAgents/com.user.git-auto-pull-2026bmb.plist
#
#   Or use cron instead:
#   crontab -e
#   */5 * * * * /Users/$USER/Documents/git/2026_BMB/scripts/git-auto-pull.sh >> /Users/$USER/Documents/git/2026_BMB/.git/auto-pull.log 2>&1
#
# DISABLE:
#   touch ~/Documents/git/2026_BMB/.git/auto-pull.disable
#   -- or for launchd --
#   launchctl unload ~/Library/LaunchAgents/com.user.git-auto-pull-2026bmb.plist
#
# ENABLE AGAIN:
#   rm ~/Documents/git/2026_BMB/.git/auto-pull.disable
#   -- or for launchd --
#   launchctl load ~/Library/LaunchAgents/com.user.git-auto-pull-2026bmb.plist
#
# =============================================================================

set -euo pipefail

# --- Configuration -----------------------------------------------------------
REPO_DIR="${GIT_AUTO_PULL_REPO:-$(cd "$(dirname "$0")/.." && pwd)}"
REMOTE="${GIT_AUTO_PULL_REMOTE:-origin}"
BRANCH="${GIT_AUTO_PULL_BRANCH:-main}"
DRY_RUN=false
INSTALL_LAUNCHD=false
LOCK_FILE="${REPO_DIR}/.git/auto-pull.lock"
DISABLE_FILE="${REPO_DIR}/.git/auto-pull.disable"

# --- Parse arguments ----------------------------------------------------------
for arg in "$@"; do
    case "$arg" in
        --dry-run) DRY_RUN=true ;;
        --install-launchd) INSTALL_LAUNCHD=true ;;
        --help|-h)
            sed -n '2,/^# =====/p' "$0" | head -n -1
            exit 0
            ;;
    esac
done

# --- Launchd plist installer --------------------------------------------------
if [[ "$INSTALL_LAUNCHD" == "true" ]]; then
    PLIST_DIR="$HOME/Library/LaunchAgents"
    PLIST_NAME="com.user.git-auto-pull-2026bmb.plist"
    PLIST_PATH="${PLIST_DIR}/${PLIST_NAME}"
    SCRIPT_PATH="${REPO_DIR}/scripts/git-auto-pull.sh"
    LOG_PATH="${REPO_DIR}/.git/auto-pull.log"

    mkdir -p "$PLIST_DIR"

    cat > "$PLIST_PATH" <<PLIST_EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>${PLIST_NAME%.plist}</string>
    <key>ProgramArguments</key>
    <array>
        <string>${SCRIPT_PATH}</string>
    </array>
    <key>StartInterval</key>
    <integer>300</integer>
    <key>StandardOutPath</key>
    <string>${LOG_PATH}</string>
    <key>StandardErrorPath</key>
    <string>${LOG_PATH}</string>
    <key>RunAtLoad</key>
    <true/>
    <key>EnvironmentVariables</key>
    <dict>
        <key>PATH</key>
        <string>/usr/local/bin:/usr/bin:/bin:/opt/homebrew/bin</string>
    </dict>
</dict>
</plist>
PLIST_EOF

    echo "Installed launchd plist to: ${PLIST_PATH}"
    echo ""
    echo "To activate:"
    echo "  launchctl load ${PLIST_PATH}"
    echo ""
    echo "To deactivate:"
    echo "  launchctl unload ${PLIST_PATH}"
    exit 0
fi

# --- Kill switch check --------------------------------------------------------
if [[ -f "$DISABLE_FILE" ]]; then
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] auto-pull disabled (remove $DISABLE_FILE to re-enable)"
    exit 0
fi

# --- Lock to prevent overlapping runs -----------------------------------------
if [[ -f "$LOCK_FILE" ]]; then
    lock_pid=$(cat "$LOCK_FILE" 2>/dev/null || echo "")
    if [[ -n "$lock_pid" ]] && kill -0 "$lock_pid" 2>/dev/null; then
        echo "[$(date '+%Y-%m-%d %H:%M:%S')] another pull is running (pid $lock_pid), skipping"
        exit 0
    fi
    rm -f "$LOCK_FILE"
fi
echo $$ > "$LOCK_FILE"
trap 'rm -f "$LOCK_FILE"' EXIT

# --- Change to repo -----------------------------------------------------------
cd "$REPO_DIR"

# --- Ensure we are on the correct branch -------------------------------------
current_branch=$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "")
if [[ "$current_branch" != "$BRANCH" ]]; then
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] not on branch '$BRANCH' (on '$current_branch'), skipping"
    exit 0
fi

# --- Fetch first to check if there are remote changes -------------------------
echo "[$(date '+%Y-%m-%d %H:%M:%S')] fetching from ${REMOTE}/${BRANCH}"
git fetch "$REMOTE" "$BRANCH" 2>&1

local_head=$(git rev-parse HEAD)
remote_head=$(git rev-parse "${REMOTE}/${BRANCH}")

if [[ "$local_head" == "$remote_head" ]]; then
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] already up to date"
    exit 0
fi

# --- Dry run ------------------------------------------------------------------
if [[ "$DRY_RUN" == "true" ]]; then
    incoming=$(git log --oneline "${local_head}..${remote_head}" 2>/dev/null || true)
    echo "[DRY RUN] Would pull the following commits:"
    echo "$incoming"
    exit 0
fi

# --- Check for local changes that might conflict ------------------------------
has_changes=false
if ! git diff --quiet 2>/dev/null || ! git diff --cached --quiet 2>/dev/null; then
    has_changes=true
fi

stashed=false
if [[ "$has_changes" == "true" ]]; then
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] stashing local changes before pull"
    stash_msg="auto-pull-stash-$(date '+%Y%m%d-%H%M%S')"
    git stash push -m "$stash_msg" --include-untracked
    stashed=true
fi

# --- Pull ---------------------------------------------------------------------
echo "[$(date '+%Y-%m-%d %H:%M:%S')] pulling from ${REMOTE}/${BRANCH}"
if git pull --ff-only "$REMOTE" "$BRANCH" 2>&1; then
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] pull successful (fast-forward)"
elif git pull --rebase "$REMOTE" "$BRANCH" 2>&1; then
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] pull successful (rebase)"
else
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] pull failed - attempting merge abort and retry next run"
    git rebase --abort 2>/dev/null || true
    git merge --abort 2>/dev/null || true
    # Re-apply stash if we stashed
    if [[ "$stashed" == "true" ]]; then
        git stash pop 2>/dev/null || true
    fi
    exit 1
fi

# --- Re-apply stashed changes -------------------------------------------------
if [[ "$stashed" == "true" ]]; then
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] re-applying stashed changes"
    if git stash pop 2>&1; then
        echo "[$(date '+%Y-%m-%d %H:%M:%S')] stash re-applied successfully"
    else
        echo "[$(date '+%Y-%m-%d %H:%M:%S')] WARNING: stash pop had conflicts - changes saved in stash, resolve manually"
        echo "[$(date '+%Y-%m-%d %H:%M:%S')] run 'git stash list' and 'git stash show -p' to inspect"
    fi
fi

echo "[$(date '+%Y-%m-%d %H:%M:%S')] sync complete"
