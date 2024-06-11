from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.password_validation import validate_password


# PasswordResetFrom by email

from typing import Iterator
from django.contrib.auth.tokens import default_token_generator
from django.http import HttpRequest
from django.shortcuts import resolve_url
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from accounts.models import CustomUser

token_generator = default_token_generator


class PasswordResetForm(forms.Form):
    # 이메일 포맷에 대한 유효성 검사만 수행할 뿐, 이메일의 존재 유무를 확인하지는 않습니다.
    email = forms.EmailField()

    # auth앱의 PasswordResetForm에서는 save 메서드에서 이메일 발송에 필요한
    # 다양한 인자를 전달받습니다.

    # save 메서드는 http요청을 인자로 받음
    def save(self, request: HttpRequest) -> None:
        email = self.cleaned_data.get("email")

        # 재설정 링크 생성
        for uidb64, token in self.make_uidb64_and_token(email):
            # 현 요청의 http sheme과 host주소를 통해 재설정 링크를 구성
            scheme = "https" if request.is_secure() else "http"
            host = request.get_host()

            # 새로운 암호를 입력받아, 암호를 변경하는 뷰
            # path는 uidb64와 token으로 구성된 ApiResetPwdConfirm url 접근 경로
            path = resolve_url(
                "accounts:ApiResetPwdConfirm", uidb64=uidb64, token=token
            )

            # 실사용 pwd reset url
            reset_url = f"{scheme}://{host}{path}"
            print(f"{email} 이메일로 {reset_url} 주소를 발송합니다.")  # TODO: 이메일 발송

    def make_uidb64_and_token(self, email: str) -> Iterator[tuple[str, str]]:
        for user in self.get_users(email):
            print(f"{email}에 매칭되는 유저를 찾았습니다.")

            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            token = token_generator.make_token(user)

            yield uidb64, token

    def get_users(self, email: str) -> Iterator[CustomUser]:
        active_users = CustomUser.objects.filter(email__iexact=email, is_active=True)
        return (
            user
            for user in active_users
            if user.has_usable_password() and email == user.email
        )


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        max_length=20,
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
        max_length=30,
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
