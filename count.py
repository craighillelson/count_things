"""
Counts elements in a one column csv. Writes results to a new csv.
"""

import csv
import glob
import os
import pyinputplus as pyip


def reports_folder():
    """
    Check to see if a reports folder exists. If a reports folder does not exist,
    create one.
    """

    if os.path.exists("reports") == True:
        print("reports directory exists")
        print("setup complete\n")
    else:
        os.mkdir("reports")
        print("reports directory created successfully")


def replace_spaces_with_underscores():
    """Replace spaces in filenames with underscores."""

    lst = [os.rename(csv_file, csv_file.replace(" ", "_").lower()) \
           for csv_file in os.listdir(".") if not csv_file.startswith(".")]
    return lst


def get_list_of_files():
    """Using glob, populate a list of all the csvs in the directory."""

    return glob.glob("*.csv")


def append_report_csv(filename):
    """
    Create a new file by appending '_report.csv' to the constituent file
    names. Results will be written to the newly created file.
    """

    return filename.split(".")[0] + "_report.csv"


def populate_list_of_elements(filename):
    """Import a csv and populate a list of all apps."""

    lst = []

    with open(filename, newline="") as csvfile:
        appreader = csv.reader(csvfile, delimiter=" ", quotechar="|")
        column_header = " ".join(next(appreader))
        for row in sorted(appreader):
            lst.append(" ".join(row))

    return column_header, lst


def build_dct_of_counts():
    """
    Using Counter from Python's standard library, populate a dictionary
    structured in the following way.
    key: item
    value: number of occurances of item
    """

    dct = {}
    for element in elements:
        dct.setdefault(element, 0)
        dct[element] = dct[element] + 1

    return dct


def prompt_user_for_num_results():
    """
    Prompt user for the number of results they'd like to see. User must input an
    integer.
    """

    return pyip.inputInt("How many results would you like to see?\n> ")


def output_results():
    """Output results to the screen."""

    print(f"{header}, count")
    for element, count in sorted(element_counts.items(), key=lambda x: x[1], \
                                 reverse=True):
        print(f"{element}, {count}")


def write_dct_to_csv(filename):
    """
    Write dictionary to csv. The dictionary will be structured in the following
    way.
    key: application
    value: number of installs
    """

    dir_filename = "reports/" + filename
    with open(dir_filename, "w") as out_file:
        out_csv = csv.writer(out_file)
        out_csv.writerow([header,"count"])
        for element, num_installs in sorted(element_counts.items(), key=lambda \
                                            x: x[1], reverse=True):
            keys_values = (element, num_installs)
            out_csv.writerow(keys_values)

    print(f'\n"{filename}" exported successfully\n')


reports_folder()
replace_spaces_with_underscores()
file_list = get_list_of_files()
for file in file_list:
    header, elements = populate_list_of_elements(file)
    element_counts = build_dct_of_counts()
    file_to_export = append_report_csv(file)
    output_results()
    write_dct_to_csv(file_to_export)
