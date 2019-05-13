# Generated by Django 2.2.1 on 2019-05-13 01:47

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
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
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course', models.CharField(max_length=100)),
                ('num', models.IntegerField()),
                ('labs', models.ManyToManyField(related_name='LabOf', to='TableBuilder.Section')),
                ('lectures', models.ManyToManyField(related_name='lectureOf', to='TableBuilder.Section')),
                ('tutorials', models.ManyToManyField(related_name='tutorialOf', to='TableBuilder.Section')),
            ],
        ),
    ]