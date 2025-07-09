#!/usr/bin/python3

import sys
import os
import requests
import json
# from glob import glob
import glob
# from pathlib import Path
# import fnmatch
import yaml


def update_repo_default_branch(org_login, repo_name, new_default_branch):
    url = f'https://api.github.com/repos/{org_login}/{repo_name}'
    data = {
        "default_branch": f"{new_default_branch}"
    }
    data = json.dumps(data)
    print("url:", url)
    print("data:", data)
    response = requests.patch(url, data=data, headers=headers)
    print(response.json())


def all_repo_rules(github_url):
    url = f'{github_url}/rulesets'
    response = requests.get(url, headers=headers)
    # response = str(response.json()).replace("'", '"')
    # return response
    return response.json()


def old_branch_rules(branch_name, headers, github_url):
    url = f'{github_url}/rules/branches/{branch_name}'
    response = requests.get(url, headers=headers)
    response = str(response.json()).replace("'", '"')
    return response


def branch_rules(url, headers):
    response = requests.get(url, headers=headers)
    # response = str(response.json()).replace("'", '"')
    return response.json()


def is_branch_protected(NEW_DEFAULT_BRANCH, protected_branch):
    os.system(f'mkdir -p {NEW_DEFAULT_BRANCH}')
    for branch in protected_branch:
        # print(branch)
        # print(fnmatch.filter(NEW_DEFAULT_BRANCH, branch))
        # Path('.').glob(branch)
        # print(branch)
        # fnmatch.filter(NEW_DEFAULT_BRANCH, branch)
        if NEW_DEFAULT_BRANCH in glob.glob(branch):
            print(branch)
            return True
    return False


def main():
    print(headers)
    url: str = 'https://api.github.com/bubutz/testops/'

    # Get all active rules
    url: str = 'https://api.github.com/bubutz/testops/rulesets'
    repo_allrules_list: list = requests.get(url, headers=headers)
    print(repo_allrules_list)

    # Get all active ruleset
    active_rulesets: list = list()
    for rule in repo_allrules_list:
        if rule["enforcement"] == "active":
            # print(rule["_links"]["self"]["href"]) # return ACTIVE ruleset url
            active_rulesets.append(branch_rules(
                rule["_links"]["self"]["href"], headers))
    print(active_rulesets)

    # Get all protected branch macroglob
    protected_branch = []
    # OLD
    for ruleset in active_rulesets:
        # print(x["rules"][0]["type"]) # return rule type is deletion
        print(ruleset)
        for rule in ruleset:
            # if ruleset["rules"][0]["type"] == "deletion":
            # print(rule)
            rule = json.loads(rule)
            if rule["type"] == "deletion":
                print(rule)
                for branch in rule["conditions"]["ref_name"]["include"]:
                    protected_branch.append(branch.replace('refs/heads/', ''))
    for ruleset in active_rulesets:
        for rule in ruleset["rules"]:
            if rule["type"] == "deletion":
                for branch in ruleset["conditions"]["ref_name"]["include"]:
                    protected_branch.append(branch.replace('refs/heads/', ''))

    # Check if glob match
    # if is_branch_protected(NEW_DEFAULT_BRANCH, protected_branch):
    #     print('lets go')
    # else:
    #     print('gtfo')


if __name__ == "__main__":
    TOK = sys.argv[1]
    headers = {
        "Authorization": f"Bearer {TOK}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28"
    }
    main()
