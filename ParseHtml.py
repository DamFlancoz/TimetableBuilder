from WebScrapper import getPage
from bs4 import BeautifulSoup as bSoup

def getCourse(term,course,courseNo):
    pageHtml = getPage(term,course,courseNo) # html page, str
    pageSoup = bSoup(pageHtml,'lxml')       # parsed html, soup

    '''
    Gives back table of all classes and other tables in list. [0] takes needed
    table.
    '''
    sectionTable = pageSoup.findAll('table',class_="datadisplaytable")[0]

    '''
    Each class has 4 index associated,
    - header/title, (i)
    - other info,   (i+1)
    - header for time, days etc. inside other info (i+2)
    - values for time, days etc. inside other info (i+3)
    '''
    sectionList = sectionTable.findAll('tr')

    lectures = []
    labs = []
    tutorials = []

    # parses sections
    for i in range(0,len(sectionList),4):
        if 'Main Campus' in str(sectionList[i+1]):
            section = {}
            
            titleList = str(sectionList[i]).split(' - ')
            section['section'] = titleList[3][:3] #some tags were also coming at the end
            section['crn'] = titleList[1]
            # can add course if needed

            info = sectionList[i+3].findAll('td')
            section['time'] = str(info[1].text)
            section['days'] = str(info[2].text)
            section['place'] = str(info[3].text)
            section['instructor'] = str(info[6].text)
            section['type'] = str(info[5].text)

            if section['type'] == 'Lab':
                labs.append(section)
            elif section['type'] == 'Lecture':
                lectures.append(section)
            elif section['type'] == 'Tutorial':
                tutorials.append(section)
    return {'lecture':lectures,'labs':labs,'tutorials':tutorials} # dict of course


def test_getCourse():
    '''
    Case of CSC11, 2019 jan-term
    '''
    expected = {'labs': [{'section': 'B01', 'type': 'Lab', 'days': 'W', 'place': 'Engineering Comp Science Bldg 242', 'time': '11:30 am - 1:20 pm', 'instructor': 'TBA', 'crn': '20638'}, {'name': 'B02', 'type': 'Lab', 'days': 'W', 'place': 'Engineering Comp Science Bldg 242', 'time': '1:30 pm - 3:20 pm', 'instructor': 'TBA', 'crn': '20639'}, {'name': 'B03', 'type': 'Lab', 'days': 'W', 'place': 'Engineering Comp Science Bldg 242', 'time': '3:30 pm - 5:20 pm', 'instructor': 'TBA', 'crn': '20640'}], 'lecture': [{'name': 'A01', 'type': 'Lecture', 'days': 'MR', 'place': 'Engineering Comp Science Bldg 125', 'time': '10:00 am - 11:20 am', 'instructor': 'William Herbert  Bird (P)', 'crn': '20636'}, {'name': 'A02', 'type': 'Lecture', 'days': 'MR', 'place': 'Engineering Comp Science Bldg 125', 'time': '10:00 am - 11:20 am', 'instructor': 'William Herbert  Bird (P)', 'crn': '20637'}], 'tutorials': []}
    
    getting = getCourse('201901','CSC','111')
    
    return getting == expected




