import os

def task_acs():
    """Fetches and extracts ACS data."""
    yield pull_api()
    yield pull_summary_files()
    yield download_summary_files()


def pull_api():
    """Fetches ACS data for 2013 to 2016 using the fetch from API script."""
    target = 'data/acs_2013_2016.csv'
    script_dep = 'acs/fetch_from_api.py'
    variables_dep = 'acs/variables.csv'
    return {
        'name': 'pull_api',
        'file_dep': [script_dep, variables_dep],
        'targets': [target],
        'actions': [
            f"python {script_dep} > {target}"
        ]
    }


def pull_summary_files():
    """Extracts variables for 2009 to 2012 from ACS summary file data."""
    target = 'data/acs_2009_2012.csv'
    script_dep = 'acs/extract_variables.py'
    data_dep = 'data/acs-summary-files'
    variables_dep = 'acs/variables.csv'
    return {
        'name': 'pull_summary_files',
        'file_dep': [script_dep, variables_dep],
        'task_dep': ['acs:download_summary_files'],
        'targets': [target],
        'actions': [
            f"python {script_dep} {data_dep} > {target}"
        ]
    }


def download_summary_files():
    """Downloads ACS summary files for 2009 to 2012 from Census website."""
    target = os.path.abspath('./data/acs-summary-files')
    dep = 'acs/download_summary_files.py'
    return {
        'name': 'download_summary_files',
        'file_dep': [dep],
        'targets': [target],
        'uptodate': [os.path.exists(target)],
        'actions': [
            f"mkdir -p {target}",
            f"python {dep} {target}"
        ]
    }
