# Generated by Django 2.2.1 on 2019-05-24 06:08

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='section',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Sections',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('term', models.IntegerField()),
                ('section', models.CharField(max_length=100)),
                ('crn', models.IntegerField(unique=True)),
                ('sTime', models.IntegerField()),
                ('eTime', models.IntegerField()),
                ('days', models.CharField(max_length=100)),
                ('place', models.CharField(max_length=100)),
                ('instructor', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Courses',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('term', models.IntegerField()),
                ('course', models.CharField(max_length=100)),
                ('num', models.IntegerField()),
                ('labs', models.ManyToManyField(related_name='LabOf', to='TableBuilder.Sections')),
                ('lectures', models.ManyToManyField(related_name='lectureOf', to='TableBuilder.Sections')),
                ('tutorials', models.ManyToManyField(related_name='tutorialOf', to='TableBuilder.Sections')),
            ],
        ),
    ]
