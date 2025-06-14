import os
import json
import random
import string
from datetime import datetime
import subprocess
import sys

# Get CLI argument
use_case = sys.argv[sys.argv.index("--use-case") + 1]
timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
branch_name = f"{use_case}_{timestamp}"

# File setup
folder = "output"
os.makedirs(folder, exist_ok=True)
filename = f"{folder}/{use_case}_{timestamp}.json"

# Create dummy data
data = {
    "use_case": use_case,
    "payload": ''.join(random.choices(string.ascii_letters + string.digits, k=32))
}

# Write the file
with open(filename, "w") as f:
    json.dump(data, f, indent=2)
print(f"Created file: {filename}")

# Git config
subprocess.run(["git", "config", "--global", "user.email", "actions@github.com"], check=True)
subprocess.run(["git", "config", "--global", "user.name", "github-actions"], check=True)

# Create orphan branch (no history)
subprocess.run(["git", "checkout", "--orphan", branch_name], check=True)
subprocess.run(["git", "rm", "-rf", "."], check=False)  # ignore errors if repo is already empty

# Move the file to root for clean branch (optional)
os.rename(filename, f"{use_case}_{timestamp}.json")

# Commit and push
subprocess.run(["git", "add", f"{use_case}_{timestamp}.json"], check=True)
subprocess.run(["git", "commit", "-m", f"Add extracted agent for {use_case}"], check=True)
subprocess.run(["git", "push", "-u", "origin", branch_name], check=True)

print(f"🚀 Pushed new orphan branch: {branch_name}")
