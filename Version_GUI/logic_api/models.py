from django.db import models


class Sections(models.Model):

    # can access course through s.course_set.all()/.filter etc
    term = models.IntegerField()
    section = models.CharField(max_length=100)
    crn = models.IntegerField(unique=True)
    sTime = models.IntegerField()
    eTime = models.IntegerField()
    days = models.CharField(max_length=100)
    place = models.CharField(max_length=100)
    instructor = models.CharField(max_length=100)


class Courses(models.Model):

    term = models.IntegerField()
    course = models.CharField(max_length=100)
    num = models.IntegerField()

    lectures = models.ForeignKey(
        Sections, blank=True, on_delete=models.CASCADE, related_name="lectureOf"
    )
    labs = models.ForeignKey(
        Sections, on_delete=models.CASCADE, blank=True, related_name="LabOf"
    )
    tutorials = models.ForeignKey(
        Sections, on_delete=models.CASCADE, blank=True, related_name="tutorialOf"
    )