"""GitHub Profile Analyzer: profile summary and a chart of languages across a user's repositories."""
import os

import matplotlib.pyplot as plt
import requests

API = "https://api.github.com"
TIMEOUT = 15  # seconds


def _headers():
    """Use GITHUB_TOKEN if set: raises the rate limit from 60 to 5,000 requests per hour."""
    headers = {"Accept": "application/vnd.github+json"}
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return headers


def fetch_github_data(username):
    try:
        response = requests.get(f"{API}/users/{username}", headers=_headers(), timeout=TIMEOUT)
    except requests.RequestException as exc:
        print(f"Network error: {exc}")
        return None
    if response.status_code == 200:
        return response.json()
    if response.status_code == 404:
        print(f"User '{username}' not found.")
    elif response.status_code == 403:
        print("Rate limit reached. Set GITHUB_TOKEN to raise the limit.")
    else:
        print(f"Error fetching data (HTTP {response.status_code}).")
    return None


def fetch_repos(username):
    """Fetch all public repositories, following pagination 100 at a time."""
    repos, page = [], 1
    while True:
        try:
            response = requests.get(f"{API}/users/{username}/repos",
                                    params={"per_page": 100, "page": page},
                                    headers=_headers(), timeout=TIMEOUT)
        except requests.RequestException as exc:
            print(f"Network error: {exc}")
            break
        if response.status_code != 200:
            break
        batch = response.json()
        repos.extend(batch)
        if len(batch) < 100:
            break
        page += 1
    return repos


def count_languages(repos):
    languages = {}
    for repo in repos:
        lang = repo.get("language")
        if lang:
            languages[lang] = languages.get(lang, 0) + 1
    return dict(sorted(languages.items(), key=lambda kv: kv[1], reverse=True))


def analyze_repos(repos):
    languages = count_languages(repos)
    if not languages:
        print("No languages found in repositories.")
        return
    print("\nRepositories by primary language:")
    for lang, n in languages.items():
        print(f"  {lang:<15} {n}")
    plt.figure(figsize=(8, 5))
    plt.bar(languages.keys(), languages.values(), color="skyblue")
    plt.xlabel("Programming Languages")
    plt.ylabel("Number of Repositories")
    plt.title("GitHub Repositories by Language")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


def main():
    username = input("Enter GitHub username: ").strip()
    user_data = fetch_github_data(username)
    if user_data:
        print(f"\nGitHub Profile Summary for {username}")
        print(f"Name: {user_data.get('name') or 'N/A'}")
        print(f"Public Repos: {user_data.get('public_repos')}")
        print(f"Followers: {user_data.get('followers')}")
        print(f"Following: {user_data.get('following')}")
        print(f"Profile URL: {user_data.get('html_url')}")

        repos = fetch_repos(username)
        analyze_repos(repos)


if __name__ == "__main__":
    main()
