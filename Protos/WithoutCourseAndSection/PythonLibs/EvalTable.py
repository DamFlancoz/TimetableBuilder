'''
deepcopy copies all list values instead of pointers so
you don't change list unintentionally during runtime
it also copies listes and itms inside the given list unlike copy.

eg. let t=[[]]
    table = t + []

    only makes new list but the lists inside are still connected
    i.e. t[0] is table[0]
'''
from copy import deepcopy

'''
Error for if a class doesnot fit in a timetable
'''
class NotFit(Exception):
    pass

'''
Converts time from webscraper to tuple of start and end integers.
eg. '8:30 am - 9:50 am' = (8.5, 10)
'''
def getTime(time):
    time = time.split(' - ') #[['3:30 pm','4:30 pm']

    for i in range(2): # for start and end term
        t = time[i][:5].split(':') #takes'3:30 ' or '10:50'
        t[0] = int(t[0].strip())

        if '30' in t[1].strip() or '20' in t[1].strip(): t[0] += 0.5
        elif '50' in t[1].strip() : t[0] += 1
        
        if 'pm' in time[i] and t[0] != 12 :t[0]+=12

        time[i] = t[0]
    return tuple(time)

'''
Checks timings for courses and inserts them table.
Raises NotFit Error if any class on a day cannot fit in.

inserts - [start,end,course+courseno.,section]
eg. [12.5,13.5,'MATH101','T01]
'''
def insertInTable(course,section,day,time,table):
    days={'M':0,'T':1,'W':2,'R':3,'F':4} #index for days in table

    #inserting in free day
    if table[days[day]]==[]:
        table[days[day]].insert(0,[time[0],time[1],course[0]+course[1],section])

    #inserting at start of day
    elif table[days[day]][0][0] >= time[1]:
        table[days[day]].insert(0,[time[0],time[1],course[0]+course[1],section])
        
    else:
        #inserting during the day
        for i in range(len(table[days[day]])-1):
            if table[days[day]][i][1] <= time[0] and table[days[day]][i+1][0] >= time[1]:
                table[days[day]].insert(i+1,[time[0],time[1],course[0]+course[1],section])
                break

        #inserting at end of day
        else:
            if table[days[day]][-1][1] <= time[0]:
                table[days[day]].append([time[0],time[1],course[0]+course[1],section])
            else:
                raise NotFit()
    return table

'''
Inserts in a class which has same timings as another inserted class
'''
def insertSameInTable(section,time,table):
    days={'M':0,'T':1,'W':2,'R':3,'F':4} #index for days in table

    for day in section['days']:
        for i in range(len(table[days[day]])):
            if table[days[day]][i][0] == time[0] and time[1] == table[days[day]][i][1]:
                table[days[day]][i].append(section['section'])
                break
     
    return table

def evalTable(selectedCourses,coursesInfo,tables):

    #Acts as buffer for new tables made in each type for each section
    newTables={}
    
    for course in selectedCourses:
        for Type in coursesInfo[course[0]+course[1]]:
            for section in coursesInfo[course[0]+course[1]][Type]:
                 for i,t in enumerate(tables):

                    #[start,end] eg [11,13.5] for'11am-1:20pm'
                    time = getTime(section['time'])

                    if not (time,section['days'],i) in newTables:
                        table = deepcopy(t)

                        try:
                            for day in section['days']:
                                table = insertInTable(course,section['section'],day,time,table)

                            newTables[(time,section['days'],i)]= table
                            
                        except NotFit:
                            continue
                    else:
                        newTables[(time,section['days'],i)] = insertSameInTable(section,time,newTables[(time,section['days'],i)])
                        
            # If at start you dont check this and labs are []
            # it makes table [] but you want it to remain a
            # free table (default value) so loop for tables can run.

            if newTables != {}:
                tables = [newTables[i] for i in newTables]
                newTables = {}

    return tables

'''
Tests if function performs its intended use

TableEval uses dictionaries so there is a chance that it will provide
same tables in different orders. Must be kept in mind when using different
system or IDE
'''

