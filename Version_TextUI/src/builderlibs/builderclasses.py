"""Stores all the classes to be used"""


class Table:
    def __init__(self):

        self.M = []
        self.T = []
        self.W = []
        self.R = []
        self.F = []

        # each element is a list of sections which have same time
        self.sections = []

        self.extra_hours = 0

    def __getitem__(self, i):

        # allows t['M'] to access t.M
        # Used in inserting in tables
        return eval("self." + i)

    def __iter__(self):

        yield self.M
        yield self.T
        yield self.W
        yield self.R
        yield self.F

    def __str__(self):  # TODO: improve this

        # Courses are represtented as [starttime, endtime, course] eg. [13,14,'CSC111']
        return "\n".join(
            day + ": " + str([i[:3] for i in table])[1:-1]
            for day, table in zip("MTWRF", self)
        )

    def get_extra_hours(self):
        """
        Gets sum total of all time when no there is no class till thh end of last
        class of the day for whole week. Used in ranking.
        """

        self.extra_hours = 0
        for day in self:
            for c in range(1, len(day)):
                self.extra_hours += day[c][0] - day[c - 1][1]
        return self.extra_hours

    def get_crns(self):
        """
        Provides crns of sections used in table in 2d tuple. All sections in same tuple
        have exact same timings so any can be taken.
        """
        return [[j.crn for j in i] for i in self.sections]


class Course:
    def __init__(self, course, num):
        self.name = course
        self.num = num

        # Contain Section objects
        self.lectures = list()
        self.labs = list()
        self.tutorials = list()

    def __eq__(self, course):
        """
        Makes Course objects comparable to ('Math','100') type tuples."""

        if (type(course) == list or type(course) == tuple) and len(course) == 2:
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

    def __ne__(self, course):
        return not self == course

    def __str__(self):
        s = "Course: " + self.name + " " + self.num + "\nLectures:\n"

        for i in self.lectures:
            s += "\t" + str(i) + "\n"

        s += "Labs:\n"

        for i in self.labs:
            s += "\t" + str(i) + "\n"

        s += "Tutorials:\n"

        for i in self.tutorials:
            s += "\t" + str(i) + "\n"

        return s

    def __iter__(self):
        """
        Makes iterable over types (lectures,labs,tutorials).
        Used to iterate over all sections of the course and build a TimeTable
        """
        yield self.lectures
        yield self.labs
        yield self.tutorials


class Section:
    def __init__(self):

        self.course_name = ""
        self.course_num = ""
        self.section = ""
        self.crn = ""
        self.time = ()
        self.days = ""
        self.place = ""
        self.instructor = ""

    def __eq__(self, other):

        """
        Makes Section Objects comparabable to [12,13,'MATH','101'] type objects
        stored in Table Objects' days (M, T, W, R, F).
        """
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
        return (
            "Course: "
            + self.course_name
            + " "
            + self.course_num
            + " | Section: "
            + self.section
            + " | Time: "
            + str(self.time)
            + " | Days: "
            + self.days
        )

    def __rep__(self):
        return (
            "Course: "
            + self.course_name
            + " "
            + self.course_num
            + " | Section: "
            + self.section
            + " | Time: "
            + str(self.time)
            + " | Days: "
            + self.days
        )

    def setTime(self, time):
        """
        Converts time from webscraper to tuple of start and end integers.
        eg. '8:30 am - 9:50 am' = (8.5, 10)
        """

        time = time.split(" - ")  # [['3:30 pm','4:30 pm']

        # For start('3:30 pm') and end ('4:30 pm') terms
        for i in range(2):

            t = time[i][:-2].split(":")  # from '3:30 ' or '10:50' to ('3', '30) or ...
            t[0] = int(t[0].strip())  # takes hour eg. 3 or 10

            # Adjust to 24 hr notation
            if "pm" in time[i] and t[0] != 12:
                t[0] += 12

            # Adjust according to minutes eg. 3:30/3:20 to 3.5
            if "30" in t[1] or "20" in t[1]:
                t[0] += 0.5
            elif "50" in t[1]:
                t[0] += 1

            # Store new value
            time[i] = t[0]

        self.time = tuple(time)
