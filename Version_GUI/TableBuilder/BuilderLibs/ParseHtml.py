from bs4 import BeautifulSoup as bSoup

from PythonLibs.Course_Section_Classes import Section, Courses

"""
takes: term and Course Object
returns: same Course Object with info filled in
"""


def put_sections_in_course(course, coursePageHtml):

    page_soup = bSoup(coursePageHtml, "lxml")  # parsed html, soup

    """
    Gives back table of all classes and other tables in list. [0] takes needed
    table.
    """
    section_table = page_soup.findAll("table", class_="datadisplaytable")[0]

    """
    Each class has 4 index associated,
    - header/title, (i)
    - other info,   (i+1)
    - header for time, days etc. inside other info (i+2)
    - values for time, days etc. inside other info (i+3)
    """
    section_list = section_table.findAll("tr")

    # parses sections
    for i in range(0, len(section_list), 4):
        if "Main Campus" in str(section_list[i + 1]):
            section = Section()

            title_list = str(section_list[i]).split(" - ")
            section.section = title_list[3][:3]  # some tags were also coming at the end
            section.crn = title_list[1]

            course_name = title_list[2].split(" ")  # eg ['CSC','111']
            section.cName = course_name[0]
            section.cNum = course_name[1]

            info = section_list[i + 3].findAll("td")
            section.setTime(str(info[1].text))  # turns str time to tuple
            section.days = str(info[2].text)
            section.place = str(info[3].text)
            section.instructor = str(info[6].text)

            # str(info[5].text) tells if class is lecture/lab/tutorial

            if str(info[5].text) == "Lab":
                course.labs.append(section)
            elif str(info[5].text) == "Lecture":
                course.lectures.append(section)
            elif str(info[5].text) == "Tutorial":
                course.tutorials.append(section)

    return course


def Test_getCourse():
    """
    Case of CSC111, 2019 jan-term
    """

    with open("TestParserPage_CSC111Spring2019.html", "r") as t:
        coursePageHtml = t.read()

    getting = put_sections_in_course(
        Course("CSC", "111"), coursePageHtml
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

    return str(getting) == expected


if __name__ == "__main__":

    from Course_Section_Classes import *

    print(Test_getCourse())
