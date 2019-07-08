"""Contains all custom exceptions"""


class NoSectionsAvailableOnline(Exception):
    """
    Raised if the Uvic says sections for course are not available.
    Used in WebScrapper
    """

    def __init__(self, course):

        super().__init__("")
        self.course = course


class NoSectionOfTypeFit(Exception):
    """
    Raised if no sections of a type can fit due to inputted time constraints
    eg. you cannot enter any tutorial of Engr 141 because they are all at night
    """

    def __init__(self, course):
        super().__init__("")
        self.course = course


class NotFit(Exception):
    """
    Raised if a section doesnot fit in a timetable
    Used in EvalTable
    """
