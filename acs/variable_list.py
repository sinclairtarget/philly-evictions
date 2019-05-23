"""
Wraps the list of ACS variables we want to download/use.
"""
import csv
import os

DIRNAME = os.path.dirname(__file__)
FILENAME = os.path.join(DIRNAME, 'variables.csv')

class VariableList:
    def __init__(self, filename=FILENAME):
        self.mapping = dict()      # Maps our var name to ACS var name

        with open(filename) as f:
            reader = csv.reader(f)
            next(reader)

            for row in reader:
                self.mapping[row[1]] = row[0]


    def acs_variables(self):
        """ACS variable names."""
        return list(self.mapping.values())


    def variables(self):
        """Nice variable names that we came up with."""
        return list(self.mapping.keys())
