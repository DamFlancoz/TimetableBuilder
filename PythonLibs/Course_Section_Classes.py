
class Table:

    def __init__(self):

        self.M = []
        self.T = []
        self.W = []
        self.R = []
        self.F = []
        
    # allows t['M'] to access t.M
    # Used in inserting in tables
    def __getitem__(self,i):
        return eval('self.'+i)
        
    def __iter__(self):
        
        yield self.M
        yield self.T
        yield self.W
        yield self.R
        yield self.F
        
    def __str__(self): #TODO: imporve this
        return '-'+'\n-'.join([ ''.join([str(j) for j in i]) for i in list(self)])



'''
Can be compared to [course,num] or Course objects
'''
class Course:

    def __init__(self,course,num):

        self.course = course
        self.num = num

        #Contain Section objects
        self.lectures = [] 
        self.labs = []
        self.tutorials = []

    def __eq__(self,course): #Used in main->rem Command, takes [course,num]
        return course[0] == self.course and course[1] == self.num

    def __ne__(self,course): #Used in main-> rem Command, takes [course,num]
        return course[0] != self.course and course[1] != self.num

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

    def __str__(self):
        return ('Course: ' + self.cName + ' ' + self.cNum 
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

            # Adjust according to minutes eg. 3:30/3:20 to 3.5
            if '30' in t[1].strip() or '20' in t[1].strip(): t[0] += 0.5
            elif '50' in t[1].strip() : t[0] += 1

            # Adjust to 24 hr notation
            if 'pm' in time[i] and t[0] != 12 :t[0]+=12

            # Store new value
            time[i] = t[0]

        self.time = tuple(time)
