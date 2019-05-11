from django.db import models

# Create your models here.
class Section(models.Model):

    # can access course through s.course_set.all()/.filter etc
    section = models.CharField(max_length = 100)
    crn = models.IntegerField(unique=True)
    sTime = models.IntegerField() 
    eTime = models.IntegerField()
    days = models.CharField(max_length = 100)
    place = models.CharField(max_length = 100)
    instructor = models.CharField(max_length = 100)

# class Type(models.Model):
    
#     sections = models.ManyToManyField(Section)
#     #course = models.OneToOneField(Course,models.CASCADE)


class Course(models.Model):
    
    course = models.CharField(max_length = 100)
    num = models.IntegerField()
    lectures = models.ManyToManyField(Section,related_name='lectureOf')
    labs = models.ManyToManyField(Section,related_name='LabOf')
    tutorials = models.ManyToManyField(Section,related_name='tutorialOf')




