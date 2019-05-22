"""
This script fetches five-year ACS estimate data (at the blockgroup level) for
2013 to 2016, which is all that is available via the Census API.
"""
import sys
from csv import DictWriter
from census import Census

API_KEY = '35c615c69742eabcfe631cf4c29ff3fed90939cc'
PA_FIPS_CODE = '42'
PHILADELPHIA_COUNTY_FIPS_CODE = '101'

YEARS = range(2013, 2017)               # Fetch from 2013-2016 inclusive.

class BlockGroup:
    COLNAME_TO_VAR_MAP = {
        'renter_occupied_household_size': 'B25010_003E'
    }

    def __init__(self, bg_data, year):
        self.bg_data = bg_data
        self.year = year


    def varnames_for_request():
        return tuple(BlockGroup.COLNAME_TO_VAR_MAP.values())


    def colnames():
        return ['GEOID', 'year'] + list(BlockGroup.COLNAME_TO_VAR_MAP.keys())


    def map_variable_names(self):
        """Maps ACS var names to nicer names we want to use for our columns."""
        for colname, var in self.COLNAME_TO_VAR_MAP.items():
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


def fetch_blockgroups(year):
    client = Census(API_KEY)
    resp = client.acs5.state_county_blockgroup(
        BlockGroup.varnames_for_request(),
        PA_FIPS_CODE,
        PHILADELPHIA_COUNTY_FIPS_CODE,
        Census.ALL,
        year=year
    )

    return [BlockGroup(bg_data, year) for bg_data in resp]


if __name__ == "__main__":
    writer = DictWriter(
        sys.stdout,                        # Output to stdout
        fieldnames=BlockGroup.colnames(),  # Look for these keys
        extrasaction='ignore'              # Ignore extra keys in row dicts
    )

    writer.writeheader()

    for year in YEARS:
        blockgroups = fetch_blockgroups(year)

        for blockgroup in blockgroups:
            writer.writerow(blockgroup.to_csv_row())
