#!/usr/bin/python3

import sys
import requests
import json
import pprint


def all_repo_rules(headers, github_url):
    url = f'{github_url}/rulesets'
    return requests.get(url, headers=headers)


def branch_rules(branch_name, headers, github_url):
    url = f'{github_url}/rules/branches/{branch_name}'
    return requests.get(url, headers=headers)


def main():
    response = all_repo_rules(headers, url)
    repo_allrules = response.json()
    print("_" * 50)
    print("retval:", repo_allrules)
    print(json.dumps(repo_allrules.content, indent=4))
    pprint.pprint(repo_allrules.content, compact=True, indent=4)

    response = branch_rules("main", headers, url)
    branch_rule = response.json()
    print("_" * 50)
    print("retval:", branch_rule)
    print(json.dumps(branch_rule.content, indent=4))
    pprint.pprint(branch_rule.content, indent=4)


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
