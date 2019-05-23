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


def task_acs_fetch():
    """Fetches ACS data for 2013 to 2016 using the fetch from API script."""
    target = 'data/acs.csv'
    dep = 'acs/fetch_from_api.py'
    return {
        'file_dep': [dep],
        'targets': [target],
        'actions': [
            f"python {dep} > {target}"
        ]
    }


def task_acs_download():
    """Downloads ACS summary files for 2009 to 2012 from Census website."""
    target = os.path.abspath('./data/acs-summary-files')
    dep = 'acs/download_summary_files.py'
    return {
        'file_dep': [dep],
        'targets': [target],
        'actions': [
            f"mkdir -p {target}",
            f"python {dep} {target}"
        ]
    }
