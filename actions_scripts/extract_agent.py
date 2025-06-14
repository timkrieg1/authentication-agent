import json
import random
import string
from datetime import datetime
import os
import requests

def random_string(length=8):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def create_random_json_file():
    data = {
        "id": random.randint(1, 1000),
        "name": random_string(12),
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "values": [random.random() for _ in range(5)]
    }

    os.makedirs("output", exist_ok=True)
    filename = f"output/random_data_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.json"
    with open(filename, "w") as f:
        json.dump(data, f, indent=2)

    print(f"Created file: {filename}")

if __name__ == "__main__":
    create_random_json_file()
