from django.contrib import messages
from django.views.decorators.csrf import csrf_protect

from .forms import CustomAuthenticationForm, CustomSetPasswordForm, PasswordResetForm
from django.contrib.auth import views as auth_views
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from account.forms import UserForm


class CustomLoginView(auth_views.LoginView):
    authentication_form = CustomAuthenticationForm
    template_name = "account/login.html"

    def form_valid(self, form):
        user = form.get_user()

        if user.check_password("poko0000!"):
            return HttpResponseRedirect(reverse("common:ApiUpdatePwd"))

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


@csrf_protect
def ApiResetPwd(request):
    if request.method == "GET":
        form = PasswordResetForm()
        return render(
            request,
            template_name="registration/password_reset_form.html",
            context={"form": form},
        )
    else:
        form = PasswordResetForm(data=request.POST)
        if form.is_valid():  # BaseForm의 form.is_valid()
            form.save(request=request)
            messages.success(
                request,
                (
                    "비밀번호 재설정 메일을 발송했습니다. 계정이 존재한다면 입력하신 이메일로 "
                    "비밀번호 재설정 안내문을 확인하실 수 있습니다. "
                    "만약 이메일을 받지 못했다면 등록하신 이메일을 다시 확인하시거나 스팸함을 확인해주세요."
                ),
            )
        return redirect("account:ApiResetPwd")


def ApiResetPwdConfirm(request, uidb64, token):
    return HttpResponse("비밀번호 재설정을 요청하셨습니다.")
