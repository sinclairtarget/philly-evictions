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


def task_fetch_acs():
    """Fetches ACS data using the fetch script."""
    target = 'data/acs.csv'
    dep = 'fetch_acs.py'
    return {
        'file_dep': [dep],
        'targets': [target],
        'actions': [
            f"python {dep} > {target}"
        ]
    }
