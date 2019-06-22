'''
This scrapes Uvic site for info on requested course (just a single page).
Use get_course_info.
'''

from urllib.request import urlopen
from bs4 import BeautifulSoup as bSoup

from .classes import Course,Section,NoSectionsAvailableOnline

def get_course_info(term, course):
    '''
    Acts as a interface to outside.

    Args:
        term (int/str): Representation of a specific term as per Uvic.
            eg. '201901' for spring 2019 term.

        course (list): List representation of course.
            eg. ['MATH',101]

    Return:
        Course Object: This contains all info for the course.

    Raises:
        NoSectionsAvailableOnline: if get_page cannot find such section.
    '''
    course = Course(course[0],course[1])
    page = get_page(term, course)
    return parse_course_html(course, page)




def get_page(term, course):
    '''
    Used to get html page with course information from Uvic to parse.

    Args:
        term (int/str): Representation of a specific term as per Uvic.
            eg. '201901' for spring 2019 term.

        course (Course Object): Should contain course name and course no.

    Returns:
        str: The html page containing classes information.

    Raises:
        NoSectionsAvailableOnline: if course is not found online.
    '''

    url = "https://www.uvic.ca/BAN1P/bwckschd.p_get_crse_unsec"
    data = (
        "term_in="
        + term
        + "&sel_subj=dummy&sel_day=dummy&sel_schd=dummy&sel_insm=dummy&sel_camp=dummy&sel_levl=dummy&sel_sess=dummy&sel_instr=dummy&sel_ptrm=dummy&sel_attr=dummy&sel_subj="
        + course.name
        + "&sel_crse="
        + course.num
        + "&sel_title=&sel_schd=%25&sel_insm=%25&sel_from_cred=&sel_to_cred=&sel_camp=%25&sel_levl=%25&sel_ptrm=%25&sel_instr=%25&begin_hh=0&begin_mi=0&begin_ap=a&end_hh=0&end_mi=0&end_ap=a"
    )

    html_page = urlopen(url=url, data=data.encode()).read().decode()
    html_lines = html_page.split("\n")

    if (
        html_lines[103] == "No classes were found that meet your search criteria"
        or html_lines[102] == "No classes were found that meet your search criteria"
    ):
        raise (NoSectionsAvailableOnline(course))

    return html_page

def parse_course_html(course, course_page_html):
    '''
    Parses the html page To fill course information in Course Object and
    return it.

    Args:
        course (Course Object): Should contain course name and course no.
        course_page_html: Should be of valid format Uvic uses.

    Returns:
        Course Object: Contains all labs, tutorials and lecture info available.
    '''

    page_soup = bSoup(course_page_html, "lxml")  # parsed html, soup


    # Gives back table of all classes and other tables in list. [0] takes needed
    # table.
    section_table = page_soup.findAll("table", class_="datadisplaytable")[0]

    # Each class has 4 index associated,
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
