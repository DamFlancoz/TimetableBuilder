from django.shortcuts import render
from django.http import HttpResponse,HttpResponseBadRequest,JsonResponse # for Ajax
from django.template.loader import render_to_string #(template,context)

'''
HttpResponse(status=400), client side error, Bad Request
HttpResponseBadRequest(content), Acts just like HttpResponse but uses a 400 status code
render(request, 'template.html', status=204)
'''

# Create your views here.
'''
Takes : POST request with selectedCourses and Day constraints
return : json (list) tables

take sample
{
    'selectedCourses':[
        ['MATH',101],
        ['MATH',110],
        <other courses>
    ],
    'dayConstr':[
        [0,24],
        [2,8],
        <for other days>
    ]
}

return sample
{
    'message':<massage>,
    'tables':[
        {
           'html':<table in html>
           'sections':[
               ['Math101',['A01','A02'],[<crns in same order>]],
               ['Math110',['A01'],[<crn>]],
               <other sections>
           ]
        
        },
        <tables2>
    ]
}
'''
def handleApi(request):
    return HttpResponse('Hello World!')

'''
Takes : POST request with selectedCourses and Day constraints
return : json (list) tables

take sample
{
    'term':201905,
    'cName':'MATH',
    'cNum':101
}

return sample
{
    'message':<massage>,
    'data':{
        'html':<table in html>,
        'course': 'MATH 101'    
    }
}
'''
def cInfoApi(request):
    
    term = request.GET['term']
    cName = request.GET['cName']
    cNum = request.GET['cNum']

    print([term,cName,cNum])

    data = {
        'html':'content<br/>content<br/>content<br/>content<br/>content',
        'course': cName + ' ' + cNum   
    }

    return JsonResponse(data)

