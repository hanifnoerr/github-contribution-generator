import sys
from pathlib import Path
from commit_generator import process_commits

# Define the Date Range (Format: "YYYY-MM-DD")
START_DATE = "2025-03-09"
END_DATE = "2026-03-08"

# The script will randomly pick a number between these two values for each day.
MIN_COMMITS_PER_DAY = 5 # Set MIN_COMMITS to 0 if you want to occasionally have completely blank days.
MAX_COMMITS_PER_DAY = 21

# Repository Settings
REPO_ROOT = Path(__file__).resolve().parent
LOG_FILE = REPO_ROOT / "logs" / "daily_updates.md"

# Push Settings
PUSH_AFTER_COMMIT = True # Set to True if you want the script to automatically push after making commits. Make sure you have the correct permissions and remote setup before enabling this.
REMOTE_NAME = "origin"
BRANCH_NAME = "main"

def run():
    print(f"Starting commit generation from {START_DATE} to {END_DATE}...")
    print(f"Targeting between {MIN_COMMITS_PER_DAY} and {MAX_COMMITS_PER_DAY} commits per day.\n")
    try:
        process_commits(
            start_date_str=START_DATE,
            end_date_str=END_DATE,
            min_commits=MIN_COMMITS_PER_DAY,
            max_commits=MAX_COMMITS_PER_DAY,
            repo_root=REPO_ROOT,
            log_file=LOG_FILE,
            push_after_commit=PUSH_AFTER_COMMIT,
            remote_name=REMOTE_NAME,
            branch_name=BRANCH_NAME
        )
        print("\nAll done! Your contribution graph should now reflect the new history.")
    except Exception as exc:
        print("\nERROR:", exc, file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    run()