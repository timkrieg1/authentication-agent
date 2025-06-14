import argparse
import os
import datetime
import subprocess

def export_agent(use_case):
    # TODO: Replace with actual Cognigy API logic
    os.makedirs("output", exist_ok=True)
    with open(f"output/{use_case}_example.json", "w") as f:
        f.write('{ "agent": "example content" }')

def create_repo_and_push(use_case):
    today = datetime.date.today().isoformat()
    repo_name = f"{use_case}_{today}"
    subprocess.run(["git", "init", repo_name])
    os.chdir(repo_name)
    subprocess.run(["git", "config", "user.name", "github-actions"])
    subprocess.run(["git", "config", "user.email", "github-actions@github.com"])

    # Copy files from ../output
    subprocess.run(["cp", "-r", "../output/.", "."])
    subprocess.run(["git", "add", "."])
    subprocess.run(["git", "commit", "-m", f"Initial export for {use_case}"])
    
    # Create repo via GitHub CLI
    subprocess.run(["gh", "repo", "create", repo_name, "--public", "--confirm"])
    subprocess.run(["git", "branch", "-M", "main"])
    subprocess.run(["git", "remote", "add", "origin", f"git@github.com:<your-org-or-user>/{repo_name}.git"])
    subprocess.run(["git", "push", "-u", "origin", "main"])

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--use-case", required=True)
    args = parser.parse_args()

    export_agent(args.use_case)
    create_repo_and_push(args.use_case)
