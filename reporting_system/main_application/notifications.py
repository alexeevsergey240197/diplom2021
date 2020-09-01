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
            role_ckeck = str(role_check)
            if role_check == RoleUser.objects.get(name='Администратор'):
                return {'user_organisation': USER.organisation, 'ROLE': 'Администратор'}
            elif role_check == RoleUser.objects.get(name='Поручитель отчётности'):
                ALL_with_status_new = ReportInfo.objects.filter(status__name='Новый')
                ALl_with_status_under_consideration = ReportInfo.objects.filter(status__name='Рассматривается')
                return {
                    'user_organisation': USER.organisation,
                    'ALL_new_reports': ALL_with_status_new.count(),
                    'ALL_under_consideration': ALl_with_status_under_consideration.count(),
                    'ROLE': 'Поручитель отчётности'
                }
            elif role_check == RoleUser.objects.get(name='Субъект отчётности'):
                objectsNEW = ReportInfo.objects.filter(status__name='Новый',
                                                       organisation__name=USER.organisation)
                objectsCHANGE = ReportInfo.objects.filter(status__name='Доработать',
                                                          organisation__name=USER.organisation)
                objectsUNDER_consideration = ReportInfo.objects.filter(status__name='Рассматривается',
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
