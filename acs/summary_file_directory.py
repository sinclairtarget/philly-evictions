import os

class SummaryFileDirectory:
    ZIP_FILENAME = 'summary_file.zip'
    SEQUENCE_FILENAME = 'sequence_lookup.txt'
    ESTIMATE_FILENAME_TEMPLATE = "e{}5pa{}000.txt"
    GEOGRAPHY_FILENAME_TEMPLATE = "g{}5pa.txt"

    def __init__(self, path):
        self.path = path


    def exists(self):
       return os.path.exists(self.path)


    def year_dir(self, year):
        return os.path.join(self.path, str(year))


    def zip_file_path(self, year):
        dirname = self.year_dir(year)
        return os.path.join(dirname, self.ZIP_FILENAME)


    def sequence_file_path(self, year):
        dirname = self.year_dir(year)
        return os.path.join(dirname, self.SEQUENCE_FILENAME)


    def estimate_file(self, year, sequence_number):
        """
        Path to estimate file for the given sequence number in the year.
        """
        dirname = self.year_dir(year)
        padded_seq_num = str(sequence_number).zfill(4)
        filename = self.ESTIMATE_FILENAME_TEMPLATE.format(year, padded_seq_num)
        return os.path.join(dirname, filename)


    def geography_file(self, year):
        dirname = self.year_dir(year)
        filename = self.GEOGRAPHY_FILENAME_TEMPLATE.format(year)
        return os.path.join(dirname, filename)


    def __str__(self):
        return self.path
