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
    