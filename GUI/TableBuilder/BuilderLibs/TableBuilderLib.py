term,cName,cNum = ['201901', 'MATH', '101']


####################################################  imports ######################################

from urllib.request import urlopen
from bs4 import BeautifulSoup as bSoup

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
Used to get system time.
Used in setting term to current or next
'''
from time import localtime

##############################################  Classes ########################################

class Table:

    def __init__(self):

        self.M = []
        self.T = []
        self.W = []
        self.R = []
        self.F = []

        # each element is a list of sections which have same time
        self.sections = [] 
        
        #adds Course('start) and Course('end') to each day
        #self.addPaddingCourses() 
        
        #Course('break') may also be added
        
    def __getitem__(self,i):
        
        # allows t['M'] to access t.M
        # Used in inserting in tables
        
        return eval('self.'+i)
        
    def __iter__(self):
        
        yield self.M
        yield self.T
        yield self.W
        yield self.R
        yield self.F
        
    def __str__(self): #TODO: imporve this
        
        # course_rep eg. [13,14,'CSC111','A01']
        '''
        return ''+'\n\n-'.join([ '\n '.join([ '(' + str(course_rep[0]) + ','
                                             +str(course_rep[1]) + ') '
                                             +'\n\t'.join([str(i) 
                                                           for i in course_rep[2:]]) 
                                         for course_rep in self[day]]) 
                                for day in 'MTWRF'])
        '''

        return '\n'.join(day +': '+str(table)[1:-1] for day,table in zip('MTWRF',self))
    
    def addPddingCourses(self):
        #adds Course('start) and Course('end') to each day
        
        for day in self:
            day+=[Course('start',''),Course('end','')]
            day[0].time = (0,0)
            day[1].time = (24,24)



'''
Can be compared to [course,num] or Course objects
'''
class Course:

    def __init__(self,course,num,lectures=[],labs=[],tutorials=[]):

        self.course = course
        self.num = num

        #Contain Section objects
        self.lectures = lectures
        self.labs = labs
        self.tutorials = tutorials

    def __eq__(self,course): 

        if (type(course) == list and len(course) == 2): #Used in main->rem Command, takes [course,num]
            return course[0] == self.course and course[1] == self.num

        elif (type(course) == Course):
            return (self.course == course.course
                    and self.num == course.num
                    and self.lectures == course.lectures 
                    and self.labs == course.labs
                    and self.tutorials == course.tutorials)
        else :
            return NotImplemented
                    

    def __ne__(self,course): #Used in main-> rem Command, takes [course,num]
        return not self == course

    def __str__(self):
        s = 'Course: ' + self.course + ' ' + self.num + '\nLectures:\n'

        for i in self.lectures:
            s+='\t'+str(i)+'\n'

        s+='Labs:\n'

        for i in self.labs:
            s+='\t'+str(i)+'\n'


        s+='Tutorials:\n'

        for i in self.tutorials:
            s+='\t'+str(i)+'\n'

        return s

    def __iter__(self): # type - lectures, labs & tutorials
        yield self.lectures
        yield self.labs
        yield self.tutorials

    


class Section:

    def __init__(self):

        self.cName = ''
        self.cNum = ''
        self.section = ''
        self.crn = ''
        self.time = ()
        self.days = ''
        self.place = ''
        self.instructor = ''
        
    def __eq__(self,other): 
        
        # Used in adding sections with same timings to table in eval table and in its test
        # Gives true if of same timmings nad course, doesnot need to be exactly same.
        # eg: T01 and T02 can be equal.
        if ((type(other) == tuple or type(other) == list) and len(other) == 4): 
            return (other[0] == self.time[0] and other[1] == self.time[1]
                    and other[2] == self.cName+self.cNum)
        
        elif (type(other) == Section):
            return (other.time == self.time 
                    and other.days == self.days
                    and other.cName == self.cName
                    and other.cNum == self.cNum)
        
        else:
            return NotImplemented

    def __ne__(self,other): 
        return (not self == other)

    def __str__(self):
        return ('Course: ' + self.cName + ' ' + self.cNum 
                + ' | Section: ' + self.section
                + ' | Time: ' + str(self.time)
                + ' | Days: ' + self.days
                )
        
    def __rep__(self):
        return('Course: ' + self.cName + ' ' + self.cNum 
                + ' | Section: ' + self.section
                + ' | Time: ' + str(self.time)
                + ' | Days: ' + self.days
                )

    def setTime(self,time):

        '''
        Converts time from webscraper to tuple of start and end integers.
        eg. '8:30 am - 9:50 am' = (8.5, 10)
        '''
        
        time = time.split(' - ')  #[['3:30 pm','4:30 pm']

        # For start('3:30 pm') and end ('4:30 pm') terms
        for i in range(2): 

            t = time[i][:5].split(':') #converts to '3:30 ' or '10:50'
            t[0] = int(t[0].strip())   #takes hour eg. 3 or 10

            # Adjust to 24 hr notation
            if 'pm' in time[i] and t[0] != 12 :t[0]+=12

            # Adjust according to minutes eg. 3:30/3:20 to 3.5
            if '30' in t[1].strip() or '20' in t[1].strip(): t[0] += 0.5
            elif '50' in t[1].strip() : t[0] += 1

            # Store new value
            time[i] = t[0]

        self.time = tuple(time)



######################################  Exceptions ##########################################

'''
Raised if the Uvic says sections for course are not available.
Used in WebScrapper
'''
class NoSectionsAvailable(Exception):
    def __init__(self,course):
        
        super().__init__('')
        self.course=course
        
        
'''
raised if no sections of a type can fit due to inputted time constraints
eg. you cannot enter any tutroial of Engr 141 because they are all at night
'''
class NoSectionOfTypeFit(Exception):
    def __init__(self,course):
        
        super().__init__('')
        self.course=course


'''
Raised if a section doesnot fit in a timetable
Used in EvalTable
'''
class NotFit(Exception):
    pass


##########################################  Functions  ############################################


'''
Takes: term code, Course Object with course name and course no.
Returns: (str)the html page containing classes information
'''
def getPage(TERM,course):
    Url = 'https://www.uvic.ca/BAN1P/bwckschd.p_get_crse_unsec'
    Data = 'term_in='+TERM+'&sel_subj=dummy&sel_day=dummy&sel_schd=dummy&sel_insm=dummy&sel_camp=dummy&sel_levl=dummy&sel_sess=dummy&sel_instr=dummy&sel_ptrm=dummy&sel_attr=dummy&sel_subj='+course.course+'&sel_crse='+course.num+'&sel_title=&sel_schd=%25&sel_insm=%25&sel_from_cred=&sel_to_cred=&sel_camp=%25&sel_levl=%25&sel_ptrm=%25&sel_instr=%25&begin_hh=0&begin_mi=0&begin_ap=a&end_hh=0&end_mi=0&end_ap=a'
    # Data contains course.course and course.num further down
 
    htmlPage = urlopen(url=Url, data=Data.encode()).read().decode()
    htmlLines = htmlPage.split('\n')
    
    if (htmlLines[103] == 'No classes were found that meet your search criteria'
        or htmlLines[102] == 'No classes were found that meet your search criteria'):
        raise(NoSectionsAvailable(course))
    
    return htmlPage 




def getCourse(course,coursePageHtml):
    
    pageSoup = bSoup(coursePageHtml,'lxml')       # parsed html, soup

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

    # parses sections
    for i in range(0,len(sectionList),4):
        if 'Main Campus' in str(sectionList[i+1]):
            section = Section()
            
            titleList = str(sectionList[i]).split(' - ')
            section.section = titleList[3][:3] #some tags were also coming at the end
            section.crn = titleList[1]

            courseName = titleList[2].split(' ') #eg ['CSC','111']
            section.cName = courseName[0]
            section.cNum = courseName[1]

            info = sectionList[i+3].findAll('td')
            section.setTime(str(info[1].text)) # turns str time to tuple
            section.days = str(info[2].text)
            section.place = str(info[3].text)
            section.instructor = str(info[6].text)

            # str(info[5].text) tells if class is lecture/lab/tutorial

            if str(info[5].text) == 'Lab':
                course.labs.append(section)
            elif str(info[5].text) == 'Lecture':
                course.lectures.append(section)
            elif str(info[5].text) == 'Tutorial':
                course.tutorials.append(section)

    return course

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


######################################################### Main ###############################


def main(term,selectedCourses,dayLengths):
    print( '''
