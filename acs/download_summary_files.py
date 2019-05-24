import sys
import os
import subprocess
import glob

from summary_file_directory import SummaryFileDirectory

SUMMARY_FILE_URL_TEMPLATE = ("https://www2.census.gov/programs-surveys/acs/"
                             "summary_file/{}/data/5_year_by_state/"
                             "Pennsylvania_Tracts_Block_Groups_Only.zip")

# URL for the sequence lookup file
SEQUENCE_FILE_URL_TEMPLATE = ("https://www2.census.gov/programs-surveys/acs/"
                              "summary_file/{}/documentation/5_year/user_tools"
                              "/Sequence_Number_and_Table_Number_Lookup.txt")

YEARS = range(2009, 2013)

def summary_file_url(year):
    return SUMMARY_FILE_URL_TEMPLATE.format(year)


def sequence_file_url(year):
    return SEQUENCE_FILE_URL_TEMPLATE.format(year)


def download_zip(summary_file_dir, year):
    dirname = summary_file_dir.year_dir(year)
    filename = summary_file_dir.zip_file_path(year)
    url = summary_file_url(year)
    os.makedirs(dirname, exist_ok=True)

    if not os.path.exists(filename):
        subprocess.run(['curl', '-o', filename, url], check=True)

    return filename


def unzip(summary_file_dir, year):
    dirname = summary_file_dir.year_dir(year)
    filename = summary_file_dir.zip_file_path(year)
    subprocess.run(['unzip', filename, '-d', dirname], check=True)
    os.remove(filename)


def download_sequence_file(summary_file_dir, year):
    dirname = summary_file_dir.year_dir(year)
    filename = summary_file_dir.sequence_file_path(year)
    url = sequence_file_url(year)
    subprocess.run(['curl', '-o', filename, url], check=True)
    return filename


def remove_margin_of_error_files(summary_file_dir, year):
    dirname = summary_file_dir.year_dir(year)
    margin_error_files = glob.glob(os.path.join(dirname, 'm*.txt'))
    for f in margin_error_files:
        os.remove(f)


def fix_encoding(filename):
    """
    Sequence lookup files are encoded as latin1 with weird characters.

    This converts the file to utf8 using the iconv utility.
    """
    temp_f = filename + '.tmp'
    subprocess.run(['iconv', '-t', 'utf-8', '-c', '-o', temp_f, filename],
                   check=True)
    os.rename(temp_f, filename)


if __name__ == '__main__':
    if len(sys.argv) <= 1:
        sys.stderr.write(f"usage: python {sys.argv[0]} "
                          "<summary-file-directory>\n")
        exit(1)

    summary_file_dir = SummaryFileDirectory(sys.argv[1])
    if not summary_file_dir.exists():
        sys.stderr.write(f"Path {summary_file_dir} does not exist!\n")
        exit(1)

    print('Downloading summary files. This might take a while...')
    for year in YEARS:
        zip_filename = download_zip(summary_file_dir, year)
        unzip(summary_file_dir, year)
        remove_margin_of_error_files(summary_file_dir, year)
        sequence_filename = download_sequence_file(summary_file_dir, year)
        fix_encoding(sequence_filename)
