

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
NotFit Exception
Error for if a section doesnot fit in a timetable
'''
if not __name__ == '__main__': from .Exceptions import NotFit,NoSectionOfTypeFit


'''
Contains all the classes  
'''
if not __name__ == '__main__': from .Course_Section_Classes import Table,Course,Section

'''
return True if sectionis compatible with dayLengths
'''
def checkSectionWithDayLengths(section,dayLengths):
    for day in section.days:
        if section.time[0] < dayLengths[day][0] or section.time[1] > dayLengths[day][1]:
            return False
    else:
        return True

'''
Checks timings for section and inserts them table.
Raises NotFit Error if any class on a day cannot fit in.

inserts - [start,end,course+courseno.,section]
eg. [12.5,13.5,'MATH101','T01']
'''
def insertInTable(section,table):
    time=section.time

    #Waring this makes the lists in all days point to sam list
    #if you make change in one toInsert in one day, all of them change
    toInsert = [time[0],time[1],section.cName+section.cNum,section.section]

    for day in section.days:
        #inserting in free day
        if table[day]==[]:
            table[day].insert(0,toInsert)
    
        #inserting at start of day
        elif table[day][0][0] >= time[1]:
            table[day].insert(0,toInsert)
            
        else:
            #inserting during the day
            for i in range(len(table[day])-1):
                if table[day][i][1] <= time[0] and table[day][i+1][0] >= time[1]:
                    table[day].insert(i+1,toInsert)
                    break
    
            #inserting at end of day
            else:
                if table[day][-1][1] <= time[0]:
                    table[day].append(toInsert)
                else:
                    raise NotFit()

    table.sections.append([section])
    
    return table

'''
Inserts in a section which has same timings as another inserted class
eg. [12.5,13.5,'MATH101','T01'] to [12.5,13.5,'MATH101','T01','T02']
'''
def insertSameInTable(section,table):
    time = section.time
    day = section.days[0]

    # you dont need to add section to each day since all of them
    # point to same list
    for i in range(len(table[day])):
        if table[day][i][0] == time[0] and time[1] == table[day][i][1]:
            table[day][i].append(section.section)
            break
    
    for s in table.sections:
        if s[0] == section:
            s.append(section)
            break
     
    return table

def evalTable(selectedCourses,dayLengths):

    tables = [Table()] #free weekby default

    #Acts as buffer for new tables made in each type for each section
    newTables={}
    
    for course in selectedCourses:
        for Type in course:
            for section in Type:
                
                # skip if class falls out of required schedule
                if not checkSectionWithDayLengths(section,dayLengths): continue
                    
                for i,t in enumerate(tables):

                    

                    # i is in newTables[(time,section.days,i)] so that a section does keep puting itself
                    #  eg 'A01' in next iterations of tables sees its previous entry in new tables and puts
                    #      itself wih it again.
                    # But it allows other section with same day and time to find the table 

                    #[start,end] eg [11,13.5] for'11am-1:20pm'
                    time = section.time

                    if not (time,section.days,i) in newTables:
                        table = deepcopy(t)

                        try:
                            table = insertInTable(section,table)

                            newTables[(time,section.days,i)]= table
                            
                        except NotFit:
                            continue
                    else:
                        newTables[(time,section.days,i)] = insertSameInTable(section,newTables[(time,section.days,i)])
                        
            # if no section of a type can be added then
            if  (not newTables) and Type: raise NoSectionOfTypeFit(course)
            
            # If at start a Type is [] it makes table [] in comprehension
            # but you want it to remain a free table (default value) so loop 
            # for tables can run.
                        
            tables = list(newTables.values()) if newTables else tables
            newTables = {}

    return tables

'''
Tests if function performs its intended use

TableEval uses dictionaries so there is a chance that it will provide
same tables in different orders. Must be kept in mind when using different
system or IDE
'''

def Test_evalTable():
        
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
    
    selectedCourses=[Course('MATH','200'),Course('MATH','204')]

    # 6 tables by default
    # R 17 rejects 2
    # T 16.5 is on border but doesnt reject any
    dayLengths = {'M':(0,24),'T':(0,16.5),'W':(0,24),'R':(0,17),'F':(0,24)}
    
    # puts info in Course objects
    for course in selectedCourses:
        for Type in coursesInfo[course.course+course.num]:
            for section in coursesInfo[course.course+course.num][Type]:
                s = Section()
                s.cName = course.course
                s.cNum = course.num
                s.section = section['section']
                s.days = section['days']
                s.place = section['place']
                s.setTime(section['time'])
                s.instructor = section['instructor']
                s.crn = section['crn']
    
                exec('course.'+Type+'.append(s)')
    

    # The tables should be following.
    # They are a set beacause order does not matter.

    expected={(((8.5, 12, 'MATH200', 'A01'),),
      ((13.5, 14.5, 'MATH204', 'A01'), (15.5, 16.5, 'MATH200', 'T01', 'T02')),
      ((13.5, 14.5, 'MATH204', 'A01'),),
      ((8.5, 12, 'MATH200', 'A01'),),
      ((13.5, 14.5, 'MATH204', 'A01'), (14.5, 15.5, 'MATH204', 'T03'))),
     (((8.5, 12, 'MATH200', 'A01'),),
      ((13.5, 14.5, 'MATH204', 'A01'), (15.5, 16.5, 'MATH200', 'T01', 'T02')),
      ((13.5, 14.5, 'MATH204', 'A01'),),
      ((8.5, 12, 'MATH200', 'A01'),),
      ((13.5, 14.5, 'MATH204', 'A01'), (15.5, 16.5, 'MATH204', 'T01', 'T04'))),
     (((8.5, 12, 'MATH200', 'A01'),),
      ((8.5, 9.5, 'MATH204', 'A02'), (15.5, 16.5, 'MATH200', 'T01', 'T02')),
      ((8.5, 9.5, 'MATH204', 'A02'),),
      ((8.5, 12, 'MATH200', 'A01'),),
      ((8.5, 9.5, 'MATH204', 'A02'), (15.5, 16.5, 'MATH204', 'T01', 'T04'))),
     (((8.5, 12, 'MATH200', 'A01'),),
      ((8.5, 9.5, 'MATH204', 'A02'), (15.5, 16.5, 'MATH200', 'T01', 'T02')),
      ((8.5, 9.5, 'MATH204', 'A02'),),
      ((8.5, 12, 'MATH200', 'A01'),),
      ((8.5, 9.5, 'MATH204', 'A02'), (14.5, 15.5, 'MATH204', 'T03')))}
    
    tables = evalTable(selectedCourses,dayLengths)
    
    # show all 6 tables
    for table in tables:
        print (table)
        print()
    
    # this line takes considerable time
    return 'Pass' if expected == set(deepTuple(tables)) else 'Error'


'''
Converts all nested iterables to tuple.
Helpful when need to convert to set from nested lists.
Used in Test_evalTable()
'''
def deepTuple(t):
    return tuple(deepTuple(i) for i in t) if type(t) == list or type(t) == Table else t



if __name__ == '__main__' :
    
    
    from Exceptions import NotFit

    from Course_Section_Classes import Table,Course,Section

    print (Test_evalTable())

    



