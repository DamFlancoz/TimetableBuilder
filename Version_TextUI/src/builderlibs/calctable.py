"""Contains calculate_tables, used to evaluate TimeTable"""

from copy import deepcopy

from src.timetablebuilder.builderlibs.exceptions import NotFit, NoSectionOfTypeFit
from src.timetablebuilder.builderlibs.builderclasses import Table, Course, Section


def check_section_with_day_lengths(section, day_lengths):
    """
    Checks if section can fit in day according to day_length.

    Args:
        section (Section Object): section to check.
        day_lengths (dict): dictionary with M,T,W,R,F keys with day lengths in tuple.

    Returns:
        bool: True if section fits in day_length False.
    """

    return all(
        [
            section.time[0] <= day_lengths[day][0]
            or section.time[1] >= day_lengths[day][1]
            for day in section.days
        ]
    )


def insert_in_table(section, table):
    """
    Checks timings for section and inserts them in table in
    [start,end,course+course_no.,section] form.
        eg. [12.5,13.5,'MATH101','T01']

    Args:
        section (Section Objects): section to insert.
        tables (Table Objects): Table to insert.

    Returns:
        Table Object: Table with section inserted.

    Raises:
        NotFit: If any class on a day cannot fit in.
    """
    time = section.time

    # Waring this makes the lists in all days point to sam list
    # if you make change in one to_insert in one day, all of them change
    to_insert = [
        time[0],
        time[1],
        section.course_name + section.course_num,
        section.section,
    ]

    for day in section.days:
        # inserting in free day
        if table[day] == []:
            table[day].insert(0, to_insert)

        # inserting at start of day
        elif time[1] <= table[day][0][0]:
            table[day].insert(0, to_insert)

        else:
            # inserting during the day
            for i in range(len(table[day]) - 1):
                if table[day][i][1] <= time[0] and time[1] <= table[day][i + 1][0]:
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


def insert_same_in_table(section, table):
    """
    Inserts section with exact same timings as another in given table in
    [start,end,course+course_no,section] form.
        eg. [12.5,13.5,'MATH101','T01']

    Args:
        section (Section Objects): section to insert.
        tables (Table Objects): Table to insert.

    Returns:
        Table Object: Table with section inserted.
    """
    time = section.time
    day = section.days[0]

    # you don't need to add section to each day since all of them
    # point to same list
    for i in range(len(table[day])):
        if table[day][i][0] == time[0] and time[1] == table[day][i][1]:
            table[day][i].append(section.section)
            break

    for s in table.sections:
        if s[0] == section:
            s.append(section)
            break

    return table


def calculate_tables(selected_courses, day_lengths):
    """
    Evaluates all possible tables from selected_courses and day_lengths and return the
    list.

    Args:
        selected_courses (list): list of courses in their representativetuple form.
        day_lengths (dict): dictionary with M,T,W,R,F keys with day lengths in tuple.

    Returns:
        Table Object: Table with section inserted.
    """

    # prints all selected courses
    for i in selected_courses:
        print(i)

    tables = [Table()]  # free weekly default
    new_tables = {}  # acts as buffer for new tables made in each type for each section

    for course in selected_courses:
        print(course.name)
        for type_ in course:
            for section in type_:
                print(section)

                # skip if section falls out of required schedule
                if not check_section_with_day_lengths(section, day_lengths):
                    continue

                for i, t in enumerate(tables):

                    # i is in new_tables[(time,section.days,i)] so that a section does
                    # not keep puting in itself.
                    #   eg 'A01' in next iterations of tables sees its previous entry in
                    #       new tables and puts itself wih it again.
                    # But it allows other sections with same day and time to find the table

                    time = section.time  # (start,end) eg (11,13.5) for'11am-1:20pm'

                    if not (time, section.days, i) in new_tables:
                        table = deepcopy(t)

                        try:
                            table = insert_in_table(section, table)
                            new_tables[(time, section.days, i)] = table

                        except NotFit:
                            continue
                    else:
                        new_tables[(time, section.days, i)] = insert_same_in_table(
                            section, new_tables[(time, section.days, i)]
                        )

            # if no section of a type can be added then
            if new_tables == {} and type_ != []:
                for i in tables:
                    print(i)
                raise NoSectionOfTypeFit(course)

            # If at start a type_ is [] it makes table [] in comprehension
            # but you want it to remain a free table (default value) so loop
            # for tables can run.

            tables = list(new_tables.values()) if new_tables else tables
            new_tables = {}

    return tables
