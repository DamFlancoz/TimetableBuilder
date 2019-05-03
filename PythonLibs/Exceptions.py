'''
Raised if the Uvic says sections for course are not available.
Used in WebScrapper
'''
class NoSectionsAvailable(Exception):
    def __init__(self,course):
        
        #
        super().__init__('')
        self.course=course
        
    
    def __str__(self):
        return ('No classes Available for ' + self.course.course + ' ' 
                + self.course.num + ' selected term.')
        
'''
Raised if a section doesnot fit in a timetable
Used in EvalTable
'''
class NotFit(Exception):
    pass
    