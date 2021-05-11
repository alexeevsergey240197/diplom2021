from django.core.exceptions import ObjectDoesNotExist

from .models import *


def ForMenu(request):
    if not request.user.is_authenticated:
        return {}
    else:
        username = request.user
        try:
            USER = UserProfile.objects.get(user=username)
            role_check = USER.role
            if role_check == 'Администратор':
                return {'user_organisation': USER.organisation, 'ROLE': 'Администратор'}
            if role_check == 'Поручитель отчётности':
                ALL_with_status_new = Report.objects.filter(status='Новый')
                ALl_with_status_under_consideration = Report.objects.filter(status='Рассматривается')
                return {
                    'user_organisation': USER.organisation,
                    'ALL_new_reports': ALL_with_status_new.count(),
                    'ALL_under_consideration': ALl_with_status_under_consideration.count(),
                    'ROLE': 'Поручитель отчётности'
                }
            if role_check == 'Субъект отчётности':
                objectsNEW = Report.objects.filter(status='Новый', organisation__name=USER.organisation)
                objectsCHANGE = Report.objects.filter(status='Доработать', organisation__name=USER.organisation)
                objectsUNDER_consideration = Report.objects.filter(status='Рассматривается',
                                                                   organisation__name=USER.organisation)
                return {
                    'user_organisation': USER.organisation,
                    'new': objectsNEW.count(),
                    'need_change': objectsCHANGE.count(),
                    'under_consideration': objectsUNDER_consideration.count(),
                    'ROLE': 'Субъект отчётности'
                }
        except ObjectDoesNotExist:
            return {}


def ForMenuOrg(request):
    if not request.user.is_authenticated:
        return {}
    else:
        username = request.user
        try:
            USER = UserProfile.objects.get(user=username)
            org = USER.organisation
            return {'org':org}
        except ObjectDoesNotExist:
            return {}
