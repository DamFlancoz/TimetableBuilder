'''
This module contains all the classes used.
'''

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
        return '\n'.join(day +': '+str(table)[1:-1] for day,table in zip('MTWRF',self))

    def addPddingCourses(self):
        #adds Course('start) and Course('end') to each day

        for day in self:
            day+=[Course('start',''),Course('end','')]
            day[0].time = (0,0)
            day[1].time = (24,24)

class Course:

    def __init__(self,course,num):

        self.name = course
        self.num = num

        #Contain Section objects
        self.lectures = []
        self.labs = []
        self.tutorials = []

    def __eq__(self,course):

        if (type(course) == list and len(course) == 2): #Used in main->rem Command, takes [course,num]
            return course[0] == self.name and course[1] == self.num

        elif (type(course) == Course):
            return (self.name == course.name
                    and self.num == course.num
                    and self.lectures == course.lectures
                    and self.labs == course.labs
                    and self.tutorials == course.tutorials)
        else :
            return NotImplemented


    def __ne__(self,course): #Used in main-> rem Command, takes [course,num]
        return not self == course

    def __str__(self):
        s = 'Course: ' + self.name + ' ' + self.num + '\nLectures:\n'

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

# Exceptions

'''
Raised if the Uvic says sections for course are not available.
Used in WebScrapper
'''
class NoSectionsAvailableOnline(Exception):

    def __init__(self,course):
        super().__init__('')
        self.course=course


'''
raised if no sections of a type can fit due to inputed time constraints
eg. you cannot enter any tutroial of Engr 141 because they are all at night
    and you said you dont want any night stuff.
'''
class NoSectionOfTypeFit(Exception):

    def __init__(self,course):
        super().__init__('')
        self.course=course


'''
Raised if a section doesnot fit in a timetable
Used in EvalTable. Not an error.
'''
class NotFit(Exception):
    pass
