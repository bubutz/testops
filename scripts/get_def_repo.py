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


def validate_branches(org_login, target_repo, NEW_DEFAULT_BRANCH):
    url = f'https://api.github.com/repos/{org_login}/{target_repo}/branches'
    response = requests.get(url, headers=headers)
    # print("NEW_DEFAULT_BRANCH:", NEW_DEFAULT_BRANCH)
    # print()
    for branch in response.json():
        # print("name:", branch["name"])
        # print("protected:", branch["protected"])
        if branch["name"] == NEW_DEFAULT_BRANCH:
            # print("hit name:", branch["name"])
            if branch["protected"]:
                # print("protected:", branch["protected"])
                print("New default branch:", NEW_DEFAULT_BRANCH, "is protected.")
                return True
    print("New default branch:", NEW_DEFAULT_BRANCH,
          "doesn't exist or is not protected.")
    return False


def validate(org_login, target_repo, new_default_branch):
    if not validate_branches(org_login, target_repo, new_default_branch):
        print('fail')
    else:
        print('OK')


def update_repo_default_branch(org_login, repo_name, new_default_branch):
    url = f'https://api.github.com/repos/{org_login}/{repo_name}'
    data = {"name": f"{repo_name}", "default_branch": f"{new_default_branch}"}
    data = json.dumps(data)
    print("url:", url)
    print("data:", data)
    response = requests.patch(url, data=json.dumps(data), headers=headers)
    print(response.json())

# def all_repo_rules(github_url):
#     url = f'{github_url}/rulesets'
#     response = requests.get(url, headers=headers)
#     # response = str(response.json()).replace("'", '"')
#     # return response
#     return response.json()
#
#
# def old_branch_rules(branch_name, headers, github_url):
#     url = f'{github_url}/rules/branches/{branch_name}'
#     response = requests.get(url, headers=headers)
#     response = str(response.json()).replace("'", '"')
#     return response
#
#
# def branch_rules(url, headers):
#     response = requests.get(url, headers=headers)
#     # response = str(response.json()).replace("'", '"')
#     return response.json()
#
#
# def is_branch_protected(NEW_DEFAULT_BRANCH, protected_branch):
#     os.system(f'mkdir -p {NEW_DEFAULT_BRANCH}')
#     for branch in protected_branch:
#         # print(branch)
#         # print(fnmatch.filter(NEW_DEFAULT_BRANCH, branch))
#         # Path('.').glob(branch)
#         # print(branch)
#         # fnmatch.filter(NEW_DEFAULT_BRANCH, branch)
#         if NEW_DEFAULT_BRANCH in glob.glob(branch):
#             print(branch)
#             return True
#     return False


def main():
    # repo_allrules_list = all_repo_rules(url)
    # print("_" * 50)
    # print(repo_allrules_list)
    # active_rulesets = []
    # for rule in repo_allrules_list:
    #     if rule["enforcement"] == "active":
    #         # print(x["_links"]["self"]["href"]) # return ACTIVE rulesets url
    #         active_rulesets.append(branch_rules(
    #             rule["_links"]["self"]["href"], headers))
    #
    # protected_branch = []
    # OLD
    # for ruleset in active_rulesets:
    #     # print(x["rules"][0]["type"]) # return rule type is deletion
    #     for rule in ruleset:
    #         # if ruleset["rules"][0]["type"] == "deletion":
    #         # print(rule)
    #         rule = json.loads(rule)
    #         if rule["type"] == "deletion":
    #             print(rule)
    #             for branch in rule["conditions"]["ref_name"]["include"]:
    #                 protected_branch.append(branch.replace('refs/heads/', ''))
    #
    # for ruleset in active_rulesets:
    #     for rule in ruleset["rules"]:
    #         if rule["type"] == "deletion":
    #             for branch in ruleset["conditions"]["ref_name"]["include"]:
    #                 protected_branch.append(branch.replace('refs/heads/', ''))
    #
    # if is_branch_protected(NEW_DEFAULT_BRANCH, protected_branch):
    #     print('lets go')
    # else:
    #     print('gtfo')
    #
    # validate(ORG, REPO)

    org_login = ORG
    with open(src_yml, 'r') as file:
        update_repo_default_branch = yaml.safe_load(file)

    target_repo = update_repo_default_branch.get('repo', None)
    print("target_repo:", target_repo)

    prj_code = update_repo_default_branch.get('project_code', None)
    print("prj_code:", prj_code)

    repo_name = f'{prj_code}{target_repo}'
    print("repo_name:", repo_name, type(repo_name))
    new_default_branch = update_repo_default_branch.get(
        'new_default_branch', None)

    print("ORG:", ORG, type(ORG))
    validate(ORG, repo_name, new_default_branch)

    data = {"default_branch": f"{new_default_branch}"}
    print("data:", data, type(data))
    data = json.dumps(data)
    print("data:", data, type(data))
    data = json.loads(data)
    print("data:", data, type(data))

    # update_repo_default_branch(ORG, repo_name, new_default_branch)
    update_repo_default_branch(ORG, repo_name, new_default_branch)


if __name__ == "__main__":
    TOK = sys.argv[1]
    ORG = 'bubutz'
    # REPO = 'testops'
    # NEW_DEFAULT_BRANCH = 'release/abc/def/ghiaaa'
    # NEW_DEFAULT_BRANCH = 'main'
    # src_yml = './get_def_repo.yml'
    src_yml = sys.argv[2]
    headers = {
        "Authorization": f"Bearer {TOK}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28"
    }
    # url = f'https://api.github.com/repos/{ORG}/{REPO}'
    main()
