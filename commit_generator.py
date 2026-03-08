import os
import subprocess
import sys
import random
from datetime import datetime, timedelta

def run_command(command, cwd, env=None):
    return subprocess.run(
        command, cwd=cwd, env=env, text=True, capture_output=True, check=False
    )

def ensure_git_repo(repo_root):
    result = run_command(["git", "rev-parse", "--is-inside-work-tree"], cwd=repo_root)
    if result.returncode != 0:
        raise RuntimeError("The specified folder is not a Git repository.")

def ensure_log_file(log_file):
    log_file.parent.mkdir(parents=True, exist_ok=True)
    if not log_file.exists():
        log_file.write_text(
            "# Daily Updates\n\n"
            "This file is updated automatically.\n\n",
            encoding="utf-8",
        )

def count_entries(log_file):
    lines = log_file.read_text(encoding="utf-8").splitlines()
    return sum(1 for line in lines if line.startswith("- **"))

def process_commits(start_date_str, end_date_str, min_commits, max_commits, repo_root, log_file, push_after_commit, remote_name, branch_name):
    ensure_git_repo(repo_root)
    ensure_log_file(log_file)
    
    start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
    end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
    
    if start_date > end_date:
        raise ValueError("Start date must be before or equal to the end date.")

    current_date = start_date
    imported_today = datetime.now().strftime("%Y-%m-%d")
    total_commits_made = 0
    
    while current_date <= end_date:
        target_date_str = current_date.strftime("%Y-%m-%d")
        
        # Determine how many commits to make on this specific day
        daily_commit_count = random.randint(min_commits, max_commits)
        
        for i in range(daily_commit_count):
            # Vary the hour and minute 
            hour = 12 + (i % 10)  # Spreads commits between 12:00 PM and 9:00 PM
            minute = random.randint(0, 59)
            target_timestamp = f"{target_date_str} {hour:02d}:{minute:02d}:00"
            
            count = count_entries(log_file) + 1
            line = f"- **{target_date_str}** - update {count} _(imported on {imported_today})_"
            
            with log_file.open("a", encoding="utf-8") as f:
                f.write(line + "\n")
            
            run_command(["git", "add", str(log_file.relative_to(repo_root))], cwd=repo_root)
            
            commit_message = f"add log for {target_date_str} imported on {imported_today} #{count}"
            custom_env = os.environ.copy()
            custom_env["GIT_AUTHOR_DATE"] = target_timestamp
            custom_env["GIT_COMMITTER_DATE"] = target_timestamp
            
            result = run_command(["git", "commit", "-m", commit_message], cwd=repo_root, env=custom_env)
            if result.returncode != 0:
                raise RuntimeError(result.stderr.strip() or f"Git commit failed on {target_date_str}.")
            
            total_commits_made += 1

        print(f"Created {daily_commit_count} commits for {target_date_str}")
        current_date += timedelta(days=1)

    if push_after_commit and total_commits_made > 0:
        print(f"\nPushing {total_commits_made} total commits to {remote_name}/{branch_name}...")
        push_result = run_command(["git", "push", remote_name, branch_name], cwd=repo_root)
        if push_result.returncode != 0:
            raise RuntimeError(push_result.stderr.strip() or "Git push failed.")
        print("Push success")