"""Contains get_page, used to get course's sections html from web."""


from urllib.request import urlopen

from builderlibs.exceptions import NoSectionsAvailableOnline
from builderlibs.builderclasses import Course


def get_course_html(term, course):
    """
    Gets the Course html from web which contains its sections for the term.

    Args:
        term (str): code for the term to use. eg '201901'
        course (Course Object): course to search sections for.

    Returns:
        str: Html of page containing given course's sections.

    Raises:
        NoSectionsAvailableOnline: if page with no sections is found.
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
    )  # data contains course.name and course.num further down

    html_page = urlopen(url=url, data=data.encode()).read().decode()
    html_lines = html_page.split("\n")

    if (
        html_lines[103] == "No classes were found that meet your search criteria"
        or html_lines[102] == "No classes were found that meet your search criteria"
    ):
        raise (NoSectionsAvailableOnline(course))

    return html_page
