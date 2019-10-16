# Generated by Django 2.2.3 on 2019-07-21 02:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('logic_api', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='courses',
            name='labs',
        ),
        migrations.RemoveField(
            model_name='courses',
            name='lectures',
        ),
        migrations.RemoveField(
            model_name='courses',
            name='tutorials',
        ),
        migrations.AddField(
            model_name='sections',
            name='course',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='logic_api.Courses'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='courses',
            name='num',
            field=models.CharField(max_length=3),
        ),
        migrations.AlterField(
            model_name='courses',
            name='term',
            field=models.CharField(max_length=6),
        ),
    ]