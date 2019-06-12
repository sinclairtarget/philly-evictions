# Prioritizing Tenant Legal Aid in Philadelphia
## Project Setup
### Pipenv
The project's Python dependencies are managed by
[pipenv](https://github.com/pypa/pipenv). The dependencies are specified in a
file called [Pipfile](Pipfile).

If you do not already have pipenv installed, you can install it using pip:
```
$ pip install pipenv
```

Once you have installed pipenv, you can install all of the dependencies for
this project in one go:
```
$ pipenv install
```

This will install the project's Python dependencies into a virtual environment.
By default, this environment will be stored under your home directory, but you
can tell pipenv to store the virtual environment locally in the project by
setting the `PIPENV_VENV_IN_PROJECT` environment variable in your
`.bash_profile`:
```
$ export PIPENV_VENV_IN_PROJECT=1
```

In order to run any executables installed by pipenv, there are two options:

#### Option One: Prefix Commands
You can prefix every executable invocation with `pipenv run`. To run `jupyter
notebook`, for example, you would instead run:
```
$ pipenv run jupyter notebook
```

This makes sure that the version of Jupyter installed by pipenv is the version
actually run.

#### Option Two: Pipenv Shell
If prefixing every executable invocation gets annoying, you can instead run
this command:
```
$ pipenv shell
```

This drops you into a sub-shell that is automatically configured to run the
proper executables. So once you are in this sub-shell you can just run, for
example:
```
(philly-evictions) $ jupyter notebook
```

This automatically runs the correct version of Jupyter.

### Doit
[doit](http://pydoit.org/) is a built tool / task runner. It's a handy
alternative to writing a bunch of shell scripts and its very good at creating a
pipeline where one step depends on a previous step.

To see all the tasks currently defined in the project, run:
```
(philly-evictions) $ doit list
```

## Downloading ACS Data
You can download ACS data using two separate doit tasks.

If you run `doit acs_pull_api`, you will download ACS data for 2013 to 2016
from the Census API.

If you run `doit acs_pull_files`, you will download ACS summary files and
extract variables from them for 2009 to 2012. Downloading the ACS summary files
can take a while.

You can edit [this variable list](./acs/variables.csv) to control what ACS
variables get downloaded.