def test_evalTable():
    coursesInfo = {'MATH200': {'labs': [],
  'lectures': [{'type': 'Lecture',
    'section': 'A01',
    'days': 'MR',
    'place': 'Hickman Building 105',
    'time': '8:30 am - 11:50 pm',
    'instructor': 'Andrew   McEachern (P)',
    'crn': '22034'}],
  'tutorials': [{'type': 'Tutorial',
    'section': 'T01',
    'days': 'T',
    'place': 'Clearihue Building A212',
    'time': '3:30 pm - 4:20 pm',
    'instructor': 'TBA',
    'crn': '22035'},
   {'type': 'Tutorial',
    'section': 'T02',
    'days': 'T',
    'place': 'Cornett Building A121',
    'time': '3:30 pm - 4:20 pm',
    'instructor': 'TBA',
    'crn': '22036'}]},
 'MATH204': {'labs': [],
  'lectures': [{'type': 'Lecture',
    'section': 'A01',
    'days': 'TWF',
    'place': 'David Strong Building C103',
    'time': '1:30 pm - 2:20 pm',
    'instructor': 'Muhammad   Awais (P)',
    'crn': '22040'},
   {'type': 'Lecture',
    'section': 'A02',
    'days': 'TWF',
    'place': 'David Turpin Building A104',
    'time': '8:30 am - 9:20 am',
    'instructor': 'Slim   Ibrahim (P)',
    'crn': '22041'}],
  'tutorials': [{'type': 'Tutorial',
    'section': 'T01',
    'days': 'F',
    'place': 'David Turpin Building A110',
    'time': '3:30 pm - 4:20 pm',
    'instructor': 'TBA',
    'crn': '22042'},
   {'type': 'Tutorial',
    'section': 'T02',
    'days': 'R',
    'place': 'David Turpin Building A102',
    'time': '4:30 pm - 5:20 pm',
    'instructor': 'TBA',
    'crn': '22043'},
   {'type': 'Tutorial',
    'section': 'T03',
    'days': 'F',
    'place': 'David Turpin Building A102',
    'time': '2:30 pm - 3:20 pm',
    'instructor': 'TBA',
    'crn': '22044'},
   {'type': 'Tutorial',
    'section': 'T04',
    'days': 'F',
    'place': 'David Turpin Building A102',
    'time': '3:30 pm - 4:20 pm',
    'instructor': 'TBA',
    'crn': '22045'}]}}

    selectedCourses=[['MATH','200'],['MATH','204']]
    tables = [[[],[],[],[],[]]]
    
    expected = [[[[8.5, 12, 'MATH200', 'A01']],
  [[13.5, 14.5, 'MATH204', 'A01'], [15.5, 16.5, 'MATH200', 'T01', 'T02']],
  [[13.5, 14.5, 'MATH204', 'A01']],
  [[8.5, 12, 'MATH200', 'A01'], [16.5, 17.5, 'MATH204', 'T02']],
  [[13.5, 14.5, 'MATH204', 'A01']]],
 [[[8.5, 12, 'MATH200', 'A01']],
  [[8.5, 9.5, 'MATH204', 'A02'], [15.5, 16.5, 'MATH200', 'T01', 'T02']],
  [[8.5, 9.5, 'MATH204', 'A02']],
  [[8.5, 12, 'MATH200', 'A01'], [16.5, 17.5, 'MATH204', 'T02']],
  [[8.5, 9.5, 'MATH204', 'A02']]],
 [[[8.5, 12, 'MATH200', 'A01']],
  [[13.5, 14.5, 'MATH204', 'A01'], [15.5, 16.5, 'MATH200', 'T01', 'T02']],
  [[13.5, 14.5, 'MATH204', 'A01']],
  [[8.5, 12, 'MATH200', 'A01']],
  [[13.5, 14.5, 'MATH204', 'A01'], [14.5, 15.5, 'MATH204', 'T03']]],
 [[[8.5, 12, 'MATH200', 'A01']],
  [[13.5, 14.5, 'MATH204', 'A01'], [15.5, 16.5, 'MATH200', 'T01', 'T02']],
  [[13.5, 14.5, 'MATH204', 'A01']],
  [[8.5, 12, 'MATH200', 'A01']],
  [[13.5, 14.5, 'MATH204', 'A01'], [15.5, 16.5, 'MATH204', 'T01', 'T04']]],
 [[[8.5, 12, 'MATH200', 'A01']],
  [[8.5, 9.5, 'MATH204', 'A02'], [15.5, 16.5, 'MATH200', 'T01', 'T02']],
  [[8.5, 9.5, 'MATH204', 'A02']],
  [[8.5, 12, 'MATH200', 'A01']],
  [[8.5, 9.5, 'MATH204', 'A02'], [15.5, 16.5, 'MATH204', 'T01', 'T04']]],
 [[[8.5, 12, 'MATH200', 'A01']],
  [[8.5, 9.5, 'MATH204', 'A02'], [15.5, 16.5, 'MATH200', 'T01', 'T02']],
  [[8.5, 9.5, 'MATH204', 'A02']],
  [[8.5, 12, 'MATH200', 'A01']],
  [[8.5, 9.5, 'MATH204', 'A02'], [14.5, 15.5, 'MATH204', 'T03']]]]

    tables = evalTable(selectedCourses,coursesInfo,tables)

    for i in expected:
        if i not in tables:
            break
        else:
            tables.remove(i) 
    else:
        if tables==[]: return 'pass'

    return 'Error detected'
        

if __name__=='__main__':
    print test_evalTable()

    



