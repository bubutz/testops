#!/usr/bin/env python3

import sys
import requests


def main():
    # response = requests.get(URL, headers=headers)
    # print("--- FULL ---------------------------------------------")
    # print(response.json())
    # for branch in response.json():
    #     print("    --- BRANCHNAME -----------------------------------")
    #     if branch["name"] == new_branch_name:
    #         print("Hit ", branch["name"])
    #     else:
    #         print("Miss", branch["name"])
    # print("--- FULL ---------------------------------------------")
    for branch_name in new_branch_name:
        print(branch_name)
        url = f'https://api.github.com/repos/bubutz/testops/branches/{branch_name}/protection'
        print(url)
        response = requests.get(URL, headers=headers)
        print(response.json())
        print()


if __name__ == '__main__':
    TOK = sys.argv[1]
    URL = sys.argv[2]
    # new_branch_name = sys.argv[3]
    new_branch_name = ['foo', 'main', 'release']

    headers = {
        "Authorization": f"Bearer {TOK}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28"
    }
    main()
