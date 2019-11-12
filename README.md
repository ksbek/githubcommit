# githubcommit

githubcommit is a jupyter notebook extension enabling users push ipython notebooks to a git repo.
The git button gets displayed in the notebook toolbar. After saving any notebook
the user can push notebook to pre-specified git repository. There are few
environment variables that must be exported. Currently this extension supports
commits to a single github repo defined in environment variable but in the long
run need help to modify this extension allowing user to select his repo and branch.

## Installation

You can currently install this directly from git:

```
pip install git+https://github.com/ksbek/githubcommit.git

jupyter serverextension enable --py githubcommit

jupyter nbextension uninstall --py githubcommit
(This command is needed when update)

jupyter nbextension install --py githubcommit
```

To enable this extension for all notebooks:

```
jupyter nbextension enable --py githubcommit
```

## Steps

* Install package using above commands
* Create Git repo where notebooks will be pushed if not already exists and clone it in your `GIT_PARENT_DIR`
* Clone this repo as well in your `GIT_PARENT_DIR` directory
* Replace the values in env.sh present in this repo itself
* Run the command - source ~/githubcommit/env.sh
* Configure ssh key (present in ~/.ssh/id_rsa.pub or specified location) in github account
* Run jupyter notebook from within your repo directory

## Example git configuration
export GIT_PARENT_DIR=~ <br />
export GIT_REPO_NAME=#your-repo <br />
export GIT_BRANCH_NAME=#your-branch <br />
export GIT_USER=#your-gituser <br />
export GIT_EMAIL=#your-email <br />
export GITHUB_ACCESS_TOKEN=#access-token from github developer settings <br />


#### This is for pull request to original repo if the current repo is forked.
export GIT_USER_UPSTREAM=#original-repo-user <br />

## Screenshots

![Extension](screens/extension.png?raw=true "Extension added to toolbar")

![Add Message](screens/add.png?raw=true "Add Message")

![Commit Message](screens/commit.png?raw=true "Commit Message")

![Push Message](screens/push.png?raw=true "Push Message")

![Pull Message](screens/pull.png?raw=true "Pull Message")

![Success Message](screens/success.png?raw=true "Success Message")

## Credits

Thanks to https://github.com/Lab41/sunny-side-up for laying the foundation of this extension.

Thanks to https://github.com/justvarshney for support.

