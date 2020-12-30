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
        print("\nreports directory exists")
    else:
        os.mkdir("reports")
        print("\nreports directory created successfully")


def exclusions_file():
    """
    Check to see if "exclusions.csv" exists in the reports folder. If an 
    exclusions file doesn't exist, create one."""

    if os.path.exists("reports/exclusions.csv"):
        print('"exclusions.csv" already exists')
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

    print("\nsetup")
    reports_folder()
    exclusions_file()
    replace_spaces_with_underscores()
    print("\nsetup complete")


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


def build_list_of_exclusions_to_add():
    """
    Taking user input, add the user's choices of elements to exclude to a list
    of exclusions to be merged with the pre-existing list of exclusions.
    """


    def print_instruction():
        """Prompt user to make a selection or quit."""

        print("\nselect an element to exclude (or nothing to exit)")


    lst = []
    while True:
        user_selection = pyip.inputInt("\n> ", min=1, blank=True)
        if user_selection == "":
            break
        lst = lst + [remaining_elements_map[user_selection]]
        print_instruction()
    return lst


def ammend_exclusions_csv():
    """Write additional exclusions to 'reports/exclusions.csv'"""

    with open("reports/exclusions.csv", "a") as out_file:
        out_csv = csv.writer(out_file)
        for element in exclusions_to_add:
            out_csv.writerow([element])


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


def print_totals():
    """Print totals."""

    for element in elements_counts:
        print(f'{element[0]}: {element[1]}')


def write_totals_to_csv():
    """Write totals for each element to 'reports/totals.csv'"""

    with open("reports/totals.csv", "w") as out_file:
        out_csv = csv.writer(out_file)
        out_csv.writerow(["element","count"])
        for element in elements_counts:
            out_csv.writerow(element)

    print('\n"totals.csv" exported to reports folder successfully\n')


setup()

pre_exisitng_exclusions = build_list_of_pre_existing_exclusions()
print_singular_or_plural(pre_exisitng_exclusions, "pre-existing exclusions",
                         "pre-existing exclusion",
                         "no pre-existing exclusions found")

filenames = build_list_of_files()
print_singular_or_plural(filenames, "filenames", "filename", "no files found")

print("\ndictionaries")
dct = defaultdict(list)
groups_elements = []
for filename in filenames:
    group_name = filename.split(".")[0]
    with open(filename, newline='') as csvfile:
        elementreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        headings = next(elementreader)
        for row in elementreader:
            groups_elements.append([group_name, row[0]])

for group_element in groups_elements:
    dct[group_element[0]].append(group_element[1])

for group, elements in dct.items():
    print(group, elements)

print("\ncounts per file")
for group, elements in dct.items():
    element_counts = Counter(elements)
    elements_counts = element_counts.most_common()
    print(group, *elements_counts)

print("\nall elements")
all_elements = []
for group, elements in dct.items():
    all_elements.extend(elements)
print(all_elements)

print("\nremaining elements map")
print("make a selection from the elements below (or nothing to quit)")

remaining_elements = []
elements_set = set(all_elements)
for element in elements_set:
    if element not in pre_exisitng_exclusions:
        remaining_elements.append(element)

remaining_elements_map = {}
for num, element in enumerate(sorted(remaining_elements), 1):
    remaining_elements_map[num] = element

for num, element in remaining_elements_map.items():
    print(f"{num}. {element}")

exclusions_to_add = build_list_of_exclusions()
all_exclusions = exclusions_to_add + pre_exisitng_exclusions
print_singular_or_plural(all_exclusions, "all exclusions", "exclusion",
                         "no exclusions found")
ammend_exclusions_csv()

print("\ntotals")
element_counts = Counter(all_elements)
elements_counts = element_counts.most_common()
print_totals()
write_totals_to_csv()
