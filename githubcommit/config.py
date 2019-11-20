###################### GIT PARAMETERS #####################################
GIT_PARENT_DIR="~"
GIT_REPO_NAME="#your-repo"
GIT_BRANCH_NAME="#your-branch"
GIT_USER="#your-gituser"
GIT_EMAIL="#your-email"
GITHUB_ACCESS_TOKEN="#access-token from github developer settings"

################ This is only needed if the repo is forked. ################
GIT_USER_UPSTREAM="#original-repo-user"


############################################################################
#### DO NOT EDIT BELOW THIS LINE: derived variables
############################################################################

GIT_REMOTE_URL="git@github.com:{}/{}.git".format(GIT_USER, GIT_REPO_NAME)
GIT_REMOTE_URL_HTTPS="https://github.com/{}/{}.git".format(GIT_USER, GIT_REPO_NAME)

############################## Original repo url ###########################
GIT_REMOTE_UPSTREAM="{}/{}".format(GIT_USER_UPSTREAM, GIT_REPO_NAME)