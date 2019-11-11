import ast

from django.http import HttpResponse, JsonResponse  # for Ajax
from django.template.loader import render_to_string  # (template,context)
from django.views.decorators.csrf import csrf_exempt
from django.utils.datastructures import MultiValueDict as m_dict

from .helper.coursesinfo import get_course_info, NoSectionsAvailableOnline
from .helper.tablebuilder import build_table, NotFit

"""
HttpResponse(status=400), client side error, Bad Request
HttpResponseBadRequest(content), Acts just like HttpResponse but uses a 400 status code
"""


def handleApi(request):
    """Test api"""
    return HttpResponse("Hello World!")


def get_cInfo(request):
    """
    Takes in term and course and returns coresponding course html (to put in tab).

    Takes: term, course_name, course_num
        eg. {
                'term':201905,
                'course_name':'MATH',
                'course_num':101
            }

    Returns: html for tab (with course info in it)
        eg. {
                'message':<massage>,
                'data':{
                    'html':<table in html>,
                    'course': 'MATH 101'
                }
            }
    """

    term = str(request.GET["term"])
    course_name = request.GET["cName"]
    course_num = str(request.GET["cNum"])

    try:
        course = get_course_info(term, (course_name, course_num))

    except NoSectionsAvailableOnline:
        print("NoSectionsAvailableOnline")
        pass  # TODO

    context = {
        "course": f"{course.name}-{course.num}",
        "lectures": [
            {
                "name": s.section,
                "formated_time": s.formated_time,
                "days": s.days,
                "instructor": s.instructor,
            }
            for s in course.lectures
        ],
        "labs": [
            {
                "name": s.section,
                "formated_time": s.formated_time,
                "days": s.days,
                "instructor": s.instructor,
            }
            for s in course.labs
        ],
        "tutorials": [
            {
                "name": s.section,
                "formated_time": s.formated_time,
                "days": s.days,
                "instructor": s.instructor,
            }
            for s in course.tutorials
        ],
    }

    data = {
        "message": "Success",
        "html": render_to_string("logic_api/coursePanel.html", context=context),
        "course": course_name + " " + course_num,
        "sections": [s.section for t in course for s in t],
    }

    return JsonResponse(data)


@csrf_exempt
def get_table(request):
    """
    Takes in courses and returns coresponding table html (to put table).

    Takes: term, course_name, course_num
        eg. {
                'selectedSections': '{
                    'MATH 101': {
                        'lab':'B01',
                        'lecture': 'A01',
                        'tutorial': '',
                    }
                }',
            }

    Returns: html for tab (with course info in it)
        eg. {
                'message':<massage>,
                'tableHTML': <html for table>,
                'error': 'None',
            }
    """

    # eg. {'CSC 111': {'lab': 'B01', 'lecture': 'A02', 'tutorial': ''}, ...}
    selected_sections = ast.literal_eval(request.POST.get("selectedSections", None))
    term = request.POST.get("term", None)
    print(term)

    try:
        html_table = build_table(term, selected_sections).to_html_table()
        return JsonResponse(
            {
                "message": "Table without css",
                "tableHTML": str(html_table),
                "error": "None",
            }
        )

    except NotFit:
        return JsonResponse(
            {
                "message": "Sections don't fit together",
                "tableHTML": "",
                "error": "courses-not-fit",
            }
        )
