from django.db import models


class Course_db(models.Model):

    term = models.CharField(max_length=6)
    name = models.CharField(max_length=100)
    num = models.CharField(max_length=3)

    def __str__(self):
        return self.name + " " + self.num + " " + self.term


class Section_db(models.Model):

    course = models.ForeignKey(Course_db, on_delete=models.CASCADE)
    type = models.CharField(
        max_length=2, choices=[("LE", "Lecture"), ("LA", "Lab"), ("TU", "Tutorial")]
    )
    section = models.CharField(max_length=100)
    crn = models.IntegerField(unique=True)
    sTime = models.DecimalField(max_digits=3, decimal_places=1)
    eTime = models.DecimalField(max_digits=3, decimal_places=1)
    formated_time = models.CharField(max_length=100)
    days = models.CharField(max_length=5)
    place = models.CharField(max_length=100)
    instructor = models.CharField(max_length=100)

    def __str__(self):
        return str(self.course) + " " + self.section
