from WebScrapper import getPage
from bs4 import BeautifulSoup as bSoup
        

pageHtml = getPage('201901','CSC','111')
with open('a.html','w') as t:
    t.write(pageHtml)

pageSoup = bSoup(pageHtml,'lxml') # parsed html


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
        section['name'] = titleList[3][:3] #some tags were also coming at the end
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



'''
header values in class (i+2)
<tr>
<th class="ddheader" scope="col">Type</th>
<th class="ddheader" scope="col">Time</th>
<th class="ddheader" scope="col">Days</th>
<th class="ddheader" scope="col">Where</th>
<th class="ddheader" scope="col">Date Range</th>
<th class="ddheader" scope="col">Schedule Type</th>
<th class="ddheader" scope="col">Instructors</th>
</tr>
'''

'''
MainDict    TO BE CREATED
-key class eg. CSC 111, seperate for lecture and tutorial
- conintains list of sections (dicts)

Section dicts of a course
- crn
- name, eg. 'A01'
- time, eg. '10:00 am - 11:20 am'
- days, eg. 'MR'
- place eg. 'Engineering Comp Science Bldg 125'
- instructor
- type, eg. 'Lab'
'''





