#!/usr/bin/env python3
"""
Centralized Docker Hub cleanup script.
Cleans up old Docker images for both backend and frontend repositories.
"""

import requests
import os

USERNAME = "andygrails"
REPOS = [
    "andy-grails-backend",
    "andy-grails-frontend"
]
KEEP = 10  # number of latest tags to keep
TOKEN = os.environ["DOCKER_HUB_CLEANUP_TOKEN"]  # personal access token

# Step 1: Log in to Docker Hub and get JWT
print("🔑 Logging in to Docker Hub...")
auth_resp = requests.post(
    "https://hub.docker.com/v2/users/login/",
    json={"username": USERNAME, "password": TOKEN},
)
auth_resp.raise_for_status()
jwt_token = auth_resp.json()["token"]
headers = {"Authorization": f"JWT {jwt_token}"}

# Step 2: Clean up each repository
for REPO in REPOS:
    print(f"\n🧹 Cleaning up {REPO}...")
    url = f"https://hub.docker.com/v2/repositories/{USERNAME}/{REPO}/tags?page_size=100"
    tags = []

    while url:
        r = requests.get(url, headers=headers)
        r.raise_for_status()
        data = r.json()
        tags.extend(data["results"])
        url = data.get("next")

    tags.sort(key=lambda t: t["last_updated"], reverse=True)

    for tag in tags[KEEP:]:
        tag_name = tag["name"]
        if tag_name in ("latest", "stable"):
            print(f"⏭️  Skipping protected tag: {tag_name}")
            continue

        delete_url = f"https://hub.docker.com/v2/repositories/{USERNAME}/{REPO}/tags/{tag_name}/"
        print(f"🗑️  Deleting {REPO}:{tag_name} ... ", end="")
        del_resp = requests.delete(delete_url, headers=headers)
        if del_resp.status_code in (202, 204):
            print("✅ Deleted")
        else:
            print(f"⚠️  Failed ({del_resp.status_code}) {del_resp.text}")

print("\n✅ Cleanup completed!")

