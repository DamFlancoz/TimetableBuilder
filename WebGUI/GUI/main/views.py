from django.shortcuts import render
from django.http import HttpResponse,HttpResponseBadRequest,JsonResponse # for Ajax
from django.template.loader import render_to_string #(template,context)

'''
HttpResponse(status=400), client side error, Bad Request
HttpResponseBadRequest(content), Acts just like HttpResponse but uses a 400 status code
render(request, 'template.html', status=204)
'''

# Subjects list
subjs = ['AGEI', 'ANTH', 'ART', 'AE', 'AHVS', 'ASTR', 'BIOC', 'BCMB', 'BIOL', 'BME', 'BUS', 'CS', 'CHEM',
         'CYC', 'CIVE', 'HUFA', 'COM', 'CD', 'CSC', 'EDCI', 'DR', 'EOS', 'ECON', 'ED-D', 'EDUC', 'ECE', 
         'ENGR', 'ENGL', 'ENT', 'ER', 'ES', 'EUS', 'EPHE', 'FA', 'FORB', 'FRAN', 'GNDR', 'GEOG', 'GMST', 
         'GS', 'GRS', 'HINF', 'HLTH', 'HS', 'HSTR', 'HDCC', 'ICDG', 'IED', 'IGOV', 'IN', 'INGH', 'IS', 
         'IET', 'INTD', 'IB', 'INTS', 'KINE', 'LAS', 'LAW', 'LING', 'MRNE', 'MGB', 'MBA', 'MATH', 'MECH',
          'MEDS', 'MEDI', 'MICR', 'MUS', 'NRSC', 'NURS', 'NUNP', 'NUHI', 'PAAS', 'PHIL', 'PHYS', 'POLI', 
          'PSYC', 'ADMN', 'PADR', 'PHSP', 'RHED', 'RS', 'SMGT', 'SLST', 'SDH', 'SJS', 'SOCW', 'SOCI', 
          'SENG', 'SPAN', 'STAT', 'TS', 'THEA', 'VIRS', 'WKEX', 'WRIT']


# Create your views here.
def main(request):

    #termOptions = getTermOptions()
    termOptions = ['201901','201905','201909']

    context={
        'termOptions':termOptions,
        'subjs':subjs,
        'days':['M','T','W','R','F']
    }

    return render(request,'main/main.html',context)


#Helper
def getTermOptions():
    pass

def handleApi(request):
    pass
