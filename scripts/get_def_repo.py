#!/usr/bin/python3

import sys
import requests
# import json


def branch_details(headers, url):
    return requests.get(url, headers=headers)


def main():
    TOK = sys.argv[1]
    ORG = sys.argv[2]
    REPO = sys.argv[3]
    headers = {
        "Authorization": f"breaker {TOK}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28"
    }
    url = f'https://api.github.com/repos/{ORG}/{REPO}'
    repo_info = branch_details(headers, url)

    print(repo_info)


if __name__ == "__main__":
    main()
