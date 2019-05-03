'''
TODO:
- remove bug which doubly adds section labels in calc when using more than
  one course
- add table class
- add validation for inputs in all methods
- take care of case in webscrapper if [age is not reachable or doesnot exist
- add conditons in making table eg. start day at 10am

'''

'''
getPage(term,course)
term: should be in coded form eg. 201901
course: Course object with course and num defined

returns html page in str
'''
from PythonLibs.WebScrapper import getPage


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


'''
All classes in use

Course
Section

TODO: Table
'''
from PythonLibs.Course_Section_Classes import Table


'''
All Exceptions defined here

NoSectionsAvailable(course) - Raised by getPage() from WebScrapper when no section for 
    Course object are found
NotFit - Raised if a section does not fit in table
'''
from PythonLibs.Exceptions import NoSectionsAvailable


'''
Used to get system time.
Used in setting term to current or next
'''
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
            term = str(time[0])+ '05'

        elif time[1] in [5,6,7,8]: # next term from sept
            term = str(time[0])+ '09'

        else: #next term from jan
            term = str(time[0]+1)+ '01'

    elif ('current' in inp) or ('curr' in inp):

        # gives tuple (year,month,date,h,min,s,weekday, etc.)
        time = localtime()

        if time[1] in [1,2,3,4]: # next term from jan
            term = str(time[0])+ '01'

        elif time[1] in [5,6,7,8]: # next term from may
            term = str(time[0])+ '05'

        else: #current term from sept
            term = str(time[0])+ '09'

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

term = setTerm('curr')# term chosen
selectedCourses = []  # Course objects

'''
tables stores list of table elements
table is a list of days which each store list of classes that day
[M,T,W,R,F]
M = [[8.5, 10, 'MATH200', 'A01'],[8.5, 9.5, 'MATH204', 'A02']]
each class elements forms, [start,end,course,section] to trace it back
'''
tables=[Table()] #single table with all free days to start





################################# Main Program

print( '''
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
''')

while True:
    print()
    inp = input(">>> ").lower().strip()

    # Commands
    # Sets term for courses
    if 'term' in inp:

        #remove command word and get the argument
        inp = inp.replace('term','').strip()
        
        try:
            term = setTerm(inp)
        except:
            print('Term takes an input; next, current or termcode')

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

        print (term + ': ',end = '')

        for course in selectedCourses:
            print (course.course,course.num+',',end='')

        print() #moves cursor to next line

    # Evaluates TimeTable
    elif ('calc' in inp) or ('eval table' in inp) or ('get tables' in inp):
        
        # Adds course info from web to Course Object
        try:
            selectedCourses = [getCourse(course,getPage(term,course)) for course in selectedCourses]
        
            tables = evalTable(selectedCourses)
        
        except NoSectionsAvailable as e:
            print(e)
            
            selectedCourses.remove(e.course)
            
            print('Removed the course.')
            print('You may want to add a replacement course.')

    elif 'showtable' in inp:
        
        #TODO

        print(tables[0])

    # Exits program            
    elif inp in ['quit','exit','q','done']:
        
        break

    # Excecutes a python command or deems input invalid
    else:

        try:
            exec(inp)
        except:
            print('Invalid Input')



    
