'''
Working with classes:
term
rem
add
show

TODO:
Webscrapper
PageParser
TableEvalater
Add Table class
'''



'''
getCourse(term,course,courseNo)

returns - course dictionary

Stores with key = selectedCourses[i][0]+selectedCourses[i][1]
eg. 'MATH101'

Parses html to get all information
- 'section' eg. 'A01'
- 'crn'
- 'time' eg. '11:30 am - 1:20 pm'
- 'days'
- 'place' eg. 'Engineering Comp Science Bldg 242'
- 'instructor'
- 'type' eg. Lecture, Labs etc.
'''
from PythonLibs.ParseHtml import getCourse

'''
evalTable(selectedCourses,Courseinfo,tables)

Changes var tables to have tables without conflicts of
selectedCourses in it.
'''
from PythonLibs.EvalTable import evalTable

# Documentation
from PythonLibs.Course_Section_Classes import *



from time import localtime

'''
setTerm
takes - input argument for term and
return - term value equal accordingly
'''
def setTerm(inp):
    if ('next' in inp) or ('n' in inp):
                
        # gives tuple (year,month,date,h,min,s,weekday, etc.)
        time = localtime()

        if time[1] in [1,2,3,4]: # next term from may
            term = str(time[0])+ '02'

        elif time[1] in [5,6,7,8]: # next term from sept
            term = str(time[0])+ '03'

        else: #next term from jan
            term = str(time[0]+1)+ '01'

    elif ('current' in inp) or ('curr' in inp):

        # gives tuple (year,month,date,h,min,s,weekday, etc.)
        time = localtime()

        if time[1] in [1,2,3,4]: # next term from jan
            term = str(time[0])+ '01'

        elif time[1] in [5,6,7,8]: # next term from may
            term = str(time[0])+ '02'

        else: #current term from sept
            term = str(time[0])+ '03'

    elif inp.isdigit() and len(inp) == 6:
        term = inp

    return term



'''
math101/MaTh 101 = ['MATH','101']
helps in add and remove
'''
def processArgToCourse(i):
    i = i.strip().upper()

    name = ''
    num = ''
    for char in i:
        if char.isalpha(): name += char
        elif char.isdigit(): num += char

    return [name,num]



############################## Global Variables

term = '<choose term>'# term chosen
selectedCourses = []  # Course objects

'''
tables stores list of table elements
table is a list of days which each store list of classes that day
[M,T,W,R,F]
M = [[8.5, 10, 'MATH200', 'A01'],[8.5, 9.5, 'MATH204', 'A02']]
each class elements forms, [start,end,course,section] to trace it back
'''
tables=[[[],[],[],[],[]]] #single table with all free days to start





################################# Main Program

print '''
Use
- Commas(,) to to seperate values, eg. add math 101, csc111
- Space in between words, eg. jan 2019 instead of jan2019
- Term has commands next and current
- Add, eg. add math101,csc111 etc.
- Remove/rem/rmv, eg. rem math101 etc.
- Show, to see selected courses
- Calc to Calculate all the tables
- ShowTable to see tables (TODO) 
- Quit to quit
'''

while True:
    print
    inp = raw_input(">>> ").lower().strip()

    # Commands
    # Sets term for courses
    if 'term' in inp:

        #remove command word and get the argument
        inp = inp.replace('term','').strip()
        
        try:
            term = setTerm(inp)
        except:
            print 'Term takes an input; next, current or termcode'

    # Adds course(s)
    elif 'add' in inp:

        #removes command word and makes list of arguments
        inp = inp.replace('add','').split(',')
        
        for course in inp:

            course = processArgToCourse(course.strip()) # returns [name,number]

            if course not in selectedCourses:
                selectedCourses.append(Course(course[0],course[1]))

    # Removes course(s)
    elif ('remove' in inp) or ('rem' in inp) or ('rmv' in inp):

        #removes command word and makes list of arguments
        inp = inp.replace('remove','').replace('rem','').replace('rmv','').split(',')
                 
        for course in inp:

            course = processArgToCourse(course.strip()) # evalCourse returns [name,number]

            if course in selectedCourses:
                selectedCourses.remove(course)

    # Displays term: courses
    # TODO: and Table
    elif inp in ['show','show courses']:

        print term + ': ',

        for course in selectedCourses:
            print course.course,course.num+',',

        print #moves cursor to next line

    # Evaluates TimeTable
    elif ('calc' in inp) or ('eval table' in inp) or ('get tables' in inp):
        
        # Adds course info from web to Course Object 
        selectedCourses = map(lambda x: getCourse(term,x),selectedCourses)
        
        tables = evalTable(selectedCourses,tables)

    elif 'showtable' in inp:
        
        #TODO

        # shows table at index 0

        print tables[0][0]
        print tables[0][1]
        print tables[0][2]
        print tables[0][3]
        print tables[0][4]
        pass

    # Exits program            
    elif inp in ['quit','exit','q','done']:
        
        break

    # Excecutes a python command or deems input invalid
    else:

        try:
            exec(inp)
        except:
            print "Invalid Input"



    
