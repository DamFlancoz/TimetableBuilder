# HANDLE_INPUT

from time import localtime

'''
Commands ( command:value; )
- white spaces dont matter
- not case sensitive

Command List
- term eg. '201901','current','next'
- courses eg. 'CSC111', 'Math 101', 'MATH 101'
- math101['instructor']; exec() may help
- works even without ':'
- works if you dont put ';' at the end



TODO in WebScrapper: handle not existing page search
TODO, put option to use '2019 jan' in term
'''

def getCourse(i):
    i = i.strip()
    i = i.upper()
    name = ''
    num = ''
    for char in i:
        if char.isalpha(): name += char
        elif char.isdigit(): num += char

    return [name,num]
        





print '''
Use
- Semicolon(;) to terminate inputs
- Colon(:) to give values, eg. term: jan 2019;
- Space in between words, eg. jan 2019 instead of jan2019
- Term has commands next and current
- Course/Add, eg. add: math101,csc111 etc.
- Remove/Rem, eg. rem: math101 etc.
- Show, eg. show, see, see courses
- Quit to quit
'''

term = ''
courses = []    #[[name1,number1],[name2,number2]]
breakLoop = False
while(True):

    inp = raw_input(">>> ").split(';') # list of input commands
    if inp[-1] == '': inp = inp[:-1]

    for i in inp:

        # list[0] - command, list[1] - inputs( ',' seperated)
        i = i.split(':')

        # Gets rid of whitespace
        try:
            i[0] = i[0].strip()
            i[1] = i[1].strip()
        except:
            pass

        # Commands
        if 'term' in i[0]:
            if len(i) == 1: # makes i[1] for no ':' case
                i.append(i[0].replace('term',''))

            try:
                if i[1] in ['next','n']:
                    
                    # gives tuple (year,month,date,h,min,s,weekday, etc.)
                    time = localtime()

                    if time[1] in [1,2,3,4]: # next term from may
                        term = str(time[0])+ '02'

                    elif time[1] in [5,6,7,8]: # next term from sept
                        term = str(time[0])+ '03'

                    else: #next term from jan
                        term = str(time[0]+1)+ '01'

                elif i[1] in ['current','c','curr']:

                    # gives tuple (year,month,date,h,min,s,weekday, etc.)
                    time = localtime()

                    if time[1] in [1,2,3,4]: # next term from jan
                        term = str(time[0])+ '01'

                    elif time[1] in [5,6,7,8]: # next term from may
                        term = str(time[0])+ '02'

                    else: #current term from sept
                        term = str(time[0])+ '03'

                elif i[1].isdigit() and len(i[1]) == 6:
                    term = i[i]

            except:
                print 'Term takes an input, next, current or termcode'

        #adds course(s)
        elif ('course' in i[0]) or ('add' in i[0]) or ('courses' in i[0]):

            # takes care of no ':' case
            if len(i) == 1:
                i.append(i[0].replace('courses','')
                         .replace('course','')
                         .replace('add',''))
            
            i[1] = i[1].split(',')
            for course in i[1]:
                course = getCourse(course) # getCourse returns [name,number]
                if course not in course:
                    courses.append(course)

        #removes course(s)
        elif ('remove' in i[0]) or ('rem' in i[0]) or ('rmv' in i[0]):

            # takes care of no ':' case
            if len(i) == 1:
                i.append(i[0].replace('remove','')
                         .replace('rem','')
                         .replace('rmv',''))
                
            i[1] = i[1].split(',')
            for course in i[1]:
                course = getCourse(course) # getCourse returns [name,number]
                if course in courses:
                    courses.remove(course)

        # displays term: courses
        elif i[0] in ['show','show courses','see','see courses']:

            # no input is needed so need take care of no ':' case

            print term+': ',
            for i in courses:
                print i[0],i[1]+',',
            print #moves cursor to next line

        # exits program            
        elif i[0] in ['quit','exit','q','done']: # exit

            # no input is needed so need take care of no ':' case
            
            breakLoop = True

        # excecutes a python command or deems input invalid
        else:

            try:
                exec(i[0])
            except:
                print "Invalid Input"

    if breakLoop: #exits program
        break







            
