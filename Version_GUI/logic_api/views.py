from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse  # for Ajax
from django.template.loader import render_to_string  # (template,context)

from .helper.coursesinfo import get_course_info, NoSectionsAvailableOnline

"""
HttpResponse(status=400), client side error, Bad Request
HttpResponseBadRequest(content), Acts just like HttpResponse but uses a 400 status code
render(request, 'template.html', status=204)
"""

# Create your views here.
def handleApi(request):
    """Test api"""
    return HttpResponse("Hello World!")


def cInfoApi(request):
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
        "course": course.name + course.num,
        "lectures": [
            {
                "name": s.section,
                "time": s.time,
                "days": s.days,
                "instructor": s.instructor,
            }
            for s in course.lectures
        ],
        "labs": [
            {
                "name": s.section,
                "time": s.time,
                "days": s.days,
                "instructor": s.instructor,
            }
            for s in course.labs
        ],
        "tutorials": [
            {
                "name": s.section,
                "time": s.time,
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


def getTableApi(request):

    # term = request.GET["term"]
    """
    courses = {'Math101':[sections], 'CSC111':[sections]}
    """
    # selected_courses = request.GET["selectedCourses"]
    # day_constraints = request.GET["dayConstraints"]

    context = {}

    data = {
        "message": "Success",
        "html": [render_to_string("TableBuilder/tablepanel.html", context=context)],
        "headers": [],
    }

    return JsonResponse(data)
