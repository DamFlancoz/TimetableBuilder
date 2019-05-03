
class NoSectionsAvailable(Exception):
    def __init__(self,course):
        
        #
        super().__init__('')
        self.course=course
        
    
    def __str__(self):
        return ('No classes Available for ' + self.course.course + ' ' 
                + self.course.num + ' selected term.')
    