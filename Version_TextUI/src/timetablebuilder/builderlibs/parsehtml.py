"""Contains put_sections_in_course, used to parse html and complete Course Object"""

from bs4 import BeautifulSoup as bSoup

from src.timetablebuilder.builderlibs.builderclasses import Section, Course


def put_sections_in_course(course, course_page_html):
    """
    Puts corresponding Section Object from html page of course.

    Args:
        course (Course Object): course to put in the sections.
        course_page_html (str): html of course's page which contains sections.
    """

    page_soup = bSoup(course_page_html, "lxml")  # parsed html, soup

    # get table with sections in it
    section_table = page_soup.findAll("table", class_="datadisplaytable")[0]

    # Each section has 4 index associated,
    # - header/title, (i)
    # - other info,   (i+1)
    # - header for time, days etc. inside other info (i+2)
    # - values for time, days etc. inside other info (i+3)
    section_list = section_table.findAll("tr")

    # parses sections
    for i in range(0, len(section_list), 4):
        if "Main Campus" in str(section_list[i + 1]):
            section = Section()

            title_list = str(section_list[i]).split(" - ")
            section.section = title_list[3][:3]  # some tags were also coming at the end
            section.crn = title_list[1]

            course_name = title_list[2].split(" ")  # eg ['CSC','111']
            section.course_name = course_name[0]
            section.course_num = course_name[1]

            info = section_list[i + 3].findAll("td")
            section.setTime(str(info[1].text))  # turns str time to tuple
            section.days = str(info[2].text)
            section.place = str(info[3].text)
            section.instructor = str(info[6].text)

            if str(info[5].text) == "Lab":
                course.labs.append(section)
            elif str(info[5].text) == "Lecture":
                course.lectures.append(section)
            elif str(info[5].text) == "Tutorial":
                course.tutorials.append(section)

    return course
