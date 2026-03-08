#!/usr/bin/env bash
# =============================================================================
# git-auto-sync.sh - Auto-commit and push changes to origin
# =============================================================================
#
# PURPOSE:
#   Detects file changes (respecting .gitignore), creates a descriptive
#   auto-commit message listing changed files, and pushes to origin.
#
# USAGE:
#   ./scripts/git-auto-sync.sh              # run once
#   ./scripts/git-auto-sync.sh --dry-run    # show what would be committed
#
# SETUP ON DGX-SPARK (cron, every 5 minutes):
#   crontab -e
#   */5 * * * * /home/$USER/git/2026_BMB/scripts/git-auto-sync.sh >> /home/$USER/git/2026_BMB/.git/auto-sync.log 2>&1
#
# DISABLE:
#   crontab -e   # comment out or remove the line
#   -- or --
#   touch ~/git/2026_BMB/.git/auto-sync.disable   # creates kill switch
#
# ENABLE AGAIN:
#   rm ~/git/2026_BMB/.git/auto-sync.disable
#
# =============================================================================

set -euo pipefail

# --- Configuration -----------------------------------------------------------
REPO_DIR="${GIT_AUTO_SYNC_REPO:-$(cd "$(dirname "$0")/.." && pwd)}"
REMOTE="${GIT_AUTO_SYNC_REMOTE:-origin}"
BRANCH="${GIT_AUTO_SYNC_BRANCH:-main}"
MAX_FILES_IN_MSG=10          # truncate commit message after this many files
DRY_RUN=false
LOCK_FILE="${REPO_DIR}/.git/auto-sync.lock"
DISABLE_FILE="${REPO_DIR}/.git/auto-sync.disable"

# --- Parse arguments ----------------------------------------------------------
for arg in "$@"; do
    case "$arg" in
        --dry-run) DRY_RUN=true ;;
        --help|-h)
            sed -n '2,/^# =====/p' "$0" | head -n -1
            exit 0
            ;;
    esac
done

# --- Kill switch check --------------------------------------------------------
if [[ -f "$DISABLE_FILE" ]]; then
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] auto-sync disabled (remove $DISABLE_FILE to re-enable)"
    exit 0
fi

# --- Lock to prevent overlapping runs -----------------------------------------
if [[ -f "$LOCK_FILE" ]]; then
    lock_pid=$(cat "$LOCK_FILE" 2>/dev/null || echo "")
    if [[ -n "$lock_pid" ]] && kill -0 "$lock_pid" 2>/dev/null; then
        echo "[$(date '+%Y-%m-%d %H:%M:%S')] another sync is running (pid $lock_pid), skipping"
        exit 0
    fi
    # stale lock
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

# --- Check for changes --------------------------------------------------------
# Stage all changes (respects .gitignore automatically)
git add -A

# Get list of staged changes
changed_files=$(git diff --cached --name-only 2>/dev/null || true)

if [[ -z "$changed_files" ]]; then
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] no changes to commit"
    exit 0
fi

# --- Build descriptive commit message -----------------------------------------
file_count=$(echo "$changed_files" | wc -l | tr -d ' ')
hostname_short=$(hostname -s 2>/dev/null || echo "unknown")

# Categorize changes
added_files=$(git diff --cached --name-only --diff-filter=A 2>/dev/null || true)
modified_files=$(git diff --cached --name-only --diff-filter=M 2>/dev/null || true)
deleted_files=$(git diff --cached --name-only --diff-filter=D 2>/dev/null || true)

# Build file list for message (truncated if too many)
file_list=""
count=0
while IFS= read -r f; do
    [[ -z "$f" ]] && continue
    count=$((count + 1))
    if [[ $count -le $MAX_FILES_IN_MSG ]]; then
        file_list="${file_list}  - ${f}\n"
    fi
done <<< "$changed_files"

if [[ $count -gt $MAX_FILES_IN_MSG ]]; then
    remaining=$((count - MAX_FILES_IN_MSG))
    file_list="${file_list}  - ... and ${remaining} more files\n"
fi

# Short summary for first line
short_list=$(echo "$changed_files" | head -3 | tr '\n' ', ' | sed 's/,$//')
if [[ $file_count -gt 3 ]]; then
    short_list="${short_list}, ... (+$((file_count - 3)) more)"
fi

commit_msg="auto(${hostname_short}): update ${short_list}

Changed files (${file_count} total):
$(echo -e "$file_list")"

# --- Dry run or commit --------------------------------------------------------
if [[ "$DRY_RUN" == "true" ]]; then
    echo "[DRY RUN] Would commit ${file_count} file(s):"
    echo "$changed_files"
    echo ""
    echo "[DRY RUN] Commit message:"
    echo "$commit_msg"
    git reset HEAD -- . > /dev/null 2>&1
    exit 0
fi

# --- Commit -------------------------------------------------------------------
echo "[$(date '+%Y-%m-%d %H:%M:%S')] committing ${file_count} file(s)"
git commit -m "$commit_msg" --no-gpg-sign

# --- Push ---------------------------------------------------------------------
echo "[$(date '+%Y-%m-%d %H:%M:%S')] pushing to ${REMOTE}/${BRANCH}"
if git push "$REMOTE" "$BRANCH" 2>&1; then
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] push successful"
else
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] push failed - will retry on next run"
    exit 1
fi
