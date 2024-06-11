from django.contrib import messages
from django.utils.http import urlsafe_base64_decode
from django.views.decorators.csrf import csrf_protect

from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from poko import settings
from .forms import CustomAuthenticationForm, CustomSetPasswordForm
from django.contrib.auth import views as auth_views
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout
from django.http import HttpResponseRedirect, HttpResponse, request
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from accounts.forms import UserForm
from .models import CustomUser


class CustomLoginView(auth_views.LoginView):
    authentication_form = CustomAuthenticationForm
    template_name = "account/login.html"

    def form_valid(self, form):
        user = form.get_user()

        if user.check_password("poko0000!"):
            return HttpResponseRedirect(reverse("account:ApiUpdatePwd"))

        auth_login(self.request, user)
        if user.username == "poko01" or user.username == "poko02":
            return HttpResponseRedirect(reverse("common:ApiIndexManager"))

        else:
            return HttpResponseRedirect(reverse("common:ApiIndexUser"))


def ApiLogoutView(request):
    logout(request)
    return redirect("/")


def ApiSignup(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data["username"]
            raw_password1 = form.cleaned_data[
                "password1"
            ]  # raw_password1 -> password로 변경후 자동 로그인 시도

            print("ApiSignup Complete!", username, raw_password1)
            return redirect("account:login")

        else:
            print("폼이 유효하지 않습니다.")
            print(form.errors)
            return render(request, "account/signup.html", {"form": form})
    else:
        print("회원가입 실패")
        form = UserForm()
        return render(request, "account/signup.html", {"form": form})


def ApiUpdatePwd(request):
    if request.method == "GET":
        form = CustomSetPasswordForm()
        return render(request, "account/update_pwd.html", {"form": form})

    if request.method == "POST":
        form = CustomSetPasswordForm(request.POST)
        if form.is_valid():  # user.save()로 비밀번호가 변경 된 form의 유효성을 검사하고
            form.save()  # form을 저장
            return redirect("account:login")


class ApiResetPwd(PasswordResetView):
    email_template_name = "accounts/password_reset_email.html"
    success_url = reverse_lazy("account:ApiResetPwd")

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(
            self.request,
            (
                "비밀번호 재설정 메일을 발송했습니다. 계정이 존재한다면 입력하신 이메일로 "
                "비밀번호 재설정 안내문을 확인하실 수 있습니다. "
                "만약 이메일을 받지 못했다면 등록하신 이메일을 다시 확인하시거나 스팸함을 확인해주세요."
            ),
        )
        return response


class ApiResetPwdConfirm(PasswordResetConfirmView):
    post_reset_login = False  # 재설정 후 자동 로그인 설정
    success_url = reverse_lazy("account:login")

    def form_valid(self, form) -> HttpResponse:
        # 변경된 암호를 데이터베이스에 저장하고
        # 세션에서 token을 삭제하고
        # post_reset_login=True 설정이라면 자동 로그인 처리하고
        # success_url로 페이지 이동
        response = super().form_valid(form)
        messages.success(self.request, "암호를 재설정했습니다. 다시 로그인 화면으로 이동합니다.")
        return response


# token_generator = default_token_generator

# def ApiResetPwdConfirm(request, uidb64, token):
#     uid = urlsafe_base64_decode(uidb64).decode()
#     user = get_object_or_404(CustomUser, pk=uid)
#
#     context_data = {}
#     reset_url_token = "set_password"
#
#     if token != reset_url_token:  # pwd 재설정 링크가 첫방문인 경우
#         if default_token_generator.check_token(user, token):
#             request.session["_password_reset_token"] = token
#             redirect_url = request.path.replace(token, reset_url_token)
#             return redirect(redirect_url)
#
#         else:  # 토큰이 유효하지 않은 경우, 재설정 링크가 유효하지 않다는 메세지 노출.
#             return render(
#                 request,
#                 template_name="registration/password_reset_confirm.html",
#                 context={"validlink": False},
#             )
#
#     else:  # 재설정 링크 두번째 방문
#         # GET/POST 요청에 상관없이 token 검증부터 !!!
#         session_token = request.session["_password_reset_token"]
#         if token_generator.check_token(user, session_token) is False:
#             validlink = False  # token 검증에 실패하면 비밀번호 입력없이 오류 응답
#         else:
#             validlink = True  # token 검증에 성공하면 재설정할 비밀번호를 입력받습니다.
#
#             if request.method == "GET":
#                 form = SetPasswordForm(user=user)
#             else:
#                 form = SetPasswordForm(user=user, data=request.POST)
#                 if form.is_valid():
#                     form.save()
#
#                     del request.session[
#                         "_password_reset_token"
#                     ]  # 암호변경 후에 session에서 token 삭제
#                     # 일반 자동 로그인
#                     # auth_login(request, user)
#
#                     # 자동 로그인 수행 여부
#                     post_reset_login = False
#
#                     if post_reset_login:
#                         auth_login(request, user)
#                         messages.success(request, "암호를 재설정했으며, 자동 로그인 처리되었습니다.")
#                         return redirect(settings.LOGIN_REDIRECT_URL)
#                     else:
#                         messages.success(request, "암호를 재설정했습니다. 다시 로그인해주세요.")
#                         return redirect("accounts:login")
#
#             context_data["form"] = form
#
#         context_data["validlink"] = validlink
#
#         return render(
#             request,
#             template_name="registration/password_reset_confirm.html",
#             context=context_data,
#         )


# @csrf_protect
# def ApiResetPwd(request):
#     if request.method == "GET":
#         form = PasswordResetForm()
#         return render(
#             request,
#             template_name="registration/password_reset_form.html",
#             context={"form": form},
#         )
#     else:
#         form = PasswordResetForm(data=request.POST)
#         if form.is_valid():  # BaseForm의 form.is_valid()
#             form.save(request=request)
#             messages.success(
#                 request,
#                 (
#                     "비밀번호 재설정 메일을 발송했습니다. 계정이 존재한다면 입력하신 이메일로 "
#                     "비밀번호 재설정 안내문을 확인하실 수 있습니다. "
#                     "만약 이메일을 받지 못했다면 등록하신 이메일을 다시 확인하시거나 스팸함을 확인해주세요."
#                 ),
#             )
#         return redirect("accounts:ApiResetPwd")
