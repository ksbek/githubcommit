from notebook.utils import url_path_join as ujoin
from notebook.base.handlers import IPythonHandler
import os, json, git, urllib, requests
from git import Repo, GitCommandError
from subprocess import check_output
import subprocess
import sys

def get_status(repo, path):
    changed = [ item.a_path for item in repo.index.diff(None) ]
    if path in repo.untracked_files:
        return 'untracked'
    elif path in changed:
        return 'modified'
    else:
        return 'nothing'

class GitBaseHandler(IPythonHandler):

    def get_git_vars(self):

        # Read git config variables from ~/config.json
        cwd = os.getcwd()
        json_file = open(cwd + '/config.json')
        data = json.load(json_file)

        git_parent_dir = data['git_parent_dir'].replace('~', cwd)
        git_dir = "{}/{}".format(git_parent_dir, data['git_repo_name'])
        git_repo_name = data['git_repo_name']
        git_url = "git@github.com:{}/{}.git".format(data['git_user'], data['git_repo_name'])
        git_user = data['git_user']
        git_branch = data['git_branch']
        git_remote = data['git_remote']

        return git_dir, git_repo_name, git_url, git_user, git_branch, git_remote

    def error_and_return(self, dirname, reason):

        # send error
        # self.send_error(500, reason=reason)
        self.write({'status': 500, 'statusText': reason})
        # return to directory
        os.chdir(dirname)


class GitAddHandler(GitBaseHandler):

    def put(self):
        try:
            git_dir, git_repo_name, git_url, git_user, git_branch, git_remote = self.get_git_vars()

            # obtain filename and msg for add
            data = json.loads(self.request.body.decode('utf-8'))
            filename = urllib.parse.unquote(data['filename']).replace('/' + git_repo_name, '')

            # get current directory (to return later)
            cwd = os.getcwd()

            # select branch within repo
            try:
                os.chdir(git_dir)
                dir_repo = check_output(['git','rev-parse','--show-toplevel']).strip()
                repo = Repo(dir_repo.decode('utf8'))
            except GitCommandError as e:
                self.error_and_return(cwd, "Could not checkout repo: {}".format(dir_repo))
                return

            # create new branch
            try:
                print(repo.git.checkout('HEAD', b=git_branch))
            except GitCommandError:
                print("Switching to {}".format(repo.heads[git_branch].checkout()))

            if get_status(repo, filename[1:]) == 'nothing':
                self.error_and_return(cwd, "There's no changes on this notbook. Did you save it after you made change?")
                return

            # commit current notebook
            # client will sent pathname containing git directory; append to git directory's parent
            try:
                subprocess.run(['jupyter', 'nbconvert', '--to', 'script', str(git_dir + filename)])
                src_filename = filename.replace('ipynb', 'py')

                print(repo.git.add(git_dir + filename))
                print(repo.git.add(git_dir + src_filename))

            except GitCommandError as e:
                print(e)
                self.error_and_return(cwd, "Could not add changes to notebook {}: {}".format(filename, str(e)))
                return

            # return to directory
            os.chdir(cwd)

            # close connection
            self.write({'status': 200, 'statusText': 'Success!  Add {} to branch {} at {}'.format(filename, git_branch, git_url)})

        except Exception as e:
            f = open("{}/logs.txt".format(os.getcwd()), "a")
            f.write("\nGIT ADD ERROR: \n")
            f.write(str(e) + "\n")
            f.close()


class GitCommitHandler(GitBaseHandler):

    def put(self):
        try:
            git_dir, git_repo_name, git_url, git_user, git_branch, git_remote = self.get_git_vars()

            # obtain filename and msg for commit
            data = json.loads(self.request.body.decode('utf-8'))
            filename = urllib.parse.unquote(data['filename']).replace('/' + git_repo_name, '')
            msg = data['msg']


            # get current directory (to return later)
            cwd = os.getcwd()

            # select branch within repo
            try:
                os.chdir(git_dir)
                dir_repo = check_output(['git','rev-parse','--show-toplevel']).strip()
                repo = Repo(dir_repo.decode('utf8'))
            except GitCommandError as e:
                self.error_and_return(cwd, "Could not checkout repo: {}".format(dir_repo))
                return

            # create new branch
            try:
                print(repo.git.checkout('HEAD', b=git_branch))
            except GitCommandError:
                print("Switching to {}".format(repo.heads[git_branch].checkout()))

            if not repo.index.diff("HEAD"):
                self.error_and_return(cwd, "There are no staged files to commit.")
                return

            # commit current notebook
            # client will sent pathname containing git directory; append to git directory's parent
            try:
                print(repo.git.commit( a=False, m="{}\n\nUpdated {}".format(msg, filename) ))

            except GitCommandError as e:
                print(e)
                self.error_and_return(cwd, "Could not commit changes to notebook {}: {}".format(filename, str(e)))
                return

            # return to directory
            os.chdir(cwd)

            # close connection
            self.write({'status': 200, 'statusText': 'Success!  Commit {} on branch {} at {}'.format(filename, git_branch, git_url)})

        except Exception as e:
            f = open("{}/logs.txt".format(os.getcwd()), "a")
            f.write("\nGIT COMMIT ERROR: \n")
            f.write(str(e) + "\n")
            f.close()


