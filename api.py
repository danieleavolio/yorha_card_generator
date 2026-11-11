import json
import os
from urllib.request import Request, urlopen
from urllib.parse import quote

API_URL = "https://api.github.com"

def get_json(url: str) -> dict | list:
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "YoRHa-Card-Generator",
        "X-GitHub-Api-Version": "2022-11-28"
    }

    token = os.getenv("GITHUB_TOKEN")

    if token:
        headers["Authorization"] = f"Bearer {token}"

    request = Request(url, headers=headers)

    with urlopen(request, timeout=60) as response:
        return json.loads(
            response.read().decode("utf-8")
        )

def get_repositories(username: str) -> list:
    repositories = []
    page = 1

    while True:
        url = (
            f"{API_URL}/users/{quote(username)}/repos"
            f"?type=owner&per_page=100&page={page}"
        )

        result = get_json(url)

        if not result:
            break

        # Ignore forks.
        repositories.extend(
            repo for repo in result
            if not repo["fork"]
        )

        if len(result) < 100:
            break

        page += 1

    return repositories

def get_languages(username: str) -> dict:
    repositories = get_repositories(username)
    language_totals = {}

    print(f"Found {len(repositories)} repositories.")

    for index, repo in enumerate(repositories, start=1):
        full_name = quote(repo["full_name"], safe="/")

        url = f"{API_URL}/repos/{full_name}/languages"

        print(
            f"Analyzing "
            f"{index}/{len(repositories)}: "
            f"{repo['name']}"
        )

        languages = get_json(url)

        for language, size in languages.items():
            language_totals[language] = (
                language_totals.get(language, 0) + size
            )

    return language_totals
