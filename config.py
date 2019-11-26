from git import Repo
import json

# Read config vars
with open('config.json') as json_file:
  data = json.load(json_file)
  git_dir = "{}/{}".format(data['git_parent_dir'], data['git_repo_name'])
  git_url = "git@github.com:{}/{}.git".format(data['git_user'], data['git_repo_name'])

  # Clone git repo
  try:
  	Repo.clone_from(git_url, git_dir)
  	print("Git cloning success")
  except Exception as e:
  	print(e)