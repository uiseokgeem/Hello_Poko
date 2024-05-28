from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.password_validation import validate_password


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


class CustomSetPasswordForm(forms.Form):
    username = forms.CharField(
        max_length=12,
        required=True,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "poko00"}
        ),
        label="사용자 코드",
    )
    new_password1 = forms.CharField(
        max_length=12,
        required=True,
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": " 대문자, 소문자, 숫자, 특수 문자 포함"}
        ),
        label="신규 비밀번호",
    )
    new_password2 = forms.CharField(
        max_length=12,
        required=True,
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "비밀번호 확인"}
        ),
        label="비밀번호 확인",
    )

    # 유효성 검사
    def clean_username(self):
        username = self.cleaned_data.get("username")
        if not User.objects.filter(username=username).exists():
            raise forms.ValidationError("입력하신 사용자 코드에 해당하는 사용자가 없습니다.")
        return username

    def clean_new_password1(self):
        password1 = self.cleaned_data.get("new_password1")
        validate_password(password1)
        return password1

    def clean_new_password2(self):
        new_password1 = self.cleaned_data.get("new_password1")
        new_password2 = self.cleaned_data.get("new_password2")
        if new_password1 and new_password2 and new_password1 != new_password2:
            raise forms.ValidationError("비밀번호가 일치하지 않습니다.")
        return new_password2

    def save(self):
        username = self.cleaned_data.get("username")
        new_password1 = self.cleaned_data.get("new_password1")
        user = User.objects.get(username=username)
        user.set_password(new_password1)
        user.save()


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