Use
- Commas(,) to to seperate values, eg. add math 101, csc111
- Space in between words, eg. jan 2019 instead of jan2019
- Term has commands next and current
- Add, eg. add math101,csc111 etc.
- Remove/rem/rmv, eg. rem math101 etc.
- Start <MR or all> at 10, use 24hr and decimals eg. start MR at 13.5
- start M at reset, to reset the value
- End <MR or all> at 10
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
        elif inp in ['show','show courses']:

            print (term + ': ',end = '')

            for course in selectedCourses:
                print (course.course,course.num+',',end='')

            print() #moves cursor to next line
            print(i+': '+str(dayLengths[i]) for i in dayLengths)

        elif 'start' in inp and 'at' in inp: 
            inp = inp.split(' ')

            if inp[1] == 'all':
                if inp[3] == 'reset':
                    for day in dayLengths:
                        dayLengths[day][0] = 0
                else:
                    for day in dayLengths:
                        dayLengths[day][0] = int(inp[3])
            else:
                if inp[3] == 'reset':
                    for day in inp[1].upper():
                        dayLengths[day][0] = 0
                else:
                    for day in inp[1].upper():
                        dayLengths[day][0] = int(inp[3])

        elif 'end' in inp and 'at' in inp: 
            inp = inp.split(' ')

            if inp[1] == 'all':
                if inp[3] == 'reset':
                    for day in dayLengths:
                        dayLengths[day][1] = 24
                else:
                    for day in dayLengths:
                        dayLengths[day][1] = int(inp[3])
            else:
                if inp[3] == 'reset':
                    for day in inp[1].upper():
                        dayLengths[day][1] = 24
                else:
                    for day in inp[1].upper():
                        dayLengths[day][1] = int(inp[3])

        # Evaluates TimeTable
        elif ('calc' in inp) or ('eval table' in inp) or ('get tables' in inp):
            
            # Adds course info from web to Course Object
            try:
                selectedCourses = [getCourse(course,getPage(term,course)) for course in selectedCourses]
            
                tables = evalTable(selectedCourses,dayLengths)
            
            except NoSectionsAvailable as e:
                
                selectedCourses.remove(e.course)
                
                print(e.course.course,e.course.num,'is not available in',term)
                print('Removed the course.')
                print('You may want to add a replacement course.')

            except NoSectionOfTypeFit as e:

                print('Current time restrictions dont allow you to take all classes of',
                    e.course.course,e.course.num)
                print('Change the Time restrictions or remove the course')

        elif 'showtable' in inp:
            
            #TODO

            print(tables[0])

        # Exits program            
        elif inp in ['quit','exit','q','done']:
            
            break

        # Excecutes a python command or deems input invalid
        else:
            print('Invalid Input')











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
dayLengths = {'M':[0,24],'T':[0,24],'W':[0,24],'R':[0,24],'F':[0,24]}

'''
tables stores list of table elements
table is a list of days which each store list of classes that day
[M,T,W,R,F]
M = [[8.5, 10, 'MATH200', 'A01'],[8.5, 9.5, 'MATH204', 'A02']]
each class elements forms, [start,end,course,section] to trace it back
'''
tables=[Table()] #single table with all free days to start

main(term,selectedCourses,dayLengths)