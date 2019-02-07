'''
handleInput
takes - inp,term,coursesList,tableEval,showTable,breakLoop
returns - term,coursesList,tableEval,showTable,breakLoop

Goes through commands of user to determine further action
'''
from HandleInput import *
#handleInput,evalCourse

'''
getCourse
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
from ParseHtml import *
#test_getCourse(),getCourse(term,course,courseNo)

'''
TODO in WebScrapper: handle not existing page search
TODO in all libs, Put Tests
TODO show table (in HandleInput), evalTable
'''

courses = {}
term = ''
coursesList[]     #[[name1,number1],[name2,number2]]; to eval
tableEval = False
showTable = False
breakLoop = False

# Main Program

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

while True:
    inp = raw_input(">>> ").split(';') # list of input commands

    # passes everything through input handler
    term,coursesList,tableEval,showTable,breakLoop = handleInput(inp,
                                                                 term,
                                                                 coursesList,
                                                                 tableEval,
                                                                 showTable,
                                                                 breakLoop)

    if (tableEval):
        #TODO
        tableEval = False
        pass

    if (showTable):
        #TODO
        showTable = False


    # Exits program
    if (breakLoop): break














    
