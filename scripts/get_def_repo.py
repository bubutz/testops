#!/usr/bin/python3

import sys
import requests
import json


def all_repo_rules(headers):
    url = f'https://api.github.com/repos/{ORG}/{REPO}/rulesets'
    return requests.get(url, headers=headers)

def branch_rules(branch_name, headers):
    url = f'https://api.github.com/repos/{ORG}/{REPO}/rules/branches/{branch_name}'
    return requests.get(url, headers=headers)

def main():
    TOK = sys.argv[1]
    ORG = sys.argv[2]
    REPO = sys.argv[3]
    headers = {
        "Authorization": f"Bearer {TOK}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28"
    }
    repo_allrules = all_repo_rules(headers)

    # print("retval:", repo_info)
    print("_" * 50)
    print(json.dumps(repo_info.content, indent=4))


    branch_rule = branch_rules("main", headers)
    print("_" * 50)
    print(json.dumps(branch_rule.content, indent=4))

if __name__ == "__main__":
    main()
