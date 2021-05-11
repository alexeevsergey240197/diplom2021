from django.views.generic import ListView
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.contrib import auth
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import IntegrityError
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist

from .forms import *
from .models import *


# Общий программный код
def Logout(request):
    auth.logout(request)
    return HttpResponseRedirect("/")


class LoginView(LoginView):
    template_name = 'main_application/GENEREL_PURPOSE/login-page.html'
    form_class = AuthUserForm
    success_url = reverse_lazy('main-page')

    def get_success_url(self):
        return self.success_url


def MainPage(request):
    template_name = 'main_application/GENEREL_PURPOSE/main-page.html'
    if not request.user.is_authenticated:
        return redirect('login_page')
    else:
        return render(request, template_name, {})


class HelpPage(LoginRequiredMixin, TemplateView):
    template_name = 'main_application/GENEREL_PURPOSE/Help/help-page.html'
    raise_exception = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

# Переделат, сократить

def SearchReport(request):
    if not request.user.is_authenticated:
        return redirect('login_page')
    else:
        organisations = Organisation.objects.all
        statuses = ['Рассматривается', 'Доработать', 'Сформирован', 'Новый']
        count = 'None'
        if request.method == 'POST':
            date_start = request.POST.get('DateStart')
            date_end = request.POST.get('DateEnd')
            organisation = request.POST.get('organisation')
            status = request.POST.get('status')
            if organisation == 'Все организации' and status == 'Любой статус':
                result = Report.objects.filter(
                    start_date__range=[date_start, date_end])
                count = result.count()
                count = int(count)
                return render(request, 'main_application/ROLE_report_collector/SearchReport/result-page.html', {"reports": result,
                                                                                          "count": count})
            elif organisation == 'Все организации' and status != 'Любой статус':
                result = Report.objects.filter(
                    start_date__range=[date_start, date_end], status=status)
                return render(request, 'main_application/ROLE_report_collector/SearchReport/result-page.html', {"reports": result,
                                                                               "count": count})
            elif organisation != 'Все организации' and status != 'Любой статус':
                result = Report.objects.filter(start_date__range=[date_start, date_end],
                                               status=status,
                                               organisation__name=organisation)
                return render(request, 'main_application/ROLE_report_collector/SearchReport/result-page.html', {"reports": result,
                                                                               "count": count})
            else:
                return render(request, 'main_application/ROLE_report_collector/SearchReport/result-page.html', {})
        else:
            return render(request, 'main_application/ROLE_report_collector/SearchReport/search-report.html', {
                'organisation_list': organisations,
                'statuses': statuses,
                'count': count
            })


# Раздел редактирование субъектом отчета
class AllReportsOfOrganisation(LoginRequiredMixin, ListView):
    paginate_by = 20
    model = Report
    context_object_name = 'reports'
    template_name = 'main_application/ROLE_subject/ArchiveReports/all-reports-of-organisation.html'
    raise_exception = True

    def get_queryset(self):
        USER = UserProfile.objects.get(user=self.request.user)
        list_reports = Report.objects.filter(
            organisation__name=USER.organisation)
        queryset = list_reports
        return queryset


def NewReports(request):
    USER = UserProfile.objects.get(user=request.user)
    list_reports = Report.objects.filter(
        status='Новый', organisation__name=USER.organisation)
    return render(request, 'main_application/ROLE_subject/new_reports_list-page.html', {'list_reports': list_reports})


def UnderConsiderationReports(request):
    USER = UserProfile.objects.get(user=request.user)
    list_reports = Report.objects.filter(
        status='Рассматривается', organisation__name=USER.organisation)
    return render(request, 'main_application/ROLE_subject/under_consideration_reports_list.html', {'list_reports': list_reports})


def NeedChangeReports(request):
    USER = UserProfile.objects.get(user=request.user)
    list_reports = Report.objects.filter(
        status='Доработать', organisation__name=USER.organisation)
    return render(request, 'main_application/ROLE_subject/need_change_reports_list.html', {'list_reports': list_reports})




