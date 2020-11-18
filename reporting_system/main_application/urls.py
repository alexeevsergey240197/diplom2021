from django.urls import path

from . import views


urlpatterns = [
    path('', views.MainPage, name='main-page'),
    path('search_report', views.SearchReport, name='search_report'),
    path('help/', views.HelpPage.as_view(), name='help-page'),
    path('login/', views.LoginView.as_view(), name='login_page'),
    path('logout/', views.Logout, name='logout'),
    path('archive/', views.ArchiveReports.as_view(), name='archive_page'),
    path('all_reports/', views.AllReportsOfOrganisation.as_view(), name='all_reports'),
    path('new_reports/', views.NewReports, name='new_reports-page'),
    path('under-consideration/', views.UnderConsiderationReports, name='under-consideration_reports-page'),
    path('edit/<int:id>', views.AddInfoIntoReport, name='edit-page'),
    path('groups/', views.GpoupsPage, name='groups-page'),
    path('table_excel_download/<int:id>', views.TableForExcel, name='table_excel'),
    path('choice_group_of_individual', views.ChoiceGroupOrIndividual.as_view(), name='choice_GorI'),
    path('create_group', views.CreateGroup, name='create_group'),
    path('reports_of_group/<int:id>', views.ReportsOfGroup, name='reports_of_group'),
    path('add_report/<int:id>', views.CreateFormReport, name='add_report'),
    path('add_names/<int:id>', views.AddTopNameSToReport, name='add_names'),
    path('check/<int:id>', views.CheckingInfoReport, name='check'),
    path('delete_group/<int:id>', views.DeleteGroup, name='delete_group'),
    path('delete/<int:id>', views.DeleteReport),
    path('check_list/', views.CheckReportsList, name='check_reports_list'),
    path('check_report/<int:id>', views.CheckReport, name='check_report'),
    path('sended_reports/', views.SendedReports, name='sended_reports'),
    path('need_change_report_list/', views.NeedChangeReports, name='need_change_reports_page'),
    path('change/<int:id>', views.ChangeReports),
    path('settings_account/', views.SettingsAccount, name='settings_account'),
    path('change_name/<int:id>', views.ChangeName, name='change_name'),
    path('change_email/<int:id>', views.ChangeEmail, name='change_email'),
    path('change_phone/<int:id>', views.ChangePhone, name='change_phone'),
    path('admin_organisations/', views.AdminOrganisations, name='admin_organisations'),
    path('rename_organisation/<int:id>', views.RenameOrganisation, name='rename_organisation'),
    path('delete_organisation/<int:id>', views.DeleteOrganisation, name='delete_organisation'),
    path('users/', views.UsersList, name='users'),
    path('create_user/', views.CreateUser, name='create_user'),
    path('add_organisation_to_user/<int:id>', views.AddOrganisationToUser, name='add_organisation_to_user'),
    path('delete_user/<int:id>', views.DeleteUser, name='delete_user'),



]
