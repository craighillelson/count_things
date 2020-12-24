"""
Counts elements in a one column csv. Writes results to a new csv.
"""

import csv
import pyinputplus as pyip


def populate_list_of_elements():
    """Import a csv and populate a list of all apps."""

    lst = []

    with open("filename.csv", newline="") as csvfile:
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


def write_dct_to_csv():
    """
    Write dictionary to csv. The dictionary will be structured in the following
    way.
    key: application
    value: number of installs
    """

    with open("filename_report.csv", "w") as out_file:
        out_csv = csv.writer(out_file)
        out_csv.writerow([header,"count"])
        for element, num_installs in sorted(element_counts.items(), key=lambda \
                                            x: x[1], reverse=True):
            keys_values = (element, num_installs)
            out_csv.writerow(keys_values)

    print('\n"abc_report.csv" exported successfully\n')


header, elements = populate_list_of_elements()
element_counts = build_dct_of_counts()
output_results()
write_dct_to_csv()
