"""Contains  tests for all VersionText"""

import os

from src.timetablebuilder.builderlibs.webscrapper import get_course_html
from src.timetablebuilder.builderlibs.parsehtml import put_sections_in_course
from src.timetablebuilder.builderlibs.calctable import calculate_tables
from src.timetablebuilder.builderlibs.builderclasses import Table, Course, Section
from src.timetablebuilder.builderlibs.exceptions import (
    NoSectionsAvailableOnline,
    NoSectionOfTypeFit,
)

with open(os.path.join("tests", "csc111spring2019.html"), "r") as t:
    csc111_html = t.read()

########################### test web scrapping


def test_get_course_html():

    expected = csc111_html
    getting = get_course_html("201901", Course("CSC", "111"))

    # with open(os.path.join("tests", "csc111spring2019.html"), "w") as t:
    #     t.write(getting)

    assert expected == getting

    # Page not available cases check
    # CSC 111 and math 101 in 201902 give a little different pages
    try:
        get_course_html("201901", Course("C1SC", "111"))
        raise AssertionError("Exception not Thrown")

    except NoSectionsAvailableOnline:
        pass

    # Math 101 not in summer 2019
    try:
        get_course_html("201902", Course("MATH", "101"))
        raise AssertionError("Exception not Thrown")

    except NoSectionsAvailableOnline:
        pass


########################## testing html parsing


def test_put_in_sections_course():
    """
    Case of CSC111, 2019 jan-term
    """

    course_page_html = csc111_html

    getting = put_sections_in_course(
        Course("CSC", "111"), course_page_html
    )  # returns Course object

    expected = """Course: CSC 111
Lectures:
	Course: CSC 111 | Section: A01 | Time: (10, 11.5) | Days: MR
	Course: CSC 111 | Section: A02 | Time: (10, 11.5) | Days: MR
Labs:
	Course: CSC 111 | Section: B01 | Time: (11.5, 13.5) | Days: W
	Course: CSC 111 | Section: B02 | Time: (13.5, 15.5) | Days: W
	Course: CSC 111 | Section: B03 | Time: (15.5, 17.5) | Days: W
Tutorials:
"""

    assert str(getting) == expected


####################### test calculate tables


def deep_tuple(t):
    """
    Converts all nested lists to tuples to tuple. Helpful when need to convert
    to set from nested lists. Used in Test_evalTable
    """
    return tuple(deep_tuple(i) for i in t) if type(t) == list or type(t) == Table else t


