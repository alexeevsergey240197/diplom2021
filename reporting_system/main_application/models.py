from django.db import models
from django.contrib.auth.models import User


class ReportStatus(models.Model):
    name = models.CharField(max_length=25)

    def __str__(self):
        return self.name


class OrganisationOfReport(models.Model):
    name = models.CharField(max_length=100)


    def __str__(self):
        return self.name



class RoleUser(models.Model):
    name = models.CharField(max_length=30)


    def __str__(self):
        return self.name

class ReportInfo(models.Model):
    name = models.CharField(max_length=80)
    start_date = models.DateField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True, null=True)
    organisation = models.ForeignKey(OrganisationOfReport, default=None, null=True, on_delete=models.DO_NOTHING)
    status = models.ForeignKey(ReportStatus, null=True, verbose_name='Статус', on_delete=models.DO_NOTHING)
    context = models.TextField(max_length=3000, default='', blank=True)
    columns = models.IntegerField(default='')
    top_names = models.TextField(default='', blank=True)
    message = models.TextField(max_length=600, default='')
    message_help = models.TextField(max_length=600, default='', blank=True, verbose_name='Сообщение для помощи')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-start_date']


class UserProfile(models.Model):
    user = models.OneToOneField(User, default="default user", on_delete=models.CASCADE)
    organisation = models.OneToOneField(OrganisationOfReport, null=True, blank=True, on_delete=models.DO_NOTHING, verbose_name='Организация')
    email = models.EmailField(blank=True, verbose_name='Электроная почта')
    phone_number = models.TextField(blank=True, max_length=25, verbose_name='Телефонный номер')
    role = models.ForeignKey(RoleUser, default=None, null=True, on_delete=models.DO_NOTHING, verbose_name='Роль')

    def __str__(self):
        return self.user.username
