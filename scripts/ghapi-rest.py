#!/usr/bin/env python3

import sys
import requests


def main():
    response = requests.get(URL, headers=headers).json()
    print(response)


if __name__ == '__main__':
    TOK = sys.argv[1]
    URL = sys.argv[2]

    headers = {
        "Authorization": f"Bearer {TOK}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28"
    }
    main()