def test_calculate_tables():

    courses_info = {
        "MATH200": {
            "labs": [],
            "lectures": [
                {
                    "type": "Lecture",
                    "section": "A01",
                    "days": "MR",
                    "place": "Hickman Building 105",
                    "time": "8:30 am - 11:50 pm",
                    "instructor": "Andrew Mc (P)",
                    "crn": "22034",
                }
            ],
            "tutorials": [
                {
                    "type": "Tutorial",
                    "section": "T01",
                    "days": "T",
                    "place": "Building A212",
                    "time": "3:30 pm - 4:20 pm",
                    "instructor": "TBA",
                    "crn": "22035",
                },
                {
                    "type": "Tutorial",
                    "section": "T02",
                    "days": "T",
                    "place": "Cornett Building A121",
                    "time": "3:30 pm - 4:20 pm",
                    "instructor": "TBA",
                    "crn": "22036",
                },
            ],
        },
        "MATH204": {
            "labs": [],
            "lectures": [
                {
                    "type": "Lecture",
                    "section": "A01",
                    "days": "TWF",
                    "place": "David Strong Building C103",
                    "time": "1:30 pm - 2:20 pm",
                    "instructor": "Muhammad (P)",
                    "crn": "22040",
                },
                {
                    "type": "Lecture",
                    "section": "A02",
                    "days": "TWF",
                    "place": "David Turpin Building A104",
                    "time": "8:30 am - 9:20 am",
                    "instructor": "Slim Sir (P)",
                    "crn": "22041",
                },
            ],
            "tutorials": [
                {
                    "type": "Tutorial",
                    "section": "T01",
                    "days": "F",
                    "place": "David Turpin Building A110",
                    "time": "3:30 pm - 4:20 pm",
                    "instructor": "TBA",
                    "crn": "22042",
                },
                {
                    "type": "Tutorial",
                    "section": "T02",
                    "days": "R",
                    "place": "David Turpin Building A102",
                    "time": "4:30 pm - 5:20 pm",
                    "instructor": "TBA",
                    "crn": "22043",
                },
                {
                    "type": "Tutorial",
                    "section": "T03",
                    "days": "F",
                    "place": "David Turpin Building A102",
                    "time": "2:30 pm - 3:20 pm",
                    "instructor": "TBA",
                    "crn": "22044",
                },
                {
                    "type": "Tutorial",
                    "section": "T04",
                    "days": "F",
                    "place": "David Turpin Building A102",
                    "time": "3:30 pm - 4:20 pm",
                    "instructor": "TBA",
                    "crn": "22045",
                },
            ],
        },
    }

    selected_courses = [Course("MATH", "200"), Course("MATH", "204")]

    # 6 tables by default
    # R 17 rejects 2
    # T 16.5 is on border but doesn't reject any
    day_lengths = {
        "M": (0, 24),
        "T": (0, 16.5),
        "W": (0, 24),
        "R": (0, 17),
        "F": (0, 24),
    }

    # puts info in Course objects
    for course in selected_courses:
        for type_ in courses_info[course.name + course.num]:
            for section in courses_info[course.name + course.num][type_]:

                # get section
                s = Section()
                s.course_name = course.name
                s.course_num = course.num
                s.section = section["section"]
                s.days = section["days"]
                s.place = section["place"]
                s.setTime(section["time"])
                s.instructor = section["instructor"]
                s.crn = section["crn"]

                # put in course
                exec("course." + type_ + ".append(s)")

    expected = {
        (
            ((8.5, 12, "MATH200", "A01"),),
            ((13.5, 14.5, "MATH204", "A01"), (15.5, 16.5, "MATH200", "T01", "T02")),
            ((13.5, 14.5, "MATH204", "A01"),),
            ((8.5, 12, "MATH200", "A01"),),
            ((13.5, 14.5, "MATH204", "A01"), (14.5, 15.5, "MATH204", "T03")),
        ),
        (
            ((8.5, 12, "MATH200", "A01"),),
            ((13.5, 14.5, "MATH204", "A01"), (15.5, 16.5, "MATH200", "T01", "T02")),
            ((13.5, 14.5, "MATH204", "A01"),),
            ((8.5, 12, "MATH200", "A01"),),
            ((13.5, 14.5, "MATH204", "A01"), (15.5, 16.5, "MATH204", "T01", "T04")),
        ),
        (
            ((8.5, 12, "MATH200", "A01"),),
            ((8.5, 9.5, "MATH204", "A02"), (15.5, 16.5, "MATH200", "T01", "T02")),
            ((8.5, 9.5, "MATH204", "A02"),),
            ((8.5, 12, "MATH200", "A01"),),
            ((8.5, 9.5, "MATH204", "A02"), (15.5, 16.5, "MATH204", "T01", "T04")),
        ),
        (
            ((8.5, 12, "MATH200", "A01"),),
            ((8.5, 9.5, "MATH204", "A02"), (15.5, 16.5, "MATH200", "T01", "T02")),
            ((8.5, 9.5, "MATH204", "A02"),),
            ((8.5, 12, "MATH200", "A01"),),
            ((8.5, 9.5, "MATH204", "A02"), (14.5, 15.5, "MATH204", "T03")),
        ),
    }

    tables = calculate_tables(selected_courses, day_lengths)

    # show all 6 tables
    # for table in tables:
    #     print(table)
    #     print()

    # this line takes considerable time
    assert expected == set(deep_tuple(tables)), "calculate_tables failed"
