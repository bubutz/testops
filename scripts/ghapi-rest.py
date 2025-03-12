#!/usr/bin/env python3

import sys
import requests


def main():
    response = requests.get(URL, headers=headers)
    print("--- FULL ---------------------------------------------")
    for branch in response.json():
        print(branch)
        print("    --- BRANCHNAME -----------------------------------")
        if branch["name"] == new_branch_name:
            print("Hit ", branch["name"])
        else:
            print("Miss", branch["name"])
    # print("--- FULL ---------------------------------------------")


if __name__ == '__main__':
    TOK = sys.argv[1]
    URL = sys.argv[2]
    new_branch_name = sys.argv[3]

    headers = {
        "Authorization": f"Bearer {TOK}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28"
    }
    main()
