import unicodedata

from django.contrib.auth import password_validation
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm, UserCreationForm, ReadOnlyPasswordHashField
from django.contrib.auth.models import User
from django import forms
from django.core import validators
from django.core.validators import EmailValidator
from django.forms import CharField, EmailInput


class UserProfileForm(UserChangeForm):
    password = ReadOnlyPasswordHashField(
        label="",
        help_text=
            "Raw passwords are not stored, so there is no way to see this "
            "user's password, but you can change the password using "
            "<a href=\"{}\">this form</a>."
        ,
    )
    class Meta:
        model = User
        fields = ('first_name', 'last_name')
        exclude = ('password', 'id_password')

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)

    def clean_password(self):
        pass


class UserPassForm(PasswordChangeForm):

    new_password1 = forms.CharField(
        label="New password",
        widget=forms.PasswordInput,
        strip=False,
    )

    class Meta:
        model = User
        # fields = ('username', 'first_name', 'last_name', 'email', 'password',)
        # exclude = ('password',)

    def __init__(self, *args, **kwargs):
        super(PasswordChangeForm, self).__init__(*args, **kwargs)


class UsernameField(CharField):

    def to_python(self, value):
        return unicodedata.normalize('NFKC', super().to_python(value))

    widget = EmailInput
    default_validators = [validators.EmailValidator(message='Email то липовый')]

    def __init__(self, **kwargs):
        super().__init__(strip=True, **kwargs)


class EmailRegisterForm(UserCreationForm):

    error_messages = {
        'password_mismatch': "Поля ввода пароля должны совпадать",
    }

    password1 = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput,
    )
    password2 = forms.CharField(
        label="Password confirmation",
        widget=forms.PasswordInput,
        strip=False,
    )

    class Meta:
        model = User
        fields = ("username",)
        field_classes = {'username': UsernameField}
        # тут мы очищаем поля подсказок
        help_texts = {
            'username': None,
            'password1': None,
            'password2': None,
        }

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
