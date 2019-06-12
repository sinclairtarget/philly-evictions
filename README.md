# Prioritizing Tenant Legal Aid in Philadelphia
## Results
See [our training notebook](train.ipynb) for our model training process and
[our evaluation notebook](evaluation.ipynb) for our model evaluation work.

A table showing train/test set time split boundaries is available
[here](./results/time_splits/time_split_ay.csv). These splits are based on a
temporal cross-validation approach that uses cumulative training sets.

Another table showing train/test set time split boundaries is also available
[here](./results/time_splits/time_split_ly.csv). These splits are based on only
using one year for a training set.

A feature list showing features we included and wanted to include is available
[here](./results/final_feature_list.csv).

We have recorded feature importance for every year. [This
file](./results/2016/clf_feature_importance.csv) is an example.

The final list of block groups (to prioritize for intervention) is given
[here](./results/2016/clf_selected_blocks.csv).

Other files including PR curves etc. are also available for each year, for
example see [2016](./results/2016).

## Running the Project (Quick Start)
In order to run the project yourself and execute the training and evaluation
notebooks, first you will need to install the Python dependencies:
```
$ pipenv install
```

Then you will need to run all the pre-defined tasks (see below for more on
tasks):
```
$ doit
```

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
[doit](http://pydoit.org/) is a build tool / task runner. It's a handy
alternative to writing a bunch of shell scripts and its very good at creating a
pipeline where one step depends on a previous step.

To see all the tasks currently defined in the project, run:
```
(philly-evictions) $ doit list
```

To run all the necessary data gathering / augmentation steps, run:
```
(philly-evictions) $ doit merge
```

WARNING: The above task can take a while to complete, since it has to download
lots of ACS data!
