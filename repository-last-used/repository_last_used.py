from dataclasses import dataclass
from datetime import datetime
from requests import Session
from typing import Generator
from csv import writer
from time import sleep

try:
    import env

    EMAIL_ADDRESS = env.EMAIL_ADDRESS
    BITBUCKET_API_TOKEN = env.BITBUCKET_API_TOKEN
    WORKSPACE = env.WORKSPACE

    session = Session()
    session.auth = (EMAIL_ADDRESS, BITBUCKET_API_TOKEN)
    URL = f"https://api.bitbucket.org/2.0/repositories/{WORKSPACE}"
except [ImportError, AttributeError]:
    print(
        'Could not locate one or more attributes within the "env.py" file. '
        "Please follow the readme to ensure that all attributes are present and try again."
    )
    exit()


@dataclass
class Repo:
    name: str
    last_commit: dict


def get_last_commiter(commits_url):
    r = session.get(commits_url)
    while r.status_code == 429:
        print("Hit the API rate limit. Sleeping for 10 sec...")
        sleep(10)
        print("Resuming...")
        r = session.get(commits_url)
    r_data = r.json()
    if r_data.get("size") == 0:
        return {"date": "No Commits", "author": "No Commits"}
    else:
        commits = r_data.get("values")
        author: dict = commits[0].get("author").get("user")
        if not author:
            author = commits[0].get("author").get("raw")
        else:
            author = author.get("display_name")
        date = commits[0].get("date")[0:10].split("-")
        return {"date": f"{date[0]}/{date[1]}/{date[2]}", "author": author}


def get_repos(page=None) -> Generator[Repo, None, None]:
    while True:
        params = {"page": page, "pagelen": 100}
        r = session.get(URL, params=params)
        while r.status_code == 429:
            print("Hit the API rate limit. Sleeping for 10 sec...")
            sleep(10)
            print("Resuming...")
            r = session.get(URL, params=params)
        r_data = r.json()
        for repo in r_data.get("values"):
            commits_url = repo.get("links").get("commits").get("href")
            last_commit = get_last_commiter(commits_url)
            new_repo = Repo(repo.get("slug"), last_commit)
            yield new_repo
        if not r_data.get("next"):
            return
        if page == None:
            page = 1
        page += 1


def main():
    today = datetime.today().strftime("%Y-%m-%d_%H:%M:%S")
    with open(f"repository_last_used_{today}.csv", "x", newline="") as file:
        writer_object = writer(file)
        writer_object.writerow(["Repository", "Last Commit Date", "Last Committer"])

        for repo in get_repos():
            writer_object.writerow(
                [
                    repo.name,
                    repo.last_commit.get("date"),
                    repo.last_commit.get("author"),
                ]
            )

    print("Done!")


if __name__ == "__main__":
    main()
