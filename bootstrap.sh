# 1. instlal gitpython package
pip install gitpython --user

# 2. clone git repo
curl https://raw.githubusercontent.com/ksbek/githubcommit/master/config.py | python

# 3. uninstall package before install(this step is needed for updating)
pip uninstall githubcommit

# 4. install package from git
pip install git+https://github.com/ksbek/githubcommit.git --user

# 5. enable serverextension
jupyter serverextension enable --py githubcommit

# 6. uninstall nbextension before(this step is needed for updating)
jupyter nbextension uninstall --py githubcommit

# 7. install nbextension
jupyter nbextension install --py githubcommit --user

# 8. enable nbextension
jupyter nbextension enable --py githubcommit --user