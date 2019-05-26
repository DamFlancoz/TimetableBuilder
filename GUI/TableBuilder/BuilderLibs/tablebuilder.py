'''
This module provides functionality to calculate time tables.
'''

from copy import deepcopy # For testing eval table
from time import localtime # for seting term

from .classes import Table,Course,Section,NotFit,NoSectionOfTypeFit



term = '201901'


def evalTable(selected_courses,day_lengths):

    tables = [Table()] #free weekby default

    #Acts as buffer for new tables made in each type for each section
    new_tables={}

    for course in selected_courses:
        for type_ in course:
            for section in type_:

                # skip if class falls out of required schedule
                if not check_section_with_day_lengths(section,day_lengths): continue

                for i,t in enumerate(tables):



                    # i is in new_tables[(time,section.days,i)] so that a section does keep puting itself
                    #  eg 'A01' in next iterations of tables sees its previous entry in new tables and puts
                    #      itself wih it again.
                    # But it allows other section with same day and time to find the table

                    #[start,end] eg [11,13.5] for'11am-1:20pm'
                    time = section.time

                    if not (time,section.days,i) in new_tables:
                        table = deepcopy(t)

                        try:
                            table = insert_in_table(section,table)

                            new_tables[(time,section.days,i)]= table

                        except NotFit:
                            continue
                    else:
                        new_tables[(time,section.days,i)] = insert_same_in_table(section,new_tables[(time,section.days,i)])

            # if no section of a type can be added then
            if  (not new_tables) and type_: raise NoSectionOfTypeFit(course)

            # If at start a type_ is [] it makes table [] in comprehension
            # but you want it to remain a free table (default value) so loop
            # for tables can run.

            tables = list(new_tables.values()) if new_tables else tables
            new_tables = {}

    return tables

'''
return True if sectionis compatible with day_lengths
'''
def check_section_with_day_lengths(section,day_lengths):
    for day in section.days:
        if section.time[0] < day_lengths[day][0] or section.time[1] > day_lengths[day][1]:
            return False
    else:
        return True

'''
Checks timings for section and inserts them table.
Raises NotFit Error if any class on a day cannot fit in.

inserts - [start,end,course+courseno.,section]
eg. [12.5,13.5,'MATH101','T01']
'''
def insert_in_table(section,table):
    time=section.time

    #Waring this makes the lists in all days point to sam list
    #if you make change in one to_insert in one day, all of them change
    to_insert = [time[0],time[1],section.cName+section.cNum,section.section]

    for day in section.days:
        #inserting in free day
        if table[day]==[]:
            table[day].insert(0,to_insert)

        #inserting at start of day
        elif table[day][0][0] >= time[1]:
            table[day].insert(0,to_insert)

        else:
            #inserting during the day
            for i in range(len(table[day])-1):
                if table[day][i][1] <= time[0] and table[day][i+1][0] >= time[1]:
                    table[day].insert(i+1,to_insert)
                    break

            #inserting at end of day
            else:
                if table[day][-1][1] <= time[0]:
                    table[day].append(to_insert)
                else:
                    raise NotFit()

    table.sections.append([section])

    return table

'''
Inserts in a section which has same timings as another inserted class
eg. [12.5,13.5,'MATH101','T01'] to [12.5,13.5,'MATH101','T01','T02']
'''
def insert_same_in_table(section,table):
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




######################################################### Main ###############################

'''
set_term
takes - input argument for term and
return - term value equal accordingly
'''
def set_term(inp):
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

############################## Global Variables

term = set_term('curr')# term chosen
selected_courses = []  # Course objects
day_lengths = {'M':[0,24],'T':[0,24],'W':[0,24],'R':[0,24],'F':[0,24]}
