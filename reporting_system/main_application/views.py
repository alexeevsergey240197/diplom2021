from django.views.generic import ListView
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.contrib import auth
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import IntegrityError

from .forms import *
from .models import *


# ДОБАВИТЬ в каждую функцию проверку логина
# Общий программный код
def Logout(request):
    auth.logout(request)
    return HttpResponseRedirect("/")


class LoginView(LoginView):
    template_name = 'main_application/login-page.html'
    form_class = AuthUserForm
    success_url = reverse_lazy('main-page')

    def get_success_url(self):
        return self.success_url


def MainPage(request):
    template_name = 'main_application/main-page.html'
    if not request.user.is_authenticated:
        return redirect('login_page')
    else:
        return render(request, template_name, {})


class HelpPage(LoginRequiredMixin, TemplateView):
    template_name = 'main_application/Help/help-page.html'
    raise_exception = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


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
                result = Report.objects.filter(start_date__range=[date_start, date_end])
                count = result.count()
                count = int(count)
                return render(request, 'main_application/SearchReport/result-page.html', {"reports": result,
                                                                                          "count": count})
            elif organisation == 'Все организации' and status != 'Любой статус':
                result = Report.objects.filter(start_date__range=[date_start, date_end], status=status)
                return render(request, 'main_application/search-report.html', {"reports": result,
                                                                               "count": count})
            elif organisation != 'Все организации' and status != 'Любой статус':
                result = Report.objects.filter(start_date__range=[date_start, date_end],
                                               status=status,
                                               organisation__name=organisation)
                return render(request, 'main_application/search-report.html', {"reports": result,
                                                                               "count": count})
            else:
                return render(request, 'main_application/search-report.html', {})
        else:
            return render(request, 'main_application/SearchReport/search-report.html', {
                'organisation_list': organisations,
                'statuses': statuses,
                'count': count
            })  # Переделать


# Раздел редактирование субъектом отчета
class AllReportsOfOrganisation(LoginRequiredMixin, ListView):
    paginate_by = 5
    model = Report
    context_object_name = 'reports'
    template_name = 'main_application/ArchiveReports/all-reports-of-organisation.html'
    raise_exception = True

    def get_queryset(self):
        USER = UserProfile.objects.get(user=self.request.user)
        list_reports = Report.objects.filter(organisation__name=USER.organisation)
        queryset = list_reports

        return queryset


def NewReports(request):
    USER = UserProfile.objects.get(user=request.user)
    list_reports = Report.objects.filter(status='Новый', organisation__name=USER.organisation)
    return render(request, 'main_application/new_reports_list-page.html', {'list_reports': list_reports})


def UnderConsiderationReports(request):
    USER = UserProfile.objects.get(user=request.user)
    list_reports = Report.objects.filter(status='Рассматривается', organisation__name=USER.organisation)
    return render(request, 'main_application/under_consideration_reports_list.html', {'list_reports': list_reports})


def NeedChangeReports(request):
    USER = UserProfile.objects.get(user=request.user)
    list_reports = Report.objects.filter(status='Доработать', organisation__name=USER.organisation)
    return render(request, 'main_application/need_change_reports_list.html', {'list_reports': list_reports})


def AddInfoIntoReport(request, id):
    report = Report.objects.get(id=id)
    top = report.top_names.split('*#*')
    names_for_input = []
    columns = report.columns
    for i in range(0, columns):
        name_input = 'input' + str(i)
        names_for_input.append(name_input)
    context = {
        "report": report,
        'context': report.top_names,
        'top': top,
        'inputs': names_for_input,
        'message': report.message
    }
    if request.method == "POST":
        DATAlist = []
        for i in range(0, columns):
            add = request.POST.get(names_for_input[i])
            DATAlist.append(add)
        DATAstr = "*#*".join(DATAlist)
        report.context = DATAstr
        report.status = "Рассматривается"
        report.save()
        return HttpResponseRedirect("/")
    else:
        return render(request, 'main_application/edit_report-page.html', context)


