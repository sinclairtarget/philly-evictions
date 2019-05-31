"""
Wraps the list of ACS variables we want to download/use.
"""
import csv
import os
import re
import collections

DIRNAME = os.path.dirname(__file__)
FILENAME = os.path.join(DIRNAME, 'variables.csv')

class VariableList:
    def __init__(self, filename=FILENAME):
        # Maps our var name to ACS var name
        self.mapping = collections.OrderedDict()
        self.reverse_mapping = collections.OrderedDict()

        with open(filename) as f:
            reader = csv.reader(f)
            next(reader)

            for row in reader:
                self.mapping[row[1]] = row[0]
                self.reverse_mapping[row[0]] = row[1]


    def acs_variables(self):
        """ACS variable names."""
        return list(self.mapping.values())


    def acs_tables(self):
        """Only the table part of ACS variable names."""
        variables = self.acs_variables()
        return [VariableList.table(var) for var in variables]


    def variables(self):
        """Nice variable names that we came up with."""
        return list(self.mapping.keys())


    def acs_var_for_our_var(self, our_varname):
        return self.mapping.get(our_varname)


    def our_var_for_acs_var(self, acs_varname):
        return self.reverse_mapping.get(acs_varname)


    def table(variable_name):
        """Get base ACS table name from variable name."""
        return variable_name.split('_')[0]


    def var_offset(variable_name):
        """
        Return offset for variable based on name.

        B25010_003E has an offset of 3, which become 2 if we zero-index.
        """
        exp = r"_([0-9]*)[a-zA-Z]*$"
        match = re.search(exp, variable_name)
        if not match:
            raise Error('Could not find offset from variable name!')

        return int(match.group(1)) - 1