class GitPushHandler(GitBaseHandler):

    def put(self):
        try:
            git_dir, git_repo_name, git_url, git_user, git_branch, git_remote = self.get_git_vars()

            # obtain force arg for push
            data = json.loads(self.request.body.decode('utf-8'))
            force_push = data['force']

            # get current directory (to return later)
            cwd = os.getcwd()

            # select branch within repo
            try:
                os.chdir(git_dir)
                dir_repo = check_output(['git','rev-parse','--show-toplevel']).strip()
                repo = Repo(dir_repo.decode('utf8'))
            except GitCommandError as e:
                self.error_and_return(cwd, "Could not checkout repo {}: {}".format(dir_repo, str(e)))
                return

            # create new branch
            try:
                print(repo.git.checkout('HEAD', b=git_branch))
            except GitCommandError:
                print("Switching to {}".format(repo.heads[git_branch].checkout()))


            # create or switch to remote
            try:
                remote = repo.create_remote(git_remote, git_url)
            except GitCommandError:
                print("Remote {} already exists...".format(git_remote))
                remote = repo.remote(git_remote)

            # push changes
            try:
                pushed = remote.push(git_branch, force=force_push==True)
                assert len(pushed)>0
                assert pushed[0].flags in [git.remote.PushInfo.UP_TO_DATE, git.remote.PushInfo.FAST_FORWARD, git.remote.PushInfo.NEW_HEAD, git.remote.PushInfo.NEW_TAG]
            except GitCommandError as e:
                print(e)
                self.error_and_return(cwd, "Could not push to remote {}: {}".format(git_remote, str(e)))
                return
            except AssertionError as e:
                self.error_and_return(cwd, "Could not push to remote {}: {}".format(git_remote, pushed[0].summary))
                return

            # return to directory
            os.chdir(cwd)

            # close connection
            self.write({'status': 200, 'statusText': 'Success!  Pushed to branch {} at {}'.format(git_branch, git_url)})

        except Exception as e:
            f = open("{}/logs.txt".format(os.getcwd()), "a")
            f.write("\nGIT PUSH ERROR: \n")
            f.write(str(e) + "\n")
            f.close()

class GitPullHandler(GitBaseHandler):

    def post(self):
        try:
            git_dir, git_repo_name, git_url, git_user, git_branch, git_remote = self.get_git_vars()

            # obtain force arg for pull
            data = json.loads(self.request.body.decode('utf-8'))
            # force_pull = data['force']

            # get current directory (to return later)
            cwd = os.getcwd()

            # select branch within repo
            try:
                os.chdir(git_dir)
                dir_repo = check_output(['git','rev-parse','--show-toplevel']).strip()
                repo = Repo(dir_repo.decode('utf8'))
            except GitCommandError as e:
                self.error_and_return(cwd, "Could not checkout repo {}: {}".format(dir_repo, str(e)))
                return

            # create new branch
            try:
                print(repo.git.checkout('HEAD', b=git_branch))
            except GitCommandError:
                print("Switching to {}".format(repo.heads[git_branch].checkout()))


            # create or switch to remote
            try:
                remote = repo.create_remote(git_remote, git_url)
            except GitCommandError:
                print("Remote {} already exists...".format(git_remote))
                remote = repo.remote(git_remote)

            # pull changes
            try:
                pulled = remote.pull(git_branch)
                assert len(pulled)>0
            except Exception as e:
                print(e)
                self.error_and_return(cwd, "Could not pull from remote {}: {}".format(git_remote, str(e)))
                return
            except AssertionError as e:
                self.error_and_return(cwd, "Could not pull from remote {}: {}".format(git_remote, pulled[0].summary))
                return

            # return to directory
            os.chdir(cwd)

            # close connection
            self.write({'status': 200, 'statusText': 'Success!  Pull from {} at {}'.format(git_branch, git_url)})

        except Exception as e:
            f = open("{}/logs.txt".format(os.getcwd()), "a")
            f.write("\nGIT PULL ERROR: \n")
            f.write(str(e) + "\n")
            f.close()

def setup_handlers(nbapp):
    route_pattern = ujoin(nbapp.settings['base_url'], '/git/add')
    nbapp.add_handlers('.*', [(route_pattern, GitAddHandler)])

    route_pattern = ujoin(nbapp.settings['base_url'], '/git/commit')
    nbapp.add_handlers('.*', [(route_pattern, GitCommitHandler)])

    route_pattern = ujoin(nbapp.settings['base_url'], '/git/push')
    nbapp.add_handlers('.*', [(route_pattern, GitPushHandler)])

    route_pattern = ujoin(nbapp.settings['base_url'], '/git/pull')
    nbapp.add_handlers('.*', [(route_pattern, GitPullHandler)])