def AddInfoIntoReport(request, id):

    report = Report.objects.get(id=id)
    rows = report.string_informations.split('$#$')
    ListRows = []
    for i in range(len(rows)):
        ListRows.append(rows[i].split('#$#'))
    del ListRows[-1]
    context = {'ListRows': ListRows, 'report': report}
    if request.method == "POST":
        contextReport = []
        for i in range(1, len(ListRows) + 1):
            info = request.POST.get('input-' + str(i))
            contextReport.append(info)
        report.context = contextReport
        report.status = 'Рассматривается'
        report.save()
        message = 'Выш отчёт принят, ожидайте проверки'
        return render(request, 'main_application/GENEREL_PURPOSE/READY.html', {"message": message})
    return render(request, 'main_application/ROLE_subject/edit_report-page.html', context)


def ChangeReports(request, id):
    report = Report.objects.get(id=id)
    rows = report.string_informations.split('$#$')
    ListRows = []
    for i in range(len(rows)):
        ListRows.append(rows[i].split('#$#'))
    del ListRows[-1]
    context = {'ListRows': ListRows, 'report': report}
    if request.method == "POST":
        contextReport = []
        for i in range(1, len(ListRows) + 1):
            info = request.POST.get('input-' + str(i))
            contextReport.append(info)
        report.context = contextReport
        report.status = 'Рассматривается'
        report.save()
        message = 'Выш отчёт принят, ожидайте проверки'
        return render(request, 'main_application/GENEREL_PURPOSE/READY.html', {"message": message})
    return render(request, 'main_application/ROLE_subject/change_report-page.html', context)


# Раздел поручителя отчётности
class ArchiveReports(LoginRequiredMixin, ListView):
    paginate_by = 15
    model = Report
    template_name = 'main_application/ROLE_report_collector/ArchiveReports/archive-reports-page.html'
    raise_exception = True


def GpoupsPage(request):
    groups = GroupOfReports.objects.all
    return render(request, 'main_application/ROLE_report_collector/groups-page.html', {'groups': groups})


def TableForExcel(request, id):
    group = GroupOfReports.objects.get(id=id)
    reports = Report.objects.filter(group__name=group.name)
    report = reports[0]

    top_names = []
    top_names.append(str(report.name))
    TOP = top_names + list(report.top_names)

    SUBJECTS = group.ListGroups
    REPORTS = reports
    lenth = len(TOP)

    return render(request, 'main_application/ROLE_report_collector/excel-page.html', {"TOP": TOP, 'group':group,
     'subjects':SUBJECTS, 'reports':REPORTS, "BOT": report.top_names})


def ReportsOfGroup(request, id):
    reports = Report.objects.filter(group__id=id)
    group = GroupOfReports.objects.get(id=id)
    return render(request, 'main_application/ROLE_report_collector/reports-of-group.html', {'reports': reports, 'group': group})


class ChoiceGroupOrIndividual(TemplateView):
    template_name = 'main_application/ROLE_report_collector/Choice_one_or_many-page.html'



def CreateFormReport(request):
    if request.method == 'POST':
        """ Создаётся группа """
        group = GroupOfReports()
        group.name = request.POST.get('name_group')
        group.organisations = request.POST.getlist('organisations')
        group.save()
        name = request.POST.get('name_report')
        message = request.POST.get('message')
        count_col = int(request.POST.get('count_col'))
        name_group = request.POST.get('name_group')


        """ Создание формы """
        string_informations = ''

        for i in range(1, int(request.POST.get('count_colPOST')) + 1):
            string_informations = string_informations + request.POST.get('input_name-' + str(i)) + '#$#' + request.POST.get('input_comment-' + str(i)) + '#$#' + request.POST.get('input_type-' + str(i)) + '$#$'
            print(string_informations)


        """ Отсылается каждой организации форма и присваивается групп"""
        N = len(group.organisations)
        for i in range(N):
            organisation = Organisation.objects.get(id=group.organisations[i])
            report = Report()
            report.name = name
            report.message = message
            report.count_row = 4
            report.count_col = count_col
            report.organisation = organisation
            report.group = group
            report.string_informations = string_informations

            report.status = 'Новый'
            report.save()

        return redirect('main-page')
    if 'count_col' in request.GET:
        count_colGET = int(request.GET.get('count_col'))
        count_colLIST = []
        for i in range(1, count_colGET + 1):
            count_colLIST.append(i)
        start = True
        organisations = Organisation.objects.all
        count_colInt = len(count_colLIST)

        return render(request, 'main_application/ROLE_report_collector/CreateFormReport/add_template_report-page.html', {
         'count_colLIST': count_colLIST,
         'start_create': start,
         'organisations': organisations,
         'count_col':count_colInt})





    return render(request, 'main_application/ROLE_report_collector/CreateFormReport/add_template_report-page.html', {})



