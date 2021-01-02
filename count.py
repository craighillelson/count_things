"""
Counts elements in a one column csvs. Totals results and outputs "totals.csv" to
reports folder.
"""

import csv
import glob
import os
from collections import Counter
from collections import defaultdict
import pyinputplus as pyip


def reports_folder():
    """
    Check to see if a reports folder exists. If a reports folder does not exist,
    create one.
    """

    if os.path.exists("reports"):
        pass
    else:
        os.mkdir("reports")


def exclusions_file():
    """
    Check to see if "exclusions.csv" exists in the reports folder. If an
    exclusions file doesn't exist, create one."""

    if os.path.exists("reports/exclusions.csv"):
        pass
    else:
        with open("reports/exclusions.csv", "w") as out_file:
            out_csv = csv.writer(out_file)
            out_csv.writerow(["element"])


def replace_spaces_with_underscores():
    """Replace spaces in filenames with underscores."""

    lst = [os.rename(csv_file, csv_file.replace(" ", "_").lower()) \
           for csv_file in os.listdir(".") if not csv_file.startswith(".")]
    return lst


def setup():
    """Runs functions that complete setup."""

    reports_folder()
    exclusions_file()
    replace_spaces_with_underscores()
    print("\nsetup complete")


def import_and_print_exclusions():
    """
    From 'exclusions.csv', import a list of exclusions and print them to the
    screen.
    """

    lst = build_list_of_pre_existing_exclusions()
    print_singular_or_plural(lst, "pre-existing exclusions",
                             "pre-existing exclusion",
                             "no pre-existing exclusions found")
    return lst


def print_singular_or_plural(lst, plural, singular, no_results):
    """Print element or elements."""

    if lst:
        if len(lst) > 1:
            print(f"\n{plural}")
            for i in sorted(lst):
                print(i)
        else:
            print(f"\n{singular}")
            print(lst[0])
    else:
        print(no_results)


def build_list_of_pre_existing_exclusions():
    """
    Import exclusions from 'reports/exclusions.csv' and return a list of all
    exclusions.
    """

    lst = []
    with open("reports/exclusions.csv", "r") as csv_file:
        f_csv = csv.reader(csv_file)
        headings = next(f_csv)
        for row in f_csv:
            lst.append(row[0])
    return lst


def build_list_of_files():
    """Using glob, populate a list of all the csvs in the directory."""

    return glob.glob("*.csv")


def build_list_of_tuples():
    """
    Return a list of tuples structured in the following way.
    (group, element)
    """
    lst = []
    for filename in filenames:
        group_name = filename.split(".")[0]
        with open(filename, newline='') as csvfile:
            elementreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
            headings = next(elementreader)
            for row in elementreader:
                lst.append([group_name, row[0]])

    return lst


def build_dct_of_groups_elements():
    """Return a dictionary strucutred in the following way.
    key: group
    value: number of occurances
    """

    dct = defaultdict(list)
    for group_element in groups_elements:
        dct[group_element[0]].append(group_element[1])

    return dct


def build_elements_counts():
    """
    Return a list of elements and a count of each element's total occurances.
    """

    for elements in group_elements.values():
        return count_elements(elements)


def build_lst_of_all_elements():
    """Return a list of all elements."""

    lst = []
    for elements in group_elements.values():
        lst.extend(elements)

    return lst


def build_lst_of_remaining_elements():
    """Return a list of elements minus exclusions specified by the user."""

    lst = []
    elements_set = set(all_elements)
    for element in elements_set:
        if element not in pre_exisitng_exclusions:
            lst.append(element)

    return lst


def build_remaining_elements_map():
    """
    Take the list of remaining elements, enumerate the elements starting at 1,
    and build a dictionary strucutred in the following way.

    key: integer (starting at 1 and incrementing by 1 for each element)
    value: element
    """

    dct = {}
    for num, element in enumerate(sorted(remaining_elements), 1):
        dct[num] = element

    return dct


