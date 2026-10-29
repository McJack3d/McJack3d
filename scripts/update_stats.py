#!/usr/bin/env python3
"""Refresh public GitHub profile counts without third-party dependencies.

Only public endpoints and public, owned repositories are used. GITHUB_TOKEN
is optional and raises the API rate limit in GitHub Actions. Existing data
remains untouched if any request, validation, or pagination step fails.
"""

from datetime import datetime, timezone
import json
import os
from pathlib import Path
import sys
import tempfile
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen


USERNAME = "McJack3d"
API_ROOT = "https://api.github.com"
OUTPUT = Path(__file__).resolve().parents[1] / "data" / "stats.json"


def get_json(path):
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": f"{USERNAME}-profile-readme",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    token = os.environ.get("GITHUB_TOKEN", "").strip()
    if token:
        headers["Authorization"] = f"Bearer {token}"
    request = Request(API_ROOT + path, headers=headers)
    with urlopen(request, timeout=30) as response:
        return json.load(response)


def count(value, field):
    if type(value) is not int or value < 0:
        raise ValueError(f"Invalid nonnegative integer for {field}")
    return value


def fetch_stats():
    user = get_json(f"/users/{USERNAME}")
    if not isinstance(user, dict) or user.get("login", "").lower() != USERNAME.lower():
        raise ValueError("Unexpected GitHub user response")
    public_repos = count(user.get("public_repos"), "public_repos")
    followers = count(user.get("followers"), "followers")
    joined = datetime.strptime(user["created_at"], "%Y-%m-%dT%H:%M:%SZ").strftime("%Y")
    stars = 0
    seen = set()
    for page in range(1, 1001):
        query = urlencode({"type": "owner", "sort": "full_name", "per_page": 100, "page": page})
        repos = get_json(f"/users/{USERNAME}/repos?{query}")
        if not isinstance(repos, list):
            raise ValueError("Unexpected GitHub repository response")
        for repo in repos:
            if not isinstance(repo, dict):
                raise ValueError("Invalid repository entry")
            if repo.get("private") is not False or repo.get("visibility") != "public":
                continue
            if repo.get("owner", {}).get("login", "").lower() != USERNAME.lower():
                continue
            repo_id = count(repo.get("id"), "repository id")
            if repo_id in seen:
                raise ValueError("Repository pagination changed during refresh; retry later")
            seen.add(repo_id)
            if repo.get("fork") is False:
                stars += count(repo.get("stargazers_count"), "stargazers_count")
            elif repo.get("fork") is not True:
                raise ValueError("Missing repository fork flag")
        if len(repos) < 100:
            break
    else:
        raise ValueError("Repository pagination exceeded its safety limit")
    if len(seen) != public_repos:
        raise ValueError("Public repository count changed during refresh; retry later")
    return {
        "public_repos": public_repos,
        "stars": stars,
        "followers": followers,
        "joined": joined,
        "updated": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
    }


def write_stats(stats, destination=OUTPUT):
    destination = Path(destination)
    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w", encoding="utf-8", dir=destination.parent,
            prefix=".stats-", suffix=".json", delete=False,
        ) as handle:
            temporary = Path(handle.name)
            json.dump(stats, handle, indent=2)
            handle.write("\n")
        temporary.replace(destination)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def main():
    try:
        stats = fetch_stats()
        write_stats(stats)
    except (HTTPError, URLError, TimeoutError, OSError, ValueError, KeyError, TypeError) as error:
        print(f"Stats refresh failed; existing stats preserved: {error}", file=sys.stderr)
        return 1
    print(json.dumps(stats, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
