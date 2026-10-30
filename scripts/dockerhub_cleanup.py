"""Delete stale image tags from Docker Hub.

For every repository the script keeps the KEEP most recently pushed tags and,
on top of that, every tag whose revision is referenced by one of the last
PARENT_HISTORY commits of this (parent) repository. Production is deployed by
checking out a parent revision, so those tags are exactly the images needed to
re-pull the current deployment or to roll back to a recent one.
"""

import os
import subprocess

import requests

USERNAME = "andygrails"
# Docker Hub repository -> path of the corresponding submodule in this repository.
REPOS = {
    "andy-grails-backend": "andy.grails.backend",
    "andy-grails-frontend": "andy.grails.frontend",
}
KEEP = 10  # most recently pushed tags to keep per repository
PARENT_HISTORY = 30  # parent commits whose submodule revisions stay pullable
ALWAYS_PROTECTED = {"latest", "stable"}
HUB = "https://hub.docker.com/v2"


def git(*args, cwd=None):
    return subprocess.run(
        ["git", *args], cwd=cwd, check=True, capture_output=True, text=True
    ).stdout


def protected_revisions(submodules, history=PARENT_HISTORY, cwd=None):
    """Short revisions of each submodule referenced by the last `history` commits.

    Returns a dict mapping every submodule path to the set of revisions it was
    checked out at in those commits, shortened to the 7 characters CI uses as
    image tags.
    """
    revisions = {path: set() for path in submodules}
    for commit in git("rev-list", "-n", str(history), "HEAD", cwd=cwd).split():
        for line in git("ls-tree", commit, "--", *submodules, cwd=cwd).splitlines():
            _mode, _type, sha, path = line.split(maxsplit=3)
            revisions[path].add(sha[:7])
    return revisions


def tags_to_delete(tags, keep, protected):
    """Names of the tags that are neither among the `keep` newest nor protected."""
    newest_first = sorted(tags, key=lambda t: t["last_updated"], reverse=True)
    return [t["name"] for t in newest_first[keep:] if t["name"] not in protected]


def login(token):
    resp = requests.post(f"{HUB}/users/login/", json={"username": USERNAME, "password": token})
    resp.raise_for_status()
    return {"Authorization": f"JWT {resp.json()['token']}"}


def fetch_tags(repo, headers):
    url = f"{HUB}/repositories/{USERNAME}/{repo}/tags?page_size=100"
    tags = []
    while url:
        resp = requests.get(url, headers=headers)
        resp.raise_for_status()
        data = resp.json()
        tags.extend(data["results"])
        url = data.get("next")
    return tags


def delete_tag(repo, tag, headers):
    resp = requests.delete(f"{HUB}/repositories/{USERNAME}/{repo}/tags/{tag}/", headers=headers)
    return resp.status_code in (202, 204), resp


def main():
    token = os.environ["DOCKER_HUB_CLEANUP_TOKEN"]  # personal access token

    print("🔑 Logging in to Docker Hub...")
    headers = login(token)

    print(f"📜 Reading submodule revisions of the last {PARENT_HISTORY} parent commits...")
    deployable = protected_revisions(list(REPOS.values()))

    for repo, submodule in REPOS.items():
        print(f"🧹 Cleaning up {repo}...")
        protected = ALWAYS_PROTECTED | deployable[submodule]
        print(f"🛡️  Protected tags: {', '.join(sorted(protected))}")

        for tag in tags_to_delete(fetch_tags(repo, headers), KEEP, protected):
            print(f"🗑️  Deleting {repo}:{tag} ... ", end="")
            deleted, resp = delete_tag(repo, tag, headers)
            if deleted:
                print("✅ Deleted")
            else:
                print(f"⚠️  Failed ({resp.status_code}) {resp.text}")

    print("✅ Cleanup completed!")


if __name__ == "__main__":
    main()
