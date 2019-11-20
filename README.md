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
1. pip uninstall githubcommit

2. git clone https://github.com/ksbek/githubcommit.git

3. cd githubcommit

4. Please open config.sh file and set env variables

5. source env.sh

6. cd {REPO INSTALLATION FOLDER}/githubcommit

7. Please open config.py file and set git env variables

8. cd {REPO INSTALLATION FOLDER}

9. pip install .

10. jupyter serverextension enable --py githubcommit

11. jupyter nbextension uninstall --py githubcommit

12. jupyter nbextension install --py githubcommit

13. jupyter nbextension enable --py githubcommit
```


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

