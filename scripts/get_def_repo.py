#!/usr/bin/python3

import sys
import requests
import json


def all_repo_rules(headers, github_url):
    url = f'{github_url}/rulesets'
    return requests.get(url, headers=headers)


def branch_rules(branch_name, headers, github_url):
    url = f'{github_url}/rules/branches/{branch_name}'
    return requests.get(url, headers=headers)


def main():
    repo_allrules = all_repo_rules(headers, url)
    print("_" * 50)
    print("retval:", repo_allrules)
    # print(json.dumps(repo_allrules.content, indent=4))
    print(repo_allrules.content)

    branch_rule = branch_rules("main", headers, url)
    print("_" * 50)
    print("retval:", branch_rule)
    # print(json.dumps(branch_rule.content, indent=4))
    print(branch_rule.content)


if __name__ == "__main__":
    TOK = sys.argv[1]
    ORG = sys.argv[2]
    REPO = sys.argv[3]
    headers = {
        "Authorization": f"Bearer {TOK}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28"
    }
    url = f'https://api.github.com/repos/{ORG}/{REPO}'

    main()
