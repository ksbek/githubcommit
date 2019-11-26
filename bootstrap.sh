# 1. ssh key for git
eval `ssh-agent -s` && ssh-add -k

# 2. change in jupyter config
if [ ! -f ~/.jupyter/jupyter_notebook_config.py ]; then
   jupyter notebook --generate-config
fi
echo 'c.NotebookApp.disable_check_xsrf = True' >> ~/.jupyter/jupyter_notebook_config.py

# 3 github.com host checking
curl -o ~/.ssh/config https://raw.githubusercontent.com/ksbek/githubcommit/master/config

# 4. instlal gitpython package
pip install gitpython --user

# 5. clone git repo
curl https://raw.githubusercontent.com/ksbek/githubcommit/master/config.py | python

# 6. uninstall package before install(this step is needed for updating)
pip uninstall githubcommit -y

# 7. install package from git
pip install git+https://github.com/ksbek/githubcommit.git --user

# 8. enable serverextension
jupyter serverextension enable --py githubcommit

# 9. uninstall nbextension before(this step is needed for updating)
jupyter nbextension uninstall --py githubcommit

# 10. install nbextension
jupyter nbextension install --py githubcommit --user

# 11. enable nbextension
jupyter nbextension enable --py githubcommit --user