from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.forms import SetPasswordForm
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        max_length=12,
        required=True,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "코드를 입력해주세요"}
        ),
        label="사용자 코드",
    )
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "비밀번호"}
        ),
        label="비밀번호",
    )


# SetPasswordForm은 username 입력이 없다! SetPasswordForm은 로그인이 된 상태에서 비밀번호를 설정하는 경우 상속받아 사용하는 것이 좋다.


class UserForm(UserCreationForm):
    first_name = forms.CharField(label="성")
    last_name = forms.CharField(label="이름")
    email = forms.EmailField(label="이메일")

    class Meta:
        model = User
        fields = (
            "username",
            "password1",
            "password2",
            "first_name",
            "last_name",
            "email",
        )


# CustomAuthenticationForm에서 유효성 검사 코드
# def clean(self):
#    cleaned_data = super().clean()
#     username = cleaned_data.get("username")
#     password = cleaned_data.get("password")
#
#     # if password:
#     #     if password == "poko0000!":
#     #         raise forms.ValidationError("초기 비밀번호 입니다. 로그인 할 수 없어요.")
#     return cleaned_data

# def confirm_login_allowed(self, user):
#     if user.check_password("poko0000!"):
#         return HttpResponseRedirect(reverse("common:ApiUpdatePwd"))
