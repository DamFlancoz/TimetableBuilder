from copy import deepcopy
class NotFit(Exception):
    pass

coursesInfo =   {'MATH200':
                 {'labs': [],
                  'lectures': [{'type': 'Lecture', 'section': 'A01',
                               'days': 'MR', 'place': 'Hickman Building 105',
                               'time': '8:30 am - 11:50 pm',
                               'instructor': 'Andrew   McEachern (P)',
                               'crn': '22034'}],
                  'tutorials': [{'type': 'Tutorial', 'section': 'T01',
                                 'days': 'T', 'place': 'Clearihue Building A212',
                                 'time': '3:30 pm - 4:20 pm', 'instructor': 'TBA',
                                 'crn': '22035'},
                                {'type': 'Tutorial', 'section': 'T02',
                                 'days': 'T', 'place': 'Cornett Building A121',
                                 'time': '3:30 pm - 4:20 pm', 'instructor': 'TBA',
                                 'crn': '22036'}]}
                 ,'MATH204':
                 {'labs': [],
                  'lectures': [{'type': 'Lecture', 'section': 'A01', 'days': 'TWF'
                               , 'place': 'David Strong Building C103',
                               'time': '1:30 pm - 2:20 pm',
                               'instructor': 'Muhammad   Awais (P)',
                               'crn': '22040'},
                              {'type': 'Lecture', 'section': 'A02', 'days': 'TWF'
                               , 'place': 'David Turpin Building A104',
                               'time': '8:30 am - 9:20 am',
                               'instructor': 'Slim   Ibrahim (P)',
                               'crn': '22041'}],
                  'tutorials': [{'type': 'Tutorial', 'section': 'T01',
                                 'days': 'F',
                                 'place': 'David Turpin Building A110',
                                 'time': '3:30 pm - 4:20 pm', 'instructor': 'TBA'
                                 , 'crn': '22042'},
                                {'type': 'Tutorial', 'section': 'T02',
                                 'days': 'R',
                                 'place': 'David Turpin Building A102',
                                 'time': '4:30 pm - 5:20 pm', 'instructor': 'TBA'
                                 , 'crn': '22043'},
                                {'type': 'Tutorial','section': 'T03',
                                 'days': 'F',
                                 'place': 'David Turpin Building A102',
                                 'time': '2:30 pm - 3:20 pm',
                                 'instructor': 'TBA', 'crn': '22044'},
                                {'type': 'Tutorial', 'section': 'T04',
                                 'days': 'F',
                                 'place': 'David Turpin Building A102',
                                 'time': '3:30 pm - 4:20 pm', 'instructor': 'TBA'
                                 , 'crn': '22045'}]}}

'''
'8:30 am - 9:50 am' = [8.5, 10]
'''
def getTime(section):
    time = section['time'].split(' - ') #[['3:30 pm','4:30 pm']

    for i in range(2): # for start and end term
        t = time[i][:5].split(':')#takes'3:30 ' or '10:50'
        t[0] = int(t[0].strip())

        if '30' in t[1].strip() or '20' in t[1].strip(): t[0] += 0.5
        elif '50' in t[1].strip() : t[0] += 1
        
        if 'pm' in time[i] and t[0] != 12 :t[0]+=12

        time[i] = t[0]
    return tuple(time)

def insertInTable(course,section,day,time,table):
    days={'M':0,'T':1,'W':2,'R':3,'F':4} #index for days in table

    #inserting in free day
    if table[days[day]]==[]:
        table[days[day]].insert(0,[time[0],time[1],course[0]+course[1],section['section']])

    #inserting at start of day
    elif table[days[day]][0][0] >= time[1]:
        table[days[day]].insert(0,[time[0],time[1],course[0]+course[1],section['section']])
        
    else:
        #inserting during the day
        for i in range(len(table[days[day]])-1):
            if table[days[day]][i][1] <= time[0] and table[days[day]][i+1][0] >= time[1]:
                table[days[day]].insert(i+1,[time[0],time[1],course[0]+course[1],section['section']])
                break

        #inserting at end of day
        else:
            if table[days[day]][-1][1] <= time[0]:
                table[days[day]].append([time[0],time[1],course[0]+course[1],section['section']])
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

#tables=[[[None]*30] for i in range(5)]
# Otherwise *5 repeats pointer to [None]*30 so all the inner lists
# are connected

'''
tables stores list of table elements
table is a list of days which each store list of classes that day
[M,T,W,R,F]
M = [[8.5, 10, 'MATH200', 'A01'],[8.5, 9.5, 'MATH204', 'A02']]
each class elements forms, [start,end,course,section] to trace it back
'''
tables=[[[],[],[],[],[]]] #single table with all free days to start
newTables={}           #Acts as buffer for new tables made in each type for each section
selectedCourses=[['MATH','200'],['MATH','204']]


for course in selectedCourses:
    print ('course in')
    for Type in coursesInfo[course[0]+course[1]]:
        print ('_type in')
        for section in coursesInfo[course[0]+course[1]][Type]:
             print ('section in',len(coursesInfo[course[0]+course[1]][Type]))
             print ('Tables len:',len(tables))
             for i,t in enumerate(tables):
                    print (1)

                    #[start,end] eg [11,13.5] for'11am-1:30pm'
                    time = getTime(section)
                    
                    if not (time,section['days'],i) in newTables:
                        table = deepcopy(t)
                        print (table)

                        try:
                            for day in section['days']:
                                table = insertInTable(course,section,day,time,table)

                            newTables[(time,section['days'],i)]= table
                            print('added',len(newTables),i)

                        except NotFit:
                            print('NotFit')
                            continue
                        
                    else:
                        print( 'same insert')
                        newTables[(time,section['days'],i)] = insertSameInTable(section,time,newTables[(time,section['days'],i)])
             print ('section out')
        print ('_type out')
        
        if coursesInfo[course[0]+course[1]][Type] != []:
                tables = [newTables[i] for i in newTables]
                newTables = {}
    print ('course out')








