"""
Extracts variables we want from the ACS summary files.
"""
import numpy as np
import pandas as pd
import sys
import re

from summary_file_directory import SummaryFileDirectory
from variable_list import VariableList

YEARS = range(2009, 2013)

GEO_COL_NAMES = [
    'FILEID', 'STUSAB', 'SUMLEVEL', 'COMPONENT', 'LOGRECNO', 'US', 'REGION',
    'DIVISION', 'STATECE', 'STATE', 'COUNTY', 'COUSUB', 'PLACE', 'TRACT',
    'BLKGRP', 'CONCIT', 'AIANHH', 'AIANHHFP', 'AIHHTLI', 'AITSCE', 'AITS',
    'ANRC', 'CBSA', 'CSA', 'METDIV', 'MACC', 'MEMI', 'NECTA', 'CNECTA',
    'NECTADIV', 'UA', 'BLANK0', 'CDCURR', 'SLDU', 'SLDL', 'BLANK1', 'BLANK2',
    'ZCTA5', 'SUBMCD', 'SDELM', 'SDSEC', 'SDUNI', 'UR', 'PCI', 'BLANK3',
    'BLANK4', 'PUMA5', 'BLANK5', 'GEOID', 'NAME', 'BTTR', 'BTBG', 'BLANK6'
]

GEO_COL_WIDTHS = [
    6, 2, 3, 2, 7, 1, 1, 1, 2, 2, 3, 5, 5, 6, 1, 5, 4, 5, 1, 3, 5, 5, 5, 3, 5,
    1, 1, 5, 3, 5, 5, 5, 2, 3, 3, 6, 3, 5, 5, 5, 5, 5, 1, 1, 6, 5, 5, 5, 40,
    1000, 6, 1, 44
]

ESTIMATE_COL_NAMES = [
    'FILEID',
    'FILETYPE',
    'STUSAB',
    'CHARITER',
    'SEQUENCE',
    'LOGRECNO'
]

variable_list = VariableList()

def clean_sequence_lookup(df, year):
    if year == 2011:
        # Column names differ in this year for some reason
        df = df.rename(columns={
            'Table ID': 'table_id',
            'seq': 'sequence_number',
            'Line Number Decimal M Lines': 'line_number',
            'position': 'start_position',
            'cells': 'total_cells'
        })
    else:
        df = df.rename(columns={
            'Table ID': 'table_id',
            'Sequence Number': 'sequence_number',
            'Start Position': 'start_position',
            'Total Cells in Table': 'total_cells'
        })

    df = df[['table_id', 'sequence_number', 'start_position',
             'total_cells']]

    # Get rows with start positions
    df = df[df.start_position.notnull()]
    df = df[df.start_position.map(lambda x: len(str(x).strip()) > 0)]
    df = df[df.start_position.map(lambda x: str(x).strip() != '.')]

    # Get only the variables we care about
    df = df[df.table_id.isin(variable_list.acs_tables())]

    # Add full variable name column
    df_vars = pd.DataFrame(data={
        'fullname': variable_list.acs_variables()
    })

    df_vars['table_id'] = \
        df_vars.fullname.map(lambda x: VariableList.table(x))

    df = pd.merge(df, df_vars, how='left', on='table_id')

    # Fix types
    df = df.astype({
        'sequence_number': int,
        'start_position': int
    })

    return df


def clean_geo(df, year):
    # We only want block groups
    df = df[(df.SUMLEVEL == 150) & (df.COUNTY == 101)]

    # Get columns we care about
    df = df[['LOGRECNO', 'TRACT', 'BLKGRP', 'GEOID', 'NAME']]

    return df


def clean_est(df, year):
    # Assign column names that we know about
    rng = range(0, len(ESTIMATE_COL_NAMES))
    df = df.rename(columns=dict(zip(rng, ESTIMATE_COL_NAMES)))
    return df


def trim_geoid(geoid):
    """Removes leading bits from summary file GEOID."""
    exp = r"42101[0-9]*$"
    match = re.search(exp, geoid)
    if not match:
        raise Error('Could not trim GEOID.')

    return match.group()


if __name__ == '__main__':
    if len(sys.argv) <= 1:
        sys.stderr.write(f"usage: python {sys.argv[0]} "
                          "<summary-file-directory>\n")
        exit(1)

    summary_file_dir = SummaryFileDirectory(sys.argv[1])
    if not summary_file_dir.exists():
        sys.stderr.write(f"Path {summary_file_dir} does not exist!\n")
        exit(1)

    df_final = pd.DataFrame(
        columns=['GEOID', 'year'] + variable_list.variables()
    )

    for year in YEARS:
        df_seq = pd.read_csv(summary_file_dir.sequence_file_path(year))
        df_seq = clean_sequence_lookup(df_seq, year)

        df_geo = pd.read_fwf(summary_file_dir.geography_file(year),
                             header=None,
                             names=GEO_COL_NAMES,
                             widths=GEO_COL_WIDTHS)
        df_geo = clean_geo(df_geo, year)

        df_out = df_geo[['GEOID']].copy()
        df_out['year'] = year

        for row in df_seq.to_dict('records'):
            var_name = row['fullname']
            seq_num = row['sequence_number']
            start_pos = row['start_position']
            offset = VariableList.var_offset(var_name)
            target_col = start_pos - 1 + offset

            path = summary_file_dir.estimate_file(year, seq_num)
            df_est = pd.read_csv(path,
                                 header=None)
            df_est = clean_est(df_est, year)

            df = pd.merge(df_geo, df_est, how='left', on='LOGRECNO')

            df = df[['GEOID', target_col]]
            df = df.rename(columns={
                target_col: variable_list.our_var_for_acs_var(var_name)
            })

            df_out = pd.merge(df_out, df, how='left', on='GEOID')
            df_out.GEOID = df_out.GEOID.map(lambda x: trim_geoid(x))

        df_final = pd.concat([df_final, df_out])

    df_final.to_csv(sys.stdout, index=False)
