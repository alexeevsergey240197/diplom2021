# Generated by Django 2.2.19 on 2021-04-07 06:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_application', '0002_auto_20210407_1104'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='report',
            name='finished_create',
        ),
        migrations.AlterField(
            model_name='report',
            name='name',
            field=models.CharField(max_length=300, verbose_name='Наименование отчёта'),
        ),
    ]
