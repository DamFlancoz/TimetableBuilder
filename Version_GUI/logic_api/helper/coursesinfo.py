"""
This scrapes Uvic site for info on requested course (just a single page).
Use get_course_info.
"""

from urllib.request import urlopen
from bs4 import BeautifulSoup as bSoup

from ..models import Course_db, Section_db
from .classes import Course, Section, NoSectionsAvailableOnline


def delete_course_to_db(term, course):
    """
    Deletes given course from database. Not used in any view, must be invoked manually.

    Args:
        term (str): Code for term course is given.
        course (Course Object/tuple): Course Object with name and num or tuple with name
            and num as first and second elements of course to be deleted.

    Returns:
        None: Saves the given Course Object.

    Raises:
        Course_db.DoesNotExist: if course is not found.
    """
    if type(course) != Course:
        course = Course(course[0], course[1])

    Course_db.objects.get(  # pylint:disable=no-member
        term=term, name=course.name, num=course.num
    ).delete()


def get_course_info(term, course):
    """
    Gets the required course. May need to retrieve it from web.

    Args:
        term (str): Code for term course is given.
        course (Course Object/tuple): Course Object with name and num or tuple with name
            and num as first and second elements of needed course.

    Returns:
        Course Object: Asked course.

    Raises:
        NoSectionsAvailableOnline: if get_page cannot find such section.
    """
    if type(course) != Course:
        course = Course(course[0], course[1])

    try:
        return retreive_course_from_db(term, course)

    except Course_db.DoesNotExist:  # pylint:disable=no-member
        course = get_course_info_from_web(term, course)
        save_course_to_db(term, course)
        return course


def save_course_to_db(term, course):
    """
    Saves given course to database

    Args:
        term (str): Code for term course is given.
        course (Course Object): Course Object to save.

    Returns:
        None: Saves the given Course Object.
    """
    c = Course_db(term=term, name=course.name, num=course.num)
    c.save()

    for t, type_ in zip(("LE", "LA", "TU"), course):
        for section in type_:
            c.section_db_set.create(  # pylint:disable=no-member
                type=t,
                section=section.section,
                crn=section.crn,
                sTime=section.time[0],
                eTime=section.time[1],
                days=section.days,
                place=section.place,
                instructor=section.instructor,
            )


def retreive_course_from_db(term, course):
    """
    Retrieves Course from database as a Course Object

    Args:
        term (str): Code for term course is given.
        course (Course Object): Course Object with name and number.

    Returns:
        Course Object: asked course.

    Raises:
        Course_db.DoesNotExist: if course is not found.
    """
    course_db = Course_db.objects.get(  # pylint:disable=no-member
        term=term, name=course.name, num=course.num
    )

    course = Course(course_db.name, course_db.num)

    course.lectures = retreive_sections_from_db(
        course, course_db.section_db_set.filter(type="LE")
    )

    course.labs = retreive_sections_from_db(
        course, course_db.section_db_set.filter(type="LA")
    )

    course.tutorials = retreive_sections_from_db(
        course, course_db.section_db_set.filter(type="TU")
    )
    return course


def retreive_sections_from_db(course, sections_qset):
    """
    Takes in Section_dbs and returns a list of them converted to Section Objects

    Args:
        course (Course Object): Course Object with name and number.
        sections_qset (list/QuerySet): list of Section_dbs.

    Returns:
        list: list with all passed elements converted to Section Objects.
    """
    sections = []
    for section_db in sections_qset:
        s = Section()
        s.course_name = course.name
        s.course_num = course.num
        s.section = section_db.section
        s.crn = section_db.crn
        s.time = (float(section_db.sTime), float(section_db.eTime))
        s.days = section_db.days
        s.place = section_db.place
        s.instructor = section_db.instructor
        sections.append(s)
    return sections


def get_course_info_from_web(term, course):
    """
    Acts as a interface to scrapping and parsing and just returns the course as an
    Course Object.

    Args:
        term (int/str): Representation of a specific term as per Uvic.
            eg. '201901' for spring 2019 term.

        course (Course Object): Course Object with name and number.

    Return:
        Course Object: This contains all info for the course.

    Raises:
        NoSectionsAvailableOnline: if get_page cannot find such section.
    """
    page = get_page(term, course)
    course = parse_course_html(course, page)
    return course


def get_page(term, course):
    """
    Used to get html page with course information from Uvic to parse.

    Args:
        term (int/str): Representation of a specific term as per Uvic.
            eg. '201901' for spring 2019 term.

        course (Course Object): Should contain course name and course no.

    Returns:
        str: The html page containing classes information.

    Raises:
        NoSectionsAvailableOnline: if course is not found online.
    """

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
    """
    Parses the html page To fill course information in Course Object and
    return it.

    Args:
        course (Course Object): Should contain course name and course no.
        course_page_html: Should be of valid format Uvic uses.

    Returns:
        Course Object: Contains all labs, tutorials and lecture info available.
    """

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
