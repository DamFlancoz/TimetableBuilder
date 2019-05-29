
# TimetableBuilder

Takes your courses, term and constraints(eg. start classes on 10 am for tuesday, instructor should be ...) to recommend you course sections you should get and shows you the timetable you will have if you get them.

For example if you want to take CSC 111, MATH 100, ... etc. in Fall. Program might recommend A01 of CSC 111, B09 for its lab, A04 of MATH 100, T07 for its tutorial, ... etc.

You can choose when in day you want to get off or start, eg. you might be fine with 9am - 6pm for classes on Tuesday but only till 3pm for Wednesday.

## Working

Uses Django to make a server and opereate a local website. GUI is essentially a webpage that talks with back-end api through AJAX to function. 

## Current Status

- Back-end methods are done.
- GUI page is ready to use.

## TODO

- Connect back-end to front-end.
- add feature to see instructors and black-list or choose them.
- add feature to pick breaks in between

