
def evalCourse(i):
    i = i.strip()
    i = i.upper()
    name = ''
    num = ''
    for char in i:
        if char.isalpha(): name += char
        elif char.isdigit(): num += char

    return [name,num]

'''
Commands ( command:value; )
- white spaces dont matter
- not case sensitive
- works with multiple commands on same line ';' seperated
- works even without ':'
- works if you dont put ';' at the end


Command List
- Term eg. '201901','current','next'
- Course/Add/courses, eg. add: math101,csc111 etc.
- Remove/Rem/rmv, eg. rem: math101 etc.
- Show/see/show courses/see courses, eg. show, see, see courses
- Quit/q/done/exit to quit
- coursesDict[math101]['instructor']; can be accessed

'''

def handleInput(inp,term,courses,tableEval,showTable,breakLoop)
    for i in inp:

            # list[0] - command, list[1] - inputs( ',' seperated)
            i = i.split(':')

            # Gets rid of whitespace
            try:
                i[0] = i[0].strip()

            # Commands
            # Evaluates TimeTable
            if ('calc' in i[0]) or ('evaluate' in i[0]) or ('eval table' in i[0]):

                tableEval = True
            
            # Sets term for courses
            elif 'term' in i[0]:
                if len(i) == 1: # makes i[1] for no ':' case
                    i.append(i[0].replace('term',''))

                try:
                    if ('next' in i[1]) or ('n' in i[1]):
                        
                        # gives tuple (year,month,date,h,min,s,weekday, etc.)
                        time = localtime()

                        if time[1] in [1,2,3,4]: # next term from may
                            term = str(time[0])+ '02'

                        elif time[1] in [5,6,7,8]: # next term from sept
                            term = str(time[0])+ '03'

                        else: #next term from jan
                            term = str(time[0]+1)+ '01'

                    elif ('current' in i[1]) or ('curr' in i[1]):

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

            # Adds course(s)
            elif ('course' in i[0]) or ('add' in i[0]) or ('courses' in i[0]):

                # takes care of no ':' case
                if len(i) == 1:
                    i.append(i[0].replace('courses','')
                             .replace('course','')
                             .replace('add',''))
                
                i[1] = i[1].split(',')
                for course in i[1]:
                    course = evalCourse(course) # evalCourse returns [name,number]
                    if course not in course:
                        courses.append(course)

            # Removes course(s)
            elif ('remove' in i[0]) or ('rem' in i[0]) or ('rmv' in i[0]):

                # takes care of no ':' case
                if len(i) == 1:
                    i.append(i[0].replace('remove','')
                             .replace('rem','')
                             .replace('rmv',''))
                    
                i[1] = i[1].split(',')
                for course in i[1]:
                    course = evalCourse(course) # evalCourse returns [name,number]
                    if course in courses:
                        courses.remove(course)

            # Displays term: courses TODO: and Table
            elif i[0] in ['show','show courses','see','see courses']:

                # no input is needed so need take care of no ':' case

                if (term = ''):
                    print '<choose term>' + ': ',
                else:
                    print term + ': ',

                for i in courses:
                    print i[0],i[1]+',',
                print #moves cursor to next line

                showTable = True

            # Exits program            
            elif i[0] in ['quit','exit','q','done']:
                
                breakLoop = True

            # Excecutes a python command or deems input invalid
            else:

                try:
                    exec(i[0])
                except:
                    print "Invalid Input"

    return term,courses,tableEval,showTable,breakLoop



                
