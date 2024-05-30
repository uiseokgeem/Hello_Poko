from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.password_validation import validate_password
from account.models import CustomUser


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
        if not CustomUser.objects.filter(username=username).exists():
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
        user = CustomUser.objects.get(username=username)
        user.set_password(new_password1)
        user.save()


class UserForm(UserCreationForm):
    username = forms.CharField(
        max_length=12,
        required=True,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "사용할 아이디를 입력해주세요."}
        ),
        label="사용자 아이디",
    )

    password1 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "비밀번호를 입력하세요."}
        ),
        label="비밀번호",
    )

    password2 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "입력한 비밀번호를 확인합니다!"}
        ),
        label="비밀번호 확인",
    )

    full_name = forms.CharField(
        max_length=12,
        required=True,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "교사의 이름을 입력해주세요."}
        ),
        label="이름",
    )

    birth_date = forms.DateField(
        required=True,
        widget=forms.DateInput(
            attrs={
                "class": "form-control",
                "placeholder": "생년월일을 입력하세요.",
                "type": "date",
            }
        ),
        label="생년월일",
    )

    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(
            attrs={"class": "form-control", "placeholder": "비밀번호 찾기를 위해 이메일을 입력하세요."}
        ),
        label="이메일",
    )

    class Meta:
        model = CustomUser
        fields = (
            "username",
            "password1",
            "password2",
            "full_name",
            "birth_date",
            "email",
        )