def ChangeReports(request, id):
    report = Report.objects.get(id=id)
    contextTABLE = report.context.split('*#*')
    namesTABLE = report.top_names.split('*#*')
    names_for_input = []
    columns = report.columns
    context = {'report': report,
               'contextTABLE': contextTABLE,
               'namesTABLE': namesTABLE,
               'names_for_input': names_for_input
               }
    for i in range(0, columns):
        name_input = 'input' + str(i)
        names_for_input.append(name_input)
    if request.method == 'POST':
        DATAlist = []
        for i in range(0, columns):
            add = request.POST.get(names_for_input[i])
            DATAlist.append(add)
        DATAstr = "*#*".join(DATAlist)
        report.context = DATAstr
        report.status = "Рассматривается"
        report.save()
        message = 'Ваши изменения отчёта применены'
        return render(request, 'main_application/READY.html', {"message": message})
    return render(request, 'main_application/change_report-page.html', context)


# Раздел поручителя
class ArchiveReports(LoginRequiredMixin, ListView):
    paginate_by = 5
    model = Report
    template_name = 'main_application/ArchiveReports/archive-reports-page.html'
    raise_exception = True



class ChoiceGroupOrIndividual(TemplateView):
    template_name = 'main_application/ArchiveReports/ChoiceGroupOrIndividual-page.html'


def CreateFormReport(request):
    form = ReportForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            name = form.cleaned_data['name']
            report = Report.objects.get(name=name)
            report.status = 'Новый'
            report.save()
            request.session['report_name'] = str(report.name)
        return redirect('add_names')
    return render(request, 'main_application/CreateFormReport/add_template_report-page.html', {'form': form})


def AddNameToReport(request):
    name = request.session['report_name']
    report = Report.objects.get(name=name)
    columns = report.columns
    inputs = []
    for i in range(0, columns):
        name_input = 'input' + str(i)
        inputs.append(name_input)
    if request.method == 'POST':
        DATAlist = []
        for i in range(0, columns):
            add = str(request.POST.get(inputs[i]))
            print(add)
            DATAlist.append(add)
        DATAstr = '*#*'.join(DATAlist)
        report.top_names = DATAstr
        report.save()
        return redirect('check')
    else:
        return render(request, 'main_application/CreateFormReport/add_top_names-page.html',
                      {'inputs': inputs, 'report': report})


def CheckingInfoReport(request):
    name = request.session['report_name']
    report = Report.objects.get(name=name)
    contextTABLE = report.top_names.split('*#*')
    return render(request, 'main_application/CreateFormReport/check-info-report-page.html',
                  {'report': report, 'contextTABLE': contextTABLE})


def DeleteReport(request, id):
    report = Report.objects.get(id=id)
    message = 'Отчёт ' + str(report.name) + ' удалён'
    report.delete()
    return render(request, 'main_application/READY.html', {"message": message})


def CheckReportsList(request):
    list_reports = Report.objects.filter(status="Рассматривается")
    return render(request, 'main_application/check-reports-page.html', {'list_reports': list_reports})


def CheckReport(request, id):
    form = CheckReportForm(request.POST)
    report = Report.objects.get(id=id)
    contextTABLE = report.context.split('*#*')
    namesTABLE = report.top_names.split('*#*')
    context = {'report': report,
               'form': form,
               'namesTABLE': namesTABLE,
               'contextTABLE': contextTABLE}
    if request.method == 'POST':
        if form.is_valid():
            added_status = form.cleaned_data['status']
            added_message = form.cleaned_data['message_help']
            report.status = added_status
            report.message_help = added_message
            print(added_status)
            report.save()
            if added_status == 'Сформирован':
                message = "Отчёт " + str(report.name) + " сформирован и помещен в архив"
            else:
                message = 'Статус "' + str(added_status) + '" присвоен для отчёта: ' + str(report.name)
            return render(request, 'main_application/READY.html', {"message": message})
    return render(request, 'main_application/check_report-page.html', context)


def SendedReports(request):
    list_reports = Report.objects.filter(status="Новый")
    return render(request, 'main_application/sended-reports-page.html', {'list_reports': list_reports})


