import requests
import json
import matplotlib.pyplot as plt
import pandas as pd


def fetch_github_data(username):
    url = f"https://api.github.com/users/{username}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print("Error fetching data. Check username or API rate limit.")
        return None


def fetch_repos(username):
    url = f"https://api.github.com/users/{username}/repos?per_page=100"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return []


def analyze_repos(repos):
    languages = {}
    for repo in repos:
        lang = repo.get("language")
        if lang:
            languages[lang] = languages.get(lang, 0) + 1

    if languages:
        plt.figure(figsize=(8, 5))
        plt.bar(languages.keys(), languages.values(), color='skyblue')
        plt.xlabel("Programming Languages")
        plt.ylabel("Number of Repositories")
        plt.title("GitHub Repositories by Language")
        plt.xticks(rotation=45)
        plt.show()
    else:
        print("No languages found in repositories.")


def main():
    username = input("Enter GitHub username: ")
    user_data = fetch_github_data(username)
    if user_data:
        print(f"\nGitHub Profile Summary for {username}")
        print(f"Name: {user_data.get('name', 'N/A')}")
        print(f"Public Repos: {user_data.get('public_repos')}")
        print(f"Followers: {user_data.get('followers')}")
        print(f"Following: {user_data.get('following')}")
        print(f"Profile URL: {user_data.get('html_url')}")

        repos = fetch_repos(username)
        analyze_repos(repos)


if __name__ == "__main__":
    main()
