## Disclaimer
This tool was NOT written by Atlassian developers and is considered a third-party tool. This means that this is also NOT supported by Atlassian. We highly recommend you have your team review the script before running it to ensure you understand the steps and actions taking place, as Atlassian is not responsible for the resulting configuration.

## Purpose
This script will check for all repositories within a given workspace when was the last time someone committed to this repository, the date of the last commit, and the commit author.  This will be outputed in a CSV file with the following format:

        Repository,Last Commit Date,Last Committer
        my_repo,2022/01/01,John Doe
        my_other_repo,2022/02/02,John Doe

## How to Use
Edit rename/copy the "env-template.py" file to "env.py" (as env.py is in the .gitignore) and fill it out accordingly.

Install package dependencies with the follow commands:

        $ pip3 install -r requirements.txt

Once the dependencies are satisfied and you have provided your unique details, simply run the script with Python 3.6+ and follow any prompts.

Run script with python via:

        $ python3 repository_last_used.py

