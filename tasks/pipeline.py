import re

def task_merge():
    """Augments evictions data with ACS and Philadephia open data."""
    target = 'data/final_merged_df.csv'
    script_dep = 'merge_data.py'
    violations_dep = 'data/violations.csv'
    crime_dep = 'data/crime_data.csv'
    acs_2012_dep = 'data/acs_2009_2012.csv'
    acs_2016_dep = 'data/acs_2013_2016.csv'

    return {
        'file_dep': [
            script_dep,
            violations_dep,
            crime_dep,
            acs_2012_dep,
            acs_2016_dep
        ],
        'targets': [target],
        'actions': [
            f"python {script_dep}"
        ]
    }


def task_train():
    """Trains models and saves results into results/ directory."""
    split_dir = 'results/time_splits'
    split_target = split_dir + '/time_split_ay.csv'

    results_dir = 'results/evaluation_results'
    clf_target = results_dir + '/clf-small-grid_ay.csv'
    reg_target = results_dir + '/reg-small-grid_ay.csv'

    data_dep = 'data/final_merged_df.csv'
    notebook_dep = 'train.ipynb'

    return {
        'file_dep': [data_dep, notebook_dep],
        'targets': [
            split_target,
            clf_target,
            reg_target
        ],
        'actions': [
            'jupyter nbconvert --execute --to html'
            f" --ExecutePreprocessor.timeout=86400 {notebook_dep}"
        ]
    }


def task_evaluate():
    """Evaluates best models."""
    notebook_dep = 'evaluation.ipynb'
    results_dir = 'results/evaluation_results'
    clf_dep = results_dir + '/clf-small-grid_ay.csv'
    reg_dep = results_dir + '/reg-small-grid_ay.csv'

    return {
        'file_dep': [clf_dep, reg_dep, notebook_dep],
        'actions': [
            'jupyter nbconvert --execute --to html'
            f" --ExecutePreprocessor.timeout=86400 {notebook_dep}"
        ]
    }
