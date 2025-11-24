#!/usr/bin/env python3
"""
Centralized Docker Hub cleanup script.
Cleans up old Docker images for both backend and frontend repositories.
"""

import requests
import os
import sys

USERNAME = "andygrails"
REPOS = [
    "andy-grails-backend",
    "andy-grails-frontend"
]
KEEP = 10  # number of latest tags to keep
PROTECTED_TAGS = ["latest", "stable"]  # tags that should never be deleted
TOKEN = os.environ.get("DOCKER_HUB_CLEANUP_TOKEN")

if not TOKEN:
    print("❌ Error: DOCKER_HUB_CLEANUP_TOKEN environment variable is required")
    sys.exit(1)


def cleanup_repo(repo_name, headers):
    """Clean up a single Docker Hub repository."""
    print(f"\n🧹 Cleaning up {repo_name}...")

    # Step 2: Get all tags
    url = f"https://hub.docker.com/v2/repositories/{USERNAME}/{repo_name}/tags?page_size=100"
    tags = []

    while url:
        r = requests.get(url, headers=headers)
        r.raise_for_status()
        data = r.json()
        tags.extend(data["results"])
        url = data.get("next")

    if not tags:
        print(f"ℹ️  No tags found for {repo_name}")
        return

    # Step 3: Sort tags by last_updated (most recent first)
    tags.sort(key=lambda t: t["last_updated"], reverse=True)

    print(f"📊 Found {len(tags)} tags. Keeping {KEEP} latest, deleting {max(0, len(tags) - KEEP)} old tags.")

    # Step 4: Delete old tags
    deleted_count = 0
    skipped_count = 0

    for tag in tags[KEEP:]:
        tag_name = tag["name"]
        
        # Skip protected tags
        if tag_name in PROTECTED_TAGS:
            print(f"⏭️  Skipping protected tag: {tag_name}")
            skipped_count += 1
            continue

        delete_url = f"https://hub.docker.com/v2/repositories/{USERNAME}/{repo_name}/tags/{tag_name}/"
        print(f"🗑️  Deleting {repo_name}:{tag_name} ... ", end="", flush=True)
        
        try:
            del_resp = requests.delete(delete_url, headers=headers)
            if del_resp.status_code in (202, 204):
                print("✅ Deleted")
                deleted_count += 1
            else:
                print(f"⚠️  Failed ({del_resp.status_code}) {del_resp.text}")
        except Exception as e:
            print(f"❌ Error: {e}")

    print(f"✅ {repo_name} cleanup completed! Deleted: {deleted_count}, Skipped: {skipped_count}")


def main():
    """Main function to clean up all repositories."""
    print("🚀 Starting Docker Hub cleanup for all repositories...")
    print(f"📦 Repositories to clean: {', '.join(REPOS)}")
    print(f"💾 Keeping {KEEP} latest tags per repository")
    
    # Authenticate once and reuse the token for all repos
    print(f"\n🔑 Logging in to Docker Hub...")
    try:
        auth_resp = requests.post(
            "https://hub.docker.com/v2/users/login/",
            json={"username": USERNAME, "password": TOKEN},
        )
        auth_resp.raise_for_status()
        jwt_token = auth_resp.json()["token"]
        headers = {"Authorization": f"JWT {jwt_token}"}
        print("✅ Successfully authenticated")
    except Exception as e:
        print(f"❌ Failed to authenticate: {e}")
        sys.exit(1)
    
    # Clean up each repository
    for repo in REPOS:
        try:
            cleanup_repo(repo, headers)
        except Exception as e:
            print(f"❌ Error cleaning up {repo}: {e}")
            # Continue with other repos even if one fails
            continue
    
    print("\n✅ All cleanup operations completed!")


if __name__ == "__main__":
    main()

