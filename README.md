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

### Jupytext
[Jupytext](https://github.com/mwouts/jupytext) is a cool tool that allows you
to save your Jupyter notebooks as Markdown files. This is great! Notebooks are
usually saved as JSON files, which sucks, because JSON is for computers not
humans. Commit your notebooks as Markdown files and it becomes so much easier
to reason about the changes people are commiting via Git.

`.ipynb` notebook files are ignored, so when you first check out the repo you
need to generate the notebooks from the Markdown source files. To do this, run:
```
(philly-evictions) $ doit sync_proposal
```

This will generate a `.ipynb` notebook that you can edit normally using Jupyter
notebook's web interface. When you save changes they automatically get saved to
both the `.ipynb` file and the Markdown file. Git will only pick up the changes
to the Markdown file.
