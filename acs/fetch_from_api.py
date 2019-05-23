"""
This script uses the Census API to fetch five-year ACS estimate data (at the
blockgroup level) for 2013 to 2016. These years are all that is available via
the Census API.
"""
import sys
from csv import DictWriter
from census import Census

from variable_list import VariableList

API_KEY = '35c615c69742eabcfe631cf4c29ff3fed90939cc'
PA_FIPS_CODE = '42'
PHILADELPHIA_COUNTY_FIPS_CODE = '101'

YEARS = range(2013, 2017)               # Fetch from 2013-2016 inclusive.

variable_list = VariableList()

class BlockGroup:
    def __init__(self, bg_data, year):
        self.bg_data = bg_data
        self.year = year


    def map_variable_names(self):
        """Maps ACS var names to nicer names we want to use for our columns."""
        for colname, var in variable_list.mapping.items():
            self.bg_data[colname] = self.bg_data.pop(var)

        return self


    def add_geoid(self):
        """
        Creates a GEO ID in the style used by the eviction lab data.

        This is state FIPS code + county FIPS code + tract id + block group id.
        """
        self.bg_data['GEOID'] = \
            PA_FIPS_CODE + PHILADELPHIA_COUNTY_FIPS_CODE + \
            self.bg_data['tract'] + self.bg_data['block group']
        return self


    def add_year(self):
        self.bg_data['year'] = self.year
        return self


    def to_csv_row(self):
        """
        Do all the transformations we want to do on the data we get from the
        Census API.
        """
        return self.map_variable_names()\
                   .add_geoid()\
                   .add_year()\
                   .bg_data


def colnames():
    return ['GEOID', 'year'] + variable_list.variables()


def fetch_blockgroups(year):
    client = Census(API_KEY)
    resp = client.acs5.state_county_blockgroup(
        variable_list.acs_variables(),
        PA_FIPS_CODE,
        PHILADELPHIA_COUNTY_FIPS_CODE,
        Census.ALL,
        year=year
    )

    return [BlockGroup(bg_data, year) for bg_data in resp]


if __name__ == "__main__":
    writer = DictWriter(
        sys.stdout,                        # Output to stdout
        fieldnames=colnames(),             # Look for these keys
        extrasaction='ignore'              # Ignore extra keys in row dicts
    )

    writer.writeheader()

    for year in YEARS:
        blockgroups = fetch_blockgroups(year)

        for blockgroup in blockgroups:
            writer.writerow(blockgroup.to_csv_row())