def CheckingInfoReport(request, id):
    group = GroupOfReports.objects.get(id=id)
    reports = Report.objects.filter(group__id=id).values_list('id', flat=True)
    report = Report.objects.get(id=reports[0])
    return render(request, 'main_application/ROLE_report_collector/CreateFormReport/check-info-report-page.html',
                  {'report': report, 'contextTABLE': report.top_names, "group": group})


def DeleteGroup(request, id):
    group = GroupOfReports.objects.get(id=id)
    message = 'Группа ' + str(group.name) + ' удалён'
    group.delete()
    return render(request, 'main_application/GENEREL_PURPOSE/READY.html', {"message": message})


def DeleteReport(request, id):
    report = Report.objects.get(id=id)
    group = GroupOfReports.objects.get(name=report.group)
    list_of_subjects = list(group.ListGroups)
    list_of_subjects.remove(str(report.organisation))
    group.ListGroups = list_of_subjects
    message = 'Отчёт ' + str(report.name) + \
        ' удалён, он был в группе ' + str(group.name)
    group.save()
    report.delete()
    return render(request, 'main_application/GENEREL_PURPOSE/READY.html', {"message": message})


def CheckReportsList(request):
    list_reports = Report.objects.filter(status="Рассматривается")
    return render(request, 'main_application/ROLE_report_collector/check-reports-page.html', {'list_reports': list_reports})


def CheckReport(request, id):
    report = Report.objects.get(id=id)
    account = UserProfile.objects.get(organisation=report.organisation)


    string_informations = report.string_informations
    rows = string_informations.split('$#$')
    ListRows = []
    del rows[-1]
    print(report.context[0])
    for i in range(len(rows)):
        row = rows[i].split('#$#')
        row.append(report.context[i])
        ListRows.append(row)
    context = {'report': report, 'ListRows':ListRows,'account':account}

    if request.method == 'POST':
        status = request.POST.get('status')
        report.status = status
        if status == 'Доработать':
            report.message_help = request.POST.get('help_message')
            message = "Отчёт от организации: " + str(report.organisation) + '- отправлен на доработку'
        else:
            message = "Отчёт от организации: " + str(report.organisation) + ' - принят'

        report.save()


        return render(request, 'main_application/GENEREL_PURPOSE/READY.html', {"message": message})
    return render(request, 'main_application/ROLE_report_collector/check_report-page.html', context)


def SendedReports(request):
    list_reports = Report.objects.filter(status="Новый")
    return render(request, 'main_application/ROLE_report_collector/sended-reports-page.html', {'list_reports': list_reports})


# Настройка своего аккаунта
def SettingsAccount(request):
    return render(request, 'main_application/GENEREL_PURPOSE/SettingsUser/settings_account-page.html', {'user': UserProfile.objects.get(user=request.user)})


def ChangeName(request, id):
    if not request.user.is_authenticated:
        return redirect('login_page')
    else:
        userNOW = request.user
        userID = User.objects.get(id=id)
        if str(userNOW) == str(userID.username):
            if request.method == 'POST':
                new_name = request.POST.get('name')
                userID.username = new_name
                userID.save()
                return redirect("settings_account")
            return render(request, 'main_application/GENEREL_PURPOSE/SettingsUser/change_NAME-page.html', {})
        else:
            raise Http404('Нет доступа')


def ChangeEmail(request, id):
    if not request.user.is_authenticated:
        return redirect('login_page')
    else:
        form = SettingsUser(request.POST)
        userNOW = request.user  # сейчас сидит
        user_info = UserProfile.objects.get(id=id)
        if str(userNOW) == str(user_info.user.username):
            if request.method == 'POST':
                if form.is_valid():
                    user_info.email = form.cleaned_data['email']
                    user_info.save()
                    return redirect("settings_account")
            return render(request, 'main_application/GENEREL_PURPOSE/SettingsUser/change_EMAIL-page.html',
                          {'user': user_info, 'form': form})
        else:
            raise Http404('Нет доступа')


