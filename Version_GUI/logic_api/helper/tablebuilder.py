"""
This module provides functionality to calculate time tables.
Use calculate_tables.
"""

from time import localtime  # for seting term

from .classes import Table, Course, NotFit
from .coursesinfo import get_course_info


def build_table(term, selected_sections):

    courses = [get_course_info(term, Course(*c.split())) for c in selected_sections]

    filter_sections(courses, selected_sections)

    table = Table()  # free weekly default

    for course in courses:
        for type_ in course:  # lab, lecture and tutorial
            for section in type_:
                insert_in_table(section, table)

    return table


def insert_in_table(section, table):
    """
    Checks timings for section and inserts them table.
    Raises NotFit Error if any class on a day cannot fit in.

    inserts - [start,end,course+courseno.,section]
    eg. [12.5,13.5,'MATH101','T01']
    """
    time = section.time

    # Waring this makes the lists in all days point to sam list
    # if you make change in one to_insert in one day, all of them change
    to_insert = [
        time[0],
        time[1],
        f"{section.course_name} {section.course_num}",
        section.section,
    ]

    for day in section.days:
        # inserting in free day
        if table[day] == []:
            table[day].insert(0, to_insert)

        # inserting at start of day
        elif table[day][0][0] >= time[1]:
            table[day].insert(0, to_insert)

        else:
            # inserting during the day
            for i in range(len(table[day]) - 1):
                if table[day][i][1] <= time[0] and table[day][i + 1][0] >= time[1]:
                    table[day].insert(i + 1, to_insert)
                    break

            # inserting at end of day
            else:
                if table[day][-1][1] <= time[0]:
                    table[day].append(to_insert)
                else:
                    raise NotFit()

    table.sections.append([section])

    return table


def filter_sections(courses, selected_sections):
    """
    Takes out not selected sections.
    """
    for c in courses:
        c_key = f"{c.name} {c.num}"

        lab_section = selected_sections[c_key]["lab"]
        lecture_section = selected_sections[c_key]["lecture"]
        tutorial_section = selected_sections[c_key]["tutorial"]

        c.labs = [s for s in c.labs if s.section == lab_section]
        c.lectures = [s for s in c.lectures if s.section == lecture_section]
        c.tutorials = [s for s in c.tutorials if s.section == tutorial_section]