def print_remaining_elements_map():
    """
    Print the remaining_elements_map in the interest of providing the user
    with options to add elements to be excluded.
    """

    print("\nmake a selection from the elements below to add to exclusions "
          "(or nothing to quit)")
    for num, element in remaining_elements_map.items():
        print(f"{num}. {element}")


def ammend_exclusions_csv():
    """Write additional exclusions to 'reports/exclusions.csv'"""

    with open("reports/exclusions.csv", "a") as out_file:
        out_csv = csv.writer(out_file)
        for element in exclusions_to_add:
            out_csv.writerow([element])


def build_filtered_lst_and_dct():
    """
    Return a list of elements minus excluded elements and a dictionary and a
    dictionary structured in the following way.
    key:
    value:
    """

    dct = defaultdict(list)
    for group, elements in group_elements.items():
        lst = [item for item in elements if not item in all_exclusions]
        dct[group].append(lst)

    return lst, dct


def build_filtered_counts_per_file():
    """
    Return a dictionary structured in the following way.
    key: group
    value: list of tuples of elements and counts
    """

    dct = defaultdict(list)

    for group, elements in filtered_dct.items():
        elements_counts = count_elements(elements[0])
        dct[group].append(elements_counts)

    return dct


def print_filtered_counts_per_file():
    """Print element counts per file."""

    print("\nelement counts per file")
    for group, elements_counts_list in filtered_counts_per_file.items():
        elements_counts = sorted(elements_counts_list[0])
        print(group, *elements_counts, sep=", ")


def build_list_of_exclusions():
    """Build a list of elements to exclude based on user input."""

    lst = []

    while True:
        selected_element = pyip.inputInt("\n> ", min=1, blank=True)
        if selected_element == "":
            break
        lst = lst + [remaining_elements_map[selected_element]]
        print("\nmake a selection from the elements below (or nothing to quit)")

    return lst


def output_results_to_csvs():
    """Write results to csvs."""

    print("\nexported files")
    for group, elements_counts_list in filtered_counts_per_file.items():
        filename = group + "_report.csv"
        dir_filename = "reports/" + filename
        with open(dir_filename, "w") as out_file:
            out_csv = csv.writer(out_file)
            out_csv.writerow(["element","count"])
            for elements_counts in elements_counts_list:
                for ele_count in elements_counts:
                    out_csv.writerow(ele_count)
            print(f"{filename} exported to reports folder successfully")


def count_elements(lst):
    """Return a list of elements and a count of their occurances."""

    element_counts = Counter(lst)
    return element_counts.most_common()


def calculate_print_and_output_totals():
    lst = []
    for ele_list in filtered_dct.values():
        for ele in ele_list:
            lst.extend(ele)
    lst2 = count_elements(lst)
    print(f"\ntotals")
    for ele_count in lst2:
        print(*ele_count)

    return lst2


def output_totals_to_csv():
    """Write totals for each element to 'reports/totals.csv'"""

    with open("reports/totals.csv", "w") as out_file:
        out_csv = csv.writer(out_file)
        out_csv.writerow(["element","count"])
        for element in totals:
            out_csv.writerow(element)

    print('\n"totals.csv" exported to reports folder successfully\n')


setup()
pre_exisitng_exclusions = import_and_print_exclusions()
filenames = build_list_of_files()
groups_elements = build_list_of_tuples()
group_elements = build_dct_of_groups_elements()
elements_counts = build_elements_counts()
all_elements = build_lst_of_all_elements()
remaining_elements = build_lst_of_remaining_elements()
remaining_elements_map = build_remaining_elements_map()
print_remaining_elements_map()
exclusions_to_add = build_list_of_exclusions()
all_exclusions = exclusions_to_add + pre_exisitng_exclusions
print_singular_or_plural(all_exclusions, "all exclusions", "exclusion",
                         "no exclusions found")
ammend_exclusions_csv()
filtered, filtered_dct = build_filtered_lst_and_dct()
filtered_counts_per_file = build_filtered_counts_per_file()
print_filtered_counts_per_file()
elements_counts = count_elements(filtered)
output_results_to_csvs()
totals = calculate_print_and_output_totals()
output_totals_to_csv()