def ChangePhone(request, id):
    if not request.user.is_authenticated:
        return redirect('login_page')
    else:
        userNOW = request.user
        user_info = UserProfile.objects.get(id=id)
        if str(userNOW) == str(user_info.user.username):
            if request.method == 'POST':
                user_info.phone_number = request.POST.get('phone')
                user_info.save()
                return redirect("settings_account")
            return render(request, 'main_application/GENEREL_PURPOSE/SettingsUser/change_PHONE-page.html',
                          {'user': user_info})
        else:
            raise Http404('Нет доступа')
# админка


def AdminOrganisations(request):
    all_organisations = Organisation.objects.all
    form = OrganisationForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            nameORG= form.cleaned_data['name']
            try:
                ORG = Organisation.objects.get(name=nameORG)
                message = 'Организация "' + nameORG + '" уже имеется в системе'
            except ObjectDoesNotExist:
                    form.save()
                    message = 'Организация "' + nameORG + '" создана'
        return render(request, 'main_application/ROLE_administrator/admin_organisations.html',
                      {"organisations": all_organisations,
                       'form': form,
                       'message': message})
    return render(request, 'main_application/ROLE_administrator/admin_organisations.html',
                  {"organisations": all_organisations,
                   'form': form})


def RenameOrganisation(request, id):
    organisation = Organisation.objects.get(id=id)
    if request.method == 'POST':
        NewName = request.POST.get('NewName')
        organisation.name = NewName
        organisation.save()
        return redirect('admin_organisations')
    return render(request, 'main_application/ROLE_administrator/rename_organisation-page.html',
                  {"organisation": organisation})


def DeleteOrganisation(request, id):
    try:
        organisation = Organisation.objects.get(id=id)
        organisation.delete()
        return redirect("admin_organisations")
    except IntegrityError:
        error = 'Сначала удалите аккаунты этой организации '
        return render(request, 'main_application/GENEREL_PURPOSE/ERRORS.html', {"errors": error})


def UsersList(request):
    users = UserProfile.objects.all
    roles = ['Поручитель отчётности', 'Субъект отчётности', 'Администратор']
    if request.method == "POST":
        ROLE = request.POST.get('role')
        id = request.POST.get('id')
        USER = UserProfile.objects.get(id=id)
        USER.role = ROLE
        USER.save()
        message = 'Пользователю ' + \
            str(USER.user.username) + " присвоена роль " + str(ROLE)
        return render(request, 'main_application/GENEREL_PURPOSE/READY.html', {"message": message})
    return render(request, 'main_application/ROLE_administrator/adm_users.html',
                  {"users": users, "roles": roles})


def CreateUser(request):
    form = myUserCreationForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            name = form.cleaned_data['username']
            added_user = User.objects.get(username=name)
            acc = UserProfile.objects.create(user=added_user)
            acc.save()
            return redirect('users')
    return render(request, 'main_application/ROLE_administrator/create_user.html', {'form': form})


def AddOrganisationToUser(request, id):
    organisations = Organisation.objects.all
    user = User.objects.get(id=id)
    if request.method == 'POST':
        account = UserProfile.objects.get(id=id)
        organisation = request.POST.get('organisation')
        organisationObj = Organisation.objects.get(name=organisation)
        organisationObj.userprofile = account
        account.save()
        message = 'Пользователю ' + \
            str(user) + ' присвоена организация ' + str(organisation)
        return render(request, 'main_application/GENEREL_PURPOSE/READY.html', {"message": message})
    return render(request, 'main_application/ROLE_administrator/AddOrgToUser-page.html',
                  {"organisations": organisations, "user": user})


def DeleteUser(request, id):
    user = User.objects.filter(id=id)
    message = 'Пользователь' + user.name + ' удалён из системы'
    user.delete()
    return render(request, 'main_application/GENEREL_PURPOSE/READY.html', {"message": message})
