from django.contrib import admin

from .models import Course_db, Section_db

# Register your models here.
admin.site.register(Section_db)
admin.site.register(Course_db)
