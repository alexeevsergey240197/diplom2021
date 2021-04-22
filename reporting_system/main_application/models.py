from django.db import models
from separatedvaluesfield.models import SeparatedValuesField

from django.contrib.auth.models import User


class Organisation(models.Model):
    status_choice = (('Муниципальный объект', 'Муниципальный объект'), ('Орган власти', 'Орган власти'))
    name = models.CharField(max_length=100)
    type = models.CharField('Кем является', max_length=20, choices=status_choice)

    def __str__(self):
        return self.name


class GroupOfReports(models.Model):
    name = models.CharField('Наименование группы', max_length=200)
    organisations = SeparatedValuesField('Список субъектов', max_length=10000, null = True)


    def __str__(self):
        return self.name


class Report(models.Model):
    status_choice = (
        ('Сформирован', 'Сформирован'), ('Рассматривается', 'Рассматривается'), ('Доработать', 'Доработать'),
        ('Новый', 'Новый'))
    name = models.CharField('Наименование отчёта', max_length=300)
    start_date = models.DateTimeField('Дата и время создания', auto_now_add=True)
    update_time = models.DateTimeField('Время последнего обновления', auto_now=True, null= True)
    organisation = models.ForeignKey(Organisation, default=None, null=True, on_delete=models.DO_NOTHING)
    status = models.CharField('Статус', max_length=20, choices=status_choice)
    count_col = models.IntegerField('Кол-во колонок', default='')
    count_row = models.IntegerField('Кол-во строк', default='')
    context = SeparatedValuesField('Содержание таблицы', max_length=10000, null = True)
    top_names = SeparatedValuesField('Имена заголовков таблицы', max_length=1000, null=True, blank=True)
    message = models.TextField('Приложенное сообщение', max_length=3000, default='')
    message_help = models.TextField('Сообщение для помощи', max_length=1000, default='', blank=True)

    typeOne = models.BooleanField('Одинарное значение?', default= True)
    string_informations = models.TextField('Информация по строкам', max_length=5000, default='')


    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-start_date']


class UserProfile(models.Model):
    role_choice = (('Поручитель отчётности', 'Поручитель отчётности'), ('Субъект отчётности', 'Субъект отчётности'),
                   ('Администратор', 'Администратор'))
    user = models.OneToOneField(User, default="default user", on_delete=models.CASCADE)
    organisation = models.OneToOneField(Organisation, default=None, null=True, blank=True, on_delete=models.DO_NOTHING,
                                        verbose_name='Организация')
    email = models.EmailField('Электроная почта', blank=True)
    phone_number = models.TextField('Телефонный номер', blank=True, max_length=25)
    role = models.CharField('Роль', max_length=30, blank=True, choices=role_choice)

    def __str__(self):
        return self.user.username
