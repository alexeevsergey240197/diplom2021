from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.forms import Textarea, NumberInput, EmailInput

from .models import *


class AuthUserForm(AuthenticationForm, forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'password')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control btn'


class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = (
            'name',
            'organisation',
            'columns',
            'message'
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
        self.fields['message'].widget = Textarea(attrs={'rows': 5,
                                                        'cols': 160,
                                                        'placeholder': 'Поле ввода',
                                                        'class': 'form-control',
                                                        'style': 'resize:both;'
                                                        })
        self.fields['columns'].widget = NumberInput(attrs={'max': 10, 'class': 'form-control'})



class CheckReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ('status', 'message_help')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
        self.fields['message_help'].widget = Textarea(attrs={'rows': 5,
                                                             'cols': 145,
                                                             'placeholder': 'Поле ввода',
                                                             'class': 'form-control'})


class SettingsUser(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('email', 'phone_number')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget = EmailInput(attrs={'placeholder': 'Введите email',
                                                        'class': 'form-control'})


class OrganisationForm(forms.ModelForm):
    class Meta:
        model = Organisation
        fields = ('name',)


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['placeholder'] = 'Добавить новую организацию'
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'


class myUserCreationForm(UserCreationForm):
    class Meta:
        model=User
        fields = ('username', 'password1', 'password2')


    def __init__(self, *args, **kwargs):
        super(myUserCreationForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['class'] = 'form-control'
