###################### GIT PARAMETERS #####################################
export GIT_PARENT_DIR=~
export GIT_REPO_NAME=#your-repo
export GIT_BRANCH_NAME=#your-branch
export GIT_USER=#your-gituser
export GIT_EMAIL=#your-email
export GITHUB_ACCESS_TOKEN=#access-token from github developer settings

################ This is only needed if the repo is forked. ################
export GIT_USER_UPSTREAM=#original-repo-user


############################################################################
#### DO NOT EDIT BELOW THIS LINE: derived variables
############################################################################

export GIT_REMOTE_URL=git@github.com:$GIT_USER/$GIT_REPO_NAME.git
export GIT_REMOTE_URL_HTTPS=https://github.com/$GIT_USER/$GIT_REPO_NAME.git

############################## Original repo url ###########################
export GIT_REMOTE_UPSTREAM=$GIT_USER_UPSTREAM/$GIT_REPO_NAME