import requests
import yaml
import sys
import logging

token = sys.argv[1]
repo_update_or_delete_file = sys.argv[2]

headers = {
    "Authorization": f"Bearer {token}",
    "Accept": "application/vnd.github+json",
    "X-GitHub-Api-Version": "2022-11-28",
}


def get_def_branch(org_login, repo_name):
    url = f'https://api.github.com/repos/{org_login}/{repo_name}'
    default_branch_name = requests.get(url, headers=headers)
    if default_branch_name.status_code != 200:
        print("ERROR: get_def_branch statuscode not 200")
        logging.error(default_branch_name.content)
        sys.exit(1)
    return default_branch_name.json()["default_branch"]


def validate_new_def_branch(org_login, repo_name, new_default_branch):
    url = f'https://api.github.com/repos/{org_login}/{repo_name}/branches'
    all_branches = requests.get(url, headers=headers)

    if all_branches.status_code != 200:
        print("ERROR: validate_new_def_branch all_branches statuscode not 200")
        print(all_branches.text)
        sys.exit(1)
    if new_default_branch not in [branchname["name"] for branchname in all_branches.json()]:
        print(f'ERROR: {new_default_branch} not exist in {repo_name}')
        sys.exit(1)

    url = f'https://api.github.com/repos/{org_login}/{repo_name}/rules/branches/{new_default_branch}'
    ruleset_types = requests.get(url, headers=headers)

    if ruleset_types.status_code != 200:
        print("ERROR: validate_new_def_branch ruleset_types statuscode not 200")
        print(ruleset_types.text)
        sys.exit(1)
    if "deletion" not in [ruletype["type"] for ruletype in ruleset_types.json()]:
        print(f'"{new_default_branch}" is not protected from deletion.')
        sys.exit(1)


def delete_repo(org_login, repo_name):
    url = f'https://api.github.com/repos/{org_login}/{repo_name}'
    response = requests.delete(url, headers=headers)
    if response.status_code == 204:
        print(f'SUCCESS: deleted {repo_name}')
    else:
        print("ERROR: delete_repo failed.")
        sys.exit(1)


def update_repo(org_login, repo_name, new_name, new_default_branch):
    url = f'https://api.github.com/repos/{org_login}/{repo_name}'
    data = {
        "name": new_name,
        "default_branch": new_default_branch
    }
    response = requests.patch(url, headers=headers, json=data)
    if response.status_code == 200:
        print(f'{org_login}/{repo_name} successfully updated.')
    else:
        print(f'{org_login}/{repo_name} fail to update.')
        print(response.text)
        sys.exit(1)


def main():
    org_login = repo_update_or_delete_file.split('/')[-2]

    with open(f'{repo_update_or_delete_file}') as file:
        repo_update_or_delete_data = yaml.safe_load(file)
    repo_update_or_delete_data['project_code'] = str(
        repo_update_or_delete_data.get('project_code', ''))

    repos_to_delete = repo_update_or_delete_data.get('repos_to_delete', [])
    repos_to_update = repo_update_or_delete_data.get('repos_to_update', [])
    prj_code = repo_update_or_delete_data.get('project_code', None)

    for repo in repos_to_delete:
        repo_name = repo.lower().replace(' ', '-')
        org_name = repo_update_or_delete_data.get(
            'lbu', None) if repo_update_or_delete_data.get(
            'lbu', None) else org_login.split('-')[-1]
        repo_slug = org_name + '-' + prj_code + '-' + repo_name
        repo_slug = repo_slug.lower()
        delete_repo(org_login, repo_slug)

    for repo in repos_to_update:
        repo_name = repo['name'].lower().replace(' ', '-')
        new_name = repo['new_name'].lower().replace(
            ' ', '-') if repo['new_name'] else repo_name
        org_name = repo_update_or_delete_data.get(
            'lbu', None) if repo_update_or_delete_data.get(
            'lbu', None) else org_login.split('-')[-1]
        repo_slug = f'{prj_code}{repo_name}'.lower()
        repo_new_slug = f'{prj_code}{new_name}'.lower()
        print(f'org_login {org_login}')
        print(f'repo_slug {repo_slug}')
        new_default_branch = repo['new_default_branch'] if repo['new_default_branch'] else get_def_branch(
            org_login, repo_slug)
        validate_new_def_branch(org_login, repo_slug, new_default_branch)
        update_repo(org_login, repo_slug, repo_new_slug, new_default_branch)


if __name__ == '__main__':
    main()
