# Generated by Django 2.2.3 on 2019-07-21 02:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('logic_api', '0003_auto_20190720_1933'),
    ]

    operations = [
        migrations.CreateModel(
            name='Section_d',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('section', models.CharField(max_length=100)),
                ('crn', models.IntegerField(unique=True)),
                ('sTime', models.DecimalField(decimal_places=1, max_digits=3)),
                ('eTime', models.DecimalField(decimal_places=1, max_digits=3)),
                ('days', models.CharField(max_length=5)),
                ('place', models.CharField(max_length=100)),
                ('instructor', models.CharField(max_length=100)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='logic_api.Course_db')),
            ],
        ),
        migrations.DeleteModel(
            name='Section_db',
        ),
    ]