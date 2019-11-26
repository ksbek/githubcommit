from git import Repo
import json, os
from subprocess import check_output

# Read config vars
with open('config.json') as json_file:
  data = json.load(json_file)
  git_dir = "{}/{}".format(data['git_parent_dir'], data['git_repo_name']).replace('~', os.getcwd())
  git_url = "git@github.com:{}/{}.git".format(data['git_user'], data['git_repo_name'])

  # Clone git repo
  try:
    Repo.clone_from(git_url, git_dir)
    print("Git cloning success")
  except Exception as e:
    print(e)

  # Set git global configuration
  try:
    check_output(['git','config','--global', 'user.name', data['git_user']]).strip()
    check_output(['git','config','--global', 'user.email', data['git_email']]).strip()
    print("Git configuration success")
  except Exception as e:
    print(e)