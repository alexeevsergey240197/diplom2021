from django.db import models
from django.contrib.auth.models import User


class Organisation(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class GroupOfReports(models.Model):
    name = models.CharField('Наименованиe группы отчётов', max_length=20)


class Report(models.Model):
    status_choice = (
        ('Сформирован', 'Сформирован'), ('Рассматривается', 'Рассматривается'), ('Доработать', 'Доработать'),
        ('Новый', 'Новый'))
    name = models.CharField('Дата создания', max_length=80)
    start_date = models.DateField('Дата создания', auto_now_add=True)
    update_time = models.DateTimeField('Время последнего обновления', auto_now=True, null=True)
    organisation = models.ForeignKey(Organisation, default=None, null=True, on_delete=models.DO_NOTHING)
    status = models.CharField('Статус', max_length=20, choices=status_choice)
    context = models.TextField('Контекст таблицы', max_length=3000, default='', blank=True)
    columns = models.IntegerField('Кол-во колонок', default='')
    top_names = models.TextField('Имена столбцов', default='', blank=True)
    message = models.TextField('Приложенное сообщение', max_length=600, default='')
    message_help = models.TextField('Сообщение для помощи', max_length=600, default='', blank=True)
    group = models.ForeignKey(GroupOfReports, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-start_date']


class UserProfile(models.Model):
    role_choice = (('Поручитель отчётности', 'Поручитель отчётности'), ('Субъект отчётности', 'Субъект отчётности'),
                   ('Администратор', 'Администратор'))
    user = models.OneToOneField(User, default="default user", on_delete=models.CASCADE)
    organisation = models.OneToOneField(Organisation, null=True, blank=True, on_delete=models.DO_NOTHING,
                                        verbose_name='Организация')
    email = models.EmailField('Электроная почта', blank=True)
    phone_number = models.TextField('Телефонный номер', blank=True, max_length=25)
    role = models.CharField('Роль', max_length=30, blank=True, choices=role_choice)

    def __str__(self):
        return self.user.username
