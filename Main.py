'''
TODO in WebScrapper: handle not existing page search
TODO in all libs, Put Tests
TODO show table, evalTable
'''



'''
getCourse(term,course,courseNo)
takes - term,course,courseno
returns - course dictionary

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
setTerm
takes - input arguments for term and
return - term value equal accordingly
'''
from time import localtime

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
helps in add and remove
'''
def evalCourse(i):
    i = i.strip()
    i = i.upper()
    name = ''
    num = ''
    for char in i:
        if char.isalpha(): name += char
        elif char.isdigit(): num += char

    return [name,num]



# Global Variables
coursesInfo = {}      # courses' information from webpage
term = ''             # term chosen
selectedCourses = []  #[[name1,number1],[name2,number2]]; courses selected by user






################################# Main Program

print '''
Use
- Commas(,) to to seperate values, eg. add math 101, csc111
- Space in between words, eg. jan 2019 instead of jan2019
- Term has commands next and current
- Course/Add, eg. add math101,csc111 etc.
- Remove/Rem, eg. rem math101 etc.
- Show, eg. show, see, see courses
- Quit to quit
'''

while True:

    inp = raw_input(">>> ").lower().strip()
    print

    # Commands
    # Sets term for courses
    if 'term' in inp:

        inp = inp.replace('term','').strip()

        try:
            
            term = setTerm(inp)

        except:
            print 'Term takes an input; next, current or termcode'

    # Adds course(s)
    elif 'add' in inp:

        #removes command word and makes into string of arguments
        inp = inp.replace('add','').split(',')
        
        for course in inp:

            course = evalCourse(course.strip()) # evalCourse returns [name,number]

            if course not in selectedCourses:
                selectedCourses.append(course)

    # Removes course(s)
    elif ('remove' in inp) or ('rem' in inp) or ('rmv' in inp):

        #removes command word and makes into string of arguments
        inp = inp.replace('remove','').replace('rem','').replace('rmv','').split(',')
                 
        for course in inp:

            course = evalCourse(course.strip()) # evalCourse returns [name,number]

            if course in selectedCourses:
                selectedCourses.remove(course)

    # Displays term: courses
    # TODO: and Table
    elif inp in ['show','show courses']:

        if (term == ''):
            print '<choose term>' + ': ',
        else:
            print term + ': ',

        for course in selectedCourses:
            print course[0],course[1]+',',

        print #moves cursor to next line

    # Evaluates TimeTable
    elif ('calc' in inp) or ('evaluate' in inp) or ('get tables' in inp):

        # getCourse also returns a dictionary
        # course here is also a list
        for course in selectedCourses:
            coursesInfo[course[0]+course[1]] = getCourse(term,course[0],course[1])

    elif 'showTable' in inp:
        
        #TODO
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



    
