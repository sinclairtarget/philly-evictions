def task_opendata():
    """Fetches Philadelphia Open Data Portal crimes and violations data."""
    yield pull_crimes()
    yield pull_violations()


def pull_crimes():
    target = 'data/crime_data.csv'
    script_dep = 'opendata/get_crime_data.py'
    return {
        'name': 'pull_crimes',
        'file_dep': [script_dep],
        'targets': [target],
        'actions': [
            f"python {script_dep}"
        ]
    }


def pull_violations():
    target = 'data/violations.csv'
    script_dep = 'opendata/get_violations_data.py'
    return {
        'name': 'pull_violations',
        'file_dep': [script_dep],
        'targets': [target],
        'actions': [
            f"python {script_dep}"
        ]
    }
