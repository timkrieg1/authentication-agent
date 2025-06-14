import os
import json
import random
import string
from datetime import datetime
import subprocess
import sys
import shutil

# --- Parse CLI argument ---
use_case = sys.argv[sys.argv.index("--use-case") + 1]
timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
branch_name = f"{use_case}_{timestamp}"
agent_folder = "agent"

# --- Generate dummy agent export data ---
data = {
    "use_case": use_case,
    "export_id": ''.join(random.choices(string.ascii_letters + string.digits, k=10)),
    "timestamp": timestamp
}

# --- Clean existing agent folder if it exists ---
if os.path.exists(agent_folder):
    shutil.rmtree(agent_folder)
os.makedirs(agent_folder, exist_ok=True)

filename = f"{agent_folder}/export.json"
with open(filename, "w") as f:
    json.dump(data, f, indent=2)
print(f"✅ Export written to {filename}")

# --- Git config ---
subprocess.run(["git", "config", "--global", "user.email", "actions@github.com"], check=True)
subprocess.run(["git", "config", "--global", "user.name", "github-actions"], check=True)

# --- Ensure we are on main and up to date ---
subprocess.run(["git", "checkout", "main"], check=True)
subprocess.run(["git", "pull", "origin", "main"], check=True)

# --- Create new branch from main ---
subprocess.run(["git", "checkout", "-b", branch_name], check=True)

# --- Stage and commit new agent export ---
subprocess.run(["git", "add", agent_folder], check=True)
subprocess.run(["git", "commit", "-m", f"Update agent export for {use_case}"], check=True)

# --- Push the new branch ---
subprocess.run(["git", "push", "-u", "origin", branch_name], check=True)

print(f"🚀 New branch created and pushed: {branch_name}")
