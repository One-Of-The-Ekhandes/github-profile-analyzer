# GitHub Profile Analyzer

A Python command-line tool that fetches a GitHub user's profile and public repositories through the GitHub REST API, prints a summary, and charts the programming languages used across their repositories.

## Features

- Profile summary: name, public repositories, followers, following, profile URL
- Fetches **all** public repositories, following pagination 100 at a time
- Counts repositories by primary language, prints the table and draws a bar chart (matplotlib)
- Clear messages for unknown users, rate limits and network errors, with request timeouts
- Optional `GITHUB_TOKEN` to raise the API rate limit from 60 to 5,000 requests per hour

## Installation

```bash
git clone https://github.com/One-Of-The-Ekhandes/github-profile-analyzer.git
cd github-profile-analyzer
pip install -r requirements.txt
```

## Usage

```bash
python main.py
# Enter GitHub username: octocat
```

Optional, for higher rate limits:

```bash
export GITHUB_TOKEN=your_token      # Windows PowerShell: $env:GITHUB_TOKEN="your_token"
python main.py
```

## Example output

```text
GitHub Profile Summary for octocat
Name: The Octocat
Public Repos: 8
Followers: ...
Following: ...
Profile URL: https://github.com/octocat

Repositories by primary language:
  ...
```

A window then shows the bar chart of repositories per language.

## How it works

- `fetch_github_data()` calls `GET /users/{username}`.
- `fetch_repos()` calls `GET /users/{username}/repos?per_page=100&page=N` until a page has fewer than 100 results.
- `count_languages()` counts each repository's primary language and sorts the result.
- `analyze_repos()` prints the counts and plots them.

## Future enhancements

- Commit activity over time
- Starred repositories and insights
- Contribution heatmap

## License

MIT
