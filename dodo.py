import os

DOIT_CONFIG = {
    'default_tasks': ['render_proposal']
}

def task_render_proposal():
    """Generates HTML notebook output for proposal."""
    target = 'proposal/proposal.html'
    dep = 'proposal/proposal.ipynb'
    return {
        'file_dep': [dep],
        'targets': [target],
        'actions': [
            f"jupyter nbconvert --execute --to html {dep}"
        ],
        'clean': True
    }


def task_sync_proposal():
    """Generate .ipynb notebook from proposal markdown source."""
    target = 'proposal/proposal.ipynb'
    dep = 'proposal/proposal.md'
    return {
        'file_dep': [dep],
        'targets': [target],
        'actions': [
            f"jupytext --to notebook {dep}",
            f"jupytext --set-format ipynb,md --sync {target}"
        ],
        'clean': True
    }


def task_sync_analysis():
    """Generate .ipynb notebook from analysis markdown source."""
    target = 'analysis.ipynb'
    dep = 'analysis.md'
    return {
        'file_dep': [dep],
        'targets': [target],
        'actions': [
            f"jupytext --to notebook {dep}",
            f"jupytext --set-format ipynb,md --sync {target}"
        ],
        'clean': True
    }


def task_acs_pull_api():
    """Fetches ACS data for 2013 to 2016 using the fetch from API script."""
    target = 'data/acs_2013_2016.csv'
    script_dep = 'acs/fetch_from_api.py'
    variables_dep = 'acs/variables.csv'
    return {
        'file_dep': [script_dep, variables_dep],
        'targets': [target],
        'actions': [
            f"python {script_dep} > {target}"
        ]
    }


def task_acs_pull_files():
    """Extracts variables for 2009 to 2012 from ACS summary file data."""
    target = 'data/acs_2009_2012.csv'
    script_dep = 'acs/extract_variables.py'
    data_dep = 'data/acs-summary-files'
    variables_dep = 'acs/variables.csv'
    return {
        'file_dep': [script_dep, variables_dep],
        'task_dep': ['download_summary_files'],
        'targets': [target],
        'actions': [
            f"python {script_dep} {data_dep} > {target}"
        ]
    }


def task_download_summary_files():
    """Downloads ACS summary files for 2009 to 2012 from Census website."""
    target = os.path.abspath('./data/acs-summary-files')
    dep = 'acs/download_summary_files.py'
    return {
        'file_dep': [dep],
        'targets': [target],
        'uptodate': [os.path.exists(target)],
        'actions': [
            f"mkdir -p {target}",
            f"python {dep} {target}"
        ]
    }