# Настройка своего аккаунта
def SettingsAccount(request):
    username = request.user
    user = UserProfile.objects.get(user=username)
    return render(request, 'main_application/SettingsUser/settings_account-page.html', {'user': user})


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
            return render(request, 'main_application/SettingsUser/change_NAME-page.html', {})
        else:
            raise Http404('Нет доступа')


def ChangeEmail(request, id):
    if not request.user.is_authenticated:
        return redirect('login_page')
    else:
        form = SettingsUser(request.POST)
        userNOW = request.user
        userID = User.objects.get(id=id)
        user_info = UserProfile.objects.get(id=id)
        if str(userNOW) == str(userID.username):
            if request.method == 'POST':
                if form.is_valid():
                    user_info.email = form.cleaned_data['email']
                    user_info.save()
                    return redirect("settings_account")
            return render(request, 'main_application/SettingsUser/change_EMAIL-page.html',
                          {'user': user_info, 'form': form})
        else:
            raise Http404('Нет доступа')


def ChangePhone(request, id):
    if not request.user.is_authenticated:
        return redirect('login_page')
    else:
        userNOW = request.user
        userID = User.objects.get(id=id)
        user_info = UserProfile.objects.get(id=id)
        if str(userNOW) == str(userID.username):
            if request.method == 'POST':
                user_info.phone_number = request.POST.get('phone')
                user_info.save()
                return redirect("settings_account")
            return render(request, 'main_application/SettingsUser/change_PHONE-page.html',
                          {'user': user_info})
        else:
            raise Http404('Нет доступа')


# админка

def AdminOrganisations(request):
    all_organisations = Organisation.objects.all
    form = OrganisationForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
        return redirect('admin_organisations')
    return render(request, 'main_application/AdminPanel/admin_organisations.html',
                  {"organisations": all_organisations,
                   'form': form})


def RenameOrganisation(request, id):
    organisation = Organisation.objects.get(id=id)
    if request.method == 'POST':
        NewName = request.POST.get('NewName')
        organisation.name = NewName
        organisation.save()
        return redirect('admin_organisations')
    return render(request, 'main_application/AdminPanel/rename_organisation-page.html',
                  {"organisation": organisation})


def DeleteOrganisation(request, id):
    try:
        organisation = Organisation.objects.get(id=id)
        organisation.delete()
        return redirect("admin_organisations")
    except IntegrityError:
        error = 'Сначала удалите аккаунты этой организации'
        return render(request, 'main_application/ERRORS.html', {"errors": error})


def UsersList(request):
    users = UserProfile.objects.all
    roles = ['Поручитель отчётности', 'Субъект отчётности', 'Администратор']
    if request.method == "POST":
        ROLE = request.POST.get('role')
        id = request.POST.get('id')
        USER = UserProfile.objects.get(id=id)
        USER.role = ROLE
        USER.save()
        message = 'Пользователю ' + str(USER.user.username) + " присвоена роль " + str(ROLE)
        return render(request, 'main_application/READY.html', {"message": message})
    return render(request, 'main_application/AdminPanel/adm_users.html',
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
    return render(request, 'main_application/AdminPanel/create_user.html', {'form': form})


# ПРОБЛЕМА!!!!
def AddOrganisationToUser(request, id):
    organisations = Organisation.objects.all
    user = User.objects.get(id=id)
    print(id)
    if request.method == 'POST':
        account = UserProfile.objects.get(id=id)
        organisation = request.POST.get('organisation')
        organisationObj = Organisation.objects.get(name=organisation)
        organisationObj.userprofile = account
        account.save()
        message = 'Пользователю ' + str(user) + ' присвоена организация ' + str(organisation)
        return render(request, 'main_application/READY.html', {"message": message})
    return render(request, 'main_application/AdminPanel/AddOrgToUser-page.html',
                  {"organisations": organisations, "user": user})


def DeleteUser(request, id):
    user = User.objects.filter(id=id)
    user.delete()
    message = 'Пользователь удалён из системы'
    return render(request, 'main_application/READY.html', {"message": message})
