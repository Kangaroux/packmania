# Generated by Django 2.1.1 on 2018-10-01 01:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('song', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chart',
            name='fakes',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='chart',
            name='hands',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='chart',
            name='holds',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='chart',
            name='jumps',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='chart',
            name='lifts',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='chart',
            name='meter',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='chart',
            name='mines',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='chart',
            name='rolls',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='chart',
            name='taps',
            field=models.IntegerField(default=0),
        ),
    ]