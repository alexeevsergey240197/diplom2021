# Generated by Django 2.2.19 on 2021-04-07 09:25

from django.db import migrations
import separatedvaluesfield.models


class Migration(migrations.Migration):

    dependencies = [
        ('main_application', '0003_auto_20210407_1338'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='report',
            name='group',
        ),
        migrations.AddField(
            model_name='groupofreports',
            name='context',
            field=separatedvaluesfield.models.SeparatedValuesField(max_length=10000, null=True, verbose_name='Список субъектов'),
        ),
    ]