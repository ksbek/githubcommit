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
1. Please configure ssh key (present in ~/.ssh/id_rsa.pub or specified location) in github account first.

2. cd && curl -O https://raw.githubusercontent.com/ksbek/githubcommit/master/config.json

3. Please open config.json and set git configuration values

4. curl https://raw.githubusercontent.com/ksbek/githubcommit/master/bootstrap.py | bash

5. Restart jupyter server
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

