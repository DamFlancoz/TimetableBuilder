""" This module contains all the classes used for courseinfo and tablebuilder. """

from .htmltable import table_to_html_table


class Table(object):
    def __init__(self):

        # Contain lists, eg. [15.5, 16.5, 'SENG 265', 'A01']
        self.M = []
        self.T = []
        self.W = []
        self.R = []
        self.F = []

        # each element is a list of sections which have same time
        self.sections = []

    def __getitem__(self, d):
        return self.__getattribute__(d)

    def __str__(self):  # TODO: improve this
        """
        eg.
        M: [15.5, 16.5, 'SENG265', 'A01']
        T: [8.5, 9.5, 'CSC230', 'A01']
        W: [8.5, 9.5, 'CSC230', 'A01'], [15.5, 16.5, 'SENG265', 'A01']
        R: [15.5, 16.5, 'SENG265', 'A01']
        F: [8.5, 9.5, 'CSC230', 'A01']
        """
        return "\n".join(
            day + ": " + str(courses)[1:-1] for day, courses in zip("MTWRF", self)
        )

    def __iter__(self):
        return (self[d] for d in "MTWRF")

    def to_html_table(self):
        return table_to_html_table(self)


class Course(object):
    def __init__(self, course, num):

        self.name = course
        self.num = num

        # Contain Section objects
        self.lectures = []
        self.labs = []
        self.tutorials = []

    def __eq__(self, course):

        if type(course) == list and len(course) == 2:
            return course[0] == self.name and course[1] == self.num

        elif type(course) == Course:
            return (
                self.name == course.name
                and self.num == course.num
                and self.lectures == course.lectures
                and self.labs == course.labs
                and self.tutorials == course.tutorials
            )
        else:
            return NotImplemented

    def __ne__(self, course):  # Used in main-> rem Command, takes [course,num]
        return not self == course

    def __str__(self):

        return f"""{self}
Lectures: {','.join(i for i in self.lectures)}
Labs:   {','.join(i for i in self.labs)}
Tutorials: {','.join(i for i in self.tutorials)}"""

    def __repr__(self):
        return f"{self.name} {self.num}"

    def __iter__(self):  # type - lectures, labs & tutorials
        yield self.lectures
        yield self.labs
        yield self.tutorials


class Section(object):
    def __init__(self):

        self.course_name = ""
        self.course_num = ""
        self.section = ""
        self.crn = ""
        self.time = ()
        self.formated_time = ""
        self.days = ""
        self.place = ""
        self.instructor = ""

    def __eq__(self, other):

        # Used in adding sections with same timings to table in eval table and in its test
        # Gives true if of same timings nad course, doesnot need to be exactly same.
        # eg: T01 and T02 can be equal.
        if (type(other) == tuple or type(other) == list) and len(other) == 4:
            return (
                other[0] == self.time[0]
                and other[1] == self.time[1]
                and other[2] == self.course_name + self.course_num
            )

        elif type(other) == Section:
            return (
                other.time == self.time
                and other.days == self.days
                and other.course_name == self.course_name
                and other.course_num == self.course_num
            )

        else:
            return NotImplemented

    def __ne__(self, other):
        return not self == other

    def __str__(self):
        return f"{self.section} {self.time} {self.days}"

    def __rep__(self):
        return f"{self.course_name} {self.course_num}: {self.section} {self.time} {self.days}"

    def setTime(self, time):
        """
        Converts time from webscraper to tuple of start and end integers.
        eg. '8:30 am - 9:50 am' = (8.5, 10)
        """

        self.formated_time = time

        time = time.split(" - ")  # [['3:30 pm','4:30 pm']

        # For start('3:30 pm') and end ('4:30 pm') terms
        for i in range(2):

            t = time[i][:5].split(":")  # converts to '3:30 ' or '10:50'
            t[0] = int(t[0].strip())  # takes hour eg. 3 or 10

            # Adjust to 24 hr notation
            if "pm" in time[i] and t[0] != 12:
                t[0] += 12

            # Adjust according to minutes eg. 3:30/3:20 to 3.5
            if "30" in t[1].strip() or "20" in t[1].strip():
                t[0] += 0.5
            elif "50" in t[1].strip():
                t[0] += 1

            # Store new value
            time[i] = t[0]

        self.time = tuple(time)


# Exceptions
class NoSectionsAvailableOnline(Exception):
    """
    Raised if the Uvic says sections for course are not available.
    Used in WebScrapper
    """

    def __init__(self, course):
        super().__init__(f"No sections available online for {course}")
        self.course = course


class NotFit(Exception):
    """
    Raised if a section does not fit in a timetable, timing-wise.
    Used in calculating table. Not an error.
    """

    pass
