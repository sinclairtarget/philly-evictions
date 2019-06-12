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
