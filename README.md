# TimetableBuilder

One of The first 'big' programs I built in University and has been quite useful. I recommend trying out both versions since they actually give different functionalities.

## Version Text

Takes your courses, term and constraints(eg. start classes on 10 am for tuesday, instructor should be ...) to recommend you course sections you should get and shows you the timetable you will have if you get them.

For example if you want to take CSC 111, MATH 100, ... etc. in Fall. Program might recommend A01 of CSC 111, B09 for its lab, A04 of MATH 100, T07 for its tutorial, ... etc.

You can choose when in day you want to get off or start, eg. you might be fine with 9am - 6pm for classes on Tuesday but only till 3pm for Wednesday.

This version fulfils original scope project. You can get sections recommended and see crns to apply.

## Version GUI

This is an extension to project, an important one. It introduces a browser GUI for ease of use. Basically a web page with HTML, CSS and jQuery using AJAX to talk with backend server and acting as like an app. In beginning I intended it to be just a place to input courses (and day constraints) but when making timetable for this semester I realized how good it is to be able to tweak tables yourself. Hence, with some inspiration from schedulecourses.com, I will also add feature to tweak.

I chose to use a server instead of using javascript is mainly because I already had written code. This also gives me the opportunity to play with web tech and write a REST API, both of which I have been meaning to do.

To use this you will have to run the server and then click on link it shows. Two steps and it works and if you need help details are inside version folders.

## Scrapping

UVic does not provide an api for course in my knowledge so I am scrapping their website. I will try to reduce the load on servers by storing the information which is scraped once but for now this is only planned in Version GUI, might extend it to text version.

## What I learned

Here is what I have learned or used during making of Timetable Builder.

### Tools

- Html, Css, Javascript (ES6)
- JQuery, Ajax
- Django
- REST API (making and working with)

### Topics

- Working of http protocols
- Using and building REST APIs
- Interacting with Database
- Building Complex data structures
- Using OOP programming style
- Software Development Cycle
