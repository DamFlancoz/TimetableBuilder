"""
This implements the main interface for the program.

TODO:
    * fix repeated adding bug with mah101 and csc115, different
        adding incase of csc115,math101 amd math101,csc115
        initial table is fine but after end at 15 problem appears
    * fix tests

"""

import re
from time import localtime

from builderlibs.webscrapper import get_course_html
from builderlibs.parsehtml import put_sections_in_course
from builderlibs.calctable import calculate_tables
from builderlibs.builderclasses import Table, Course
from builderlibs.exceptions import NoSectionsAvailableOnline, NoSectionOfTypeFit


def set_term(inp):
    """
    Converts term input to term code to be passed into request header.

    Args:
        inp (str): input for term next/n or current/curr.

    Returns:
        str: representative str of int.
    """
    if ("next" in inp) or ("n" in inp):

        # gives tuple (year,month,date,h,min,s,weekday, etc.)
        time = localtime()

        if time[1] in [1, 2, 3, 4]:  # next term from may
            term = str(time[0]) + "05"

        elif time[1] in [5, 6, 7, 8]:  # next term from sept
            term = str(time[0]) + "09"

        else:  # next term from jan
            term = str(time[0] + 1) + "01"

    elif ("current" in inp) or ("curr" in inp):

        # gives tuple (year,month,date,h,min,s,weekday, etc.)
        time = localtime()

        if time[1] in [1, 2, 3, 4]:  # next term from jan
            term = str(time[0]) + "01"

        elif time[1] in [5, 6, 7, 8]:  # next term from may
            term = str(time[0]) + "05"

        else:  # current term from sept
            term = str(time[0]) + "09"

    elif inp.isdigit() and len(inp) == 6:
        term = inp

    return term


def processArgToCourse(i):
    """
    Converts input course into representative tuple.
        eg. math101/MaTh 101 = ('MATH','101')

    Args:
        i (str): input course.

    Returns:
        tuple: representative tuple.
    """
    i = i.strip().upper()

    name = ""
    num = ""
    for char in i:
        if char.isalpha():
            name += char
        elif char.isdigit():
            num += char

    return (name, num)


############################## Global Variables

term = set_term("curr")  # term chosen
selected_courses = []  # Course objects
day_lengths = {"M": [0, 24], "T": [0, 24], "W": [0, 24], "R": [0, 24], "F": [0, 24]}
tables = [Table()]  # single table with all free days to start

help = """
Use
- Commas(,) to to separate values, eg. add math 101, csc111
- Term has commands next and current, or equivalently, n and curr respectively
- Add, eg. add math101,csc111 etc.
- Remove/rem/rmv, eg. rem math101 etc.
- Start <MR or all> at 10, use 24hr and decimals eg. start MR at 13.5 for start Monday and Thursday at 1:30pm
- start M at reset, to reset the value
- End <MR or all> at 10, same as start but for day ends
- Show, to see selected courses and term
- Calc to Calculate all the tables
- Show table to see tables
- crns of <table index> to get crns of classes in that table
- Quit to quit
- help to show this again
"""


################################# Main Program


def main():
    global term, selected_courses, day_lengths, tables, help

    print(help)

    while True:
        print()
        inp = input(">>> ").lower().strip()

        ## Commands
        # sets term for courses
        if "term" in inp:

            # remove command word and get the argument
            inp = inp.replace("term", "").strip()

            try:
                term = set_term(inp)
            except:
                print("Term takes an input; next, current or termcode")

        # adds course(s)
        elif "add" in inp:

            # removes command word and makes list of arguments
            inp = inp.replace("add", "").split(",")

            for course in inp:

                course = processArgToCourse(course.strip())  # returns [name,number]

                if course not in selected_courses:
                    selected_courses.append(Course(course[0], course[1]))

        # removes course(s)
        elif ("remove" in inp) or ("rem" in inp) or ("rmv" in inp):

            # removes command word and makes list of arguments
            inp = (
                inp.replace("remove", "")
                .replace("rem", "")
                .replace("rmv", "")
                .split(",")
            )

            for course in inp:

                course = processArgToCourse(
                    course.strip()
                )  # evalCourse returns [name,number]

                if course in selected_courses:
                    selected_courses.remove(course)

        # displays term: courses
        elif inp in ["show", "show courses"]:

            print(term + ": ", end="")

            for course in selected_courses:
                print(course.name, course.num + ",", end="")

            print()  # moves cursor to next line
            print(i + ": " + str(day_lengths[i]) for i in day_lengths)

        elif "start" in inp and "at" in inp:
            inp = inp.split(" ")

            if inp[1] == "all":
                if inp[3] == "reset":
                    for day in day_lengths:
                        day_lengths[day][0] = 0
                else:
                    for day in day_lengths:
                        day_lengths[day][0] = int(inp[3])
            else:
                if inp[3] == "reset":
                    for day in inp[1].upper():
                        day_lengths[day][0] = 0
                else:
                    for day in inp[1].upper():
                        day_lengths[day][0] = int(inp[3])

        elif "end" in inp and "at" in inp:
            inp = inp.split(" ")

            if inp[1] == "all":
                if inp[3] == "reset":
                    for day in day_lengths:
                        day_lengths[day][1] = 24
                else:
                    for day in day_lengths:
                        day_lengths[day][1] = int(inp[3])
            else:
                if inp[3] == "reset":
                    for day in inp[1].upper():
                        day_lengths[day][1] = 24
                else:
                    for day in inp[1].upper():
                        day_lengths[day][1] = int(inp[3])

        # Evaluates TimeTable
        elif ("calc" in inp) or ("eval table" in inp) or ("get tables" in inp):

            # add course info from web to Course Object
            try:
                selected_courses = [
                    put_sections_in_course(course, get_course_html(term, course))
                    for course in selected_courses
                ]

                tables = calculate_tables(selected_courses, day_lengths)

            # no section of given course is available in given term
            except NoSectionsAvailableOnline as e:

                selected_courses.remove(e.course)

                print(e.course.name, e.course.num, "is not available in", term)
                print("Removed the course.")
                print("You may want to add a replacement course.")

            # its impossible to fit all classes
            except NoSectionOfTypeFit as e:

                print(
                    "Current time restrictions don't allow you to take all classes of",
                    e.course.name,
                    e.course.num,
                )
                print("Change the Time restrictions or remove the course")

        elif "show tables" in inp:

            # ranks tables
            keys = [i.get_extra_hours() for i in tables]
            d = {}
            for k, i, t in zip(keys, *list(zip(*enumerate(tables)))):
                if k in d:
                    d[k].append((i, t))
                else:
                    d[k] = [(i, t)]
            keys = list(set(keys))
            keys.sort()

            # prints tables
            for k in keys:
                print(f"\t\t\t\t\t {k} extra hours")
                for i, t in d[k]:
                    print(f"index: {i}")
                    print(t)
                    print()
                print()

        elif "crns of" in inp:

            # get crns in 2d form
            crns = tables[int(re.search(r"[0-9]", inp).group(0))].get_crns()
            for i in crns:
                for j in i:
                    print(j, end=" ")
                print()

        # exit program
        elif inp in ["quit", "exit", "q", "done"]:
            break

        # show help
        elif "help" in inp:
            print(help)

        # deems input invalid
        else:
            print("Invalid Input")


########################################## Main Call

if __name__ == "__main__":
    main()
