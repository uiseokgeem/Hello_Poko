# login
from .forms import CustomAuthenticationForm, PasswordResetForm
from django.contrib.auth import views as auth_views
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse


from checking.models import Member
from django.contrib.auth.models import User
from common.forms import UserForm

# Graph
from graph.views import ApiGraph6week as graph_6week
from graph.views import ApiGraphWeekly as graph_weekly


class CustomLoginView(auth_views.LoginView):
    authentication_form = CustomAuthenticationForm
    template_name = "common/login.html"

    def form_valid(self, form):
        user = form.get_user()

        if user.check_password("poko0000!"):
            # redirect와의 차이?
            return HttpResponseRedirect(reverse("common:ApiUpdatePwd"))

        auth_login(self.request, user)
        return HttpResponseRedirect(self.get_success_url())


def logout_view(request):
    logout(request)
    return redirect("/")


def ApiUpdatePwd(request):
    if request.method == "GET":
        form = PasswordResetForm()
        return render(request, "common/update_pwd.html", {"form": form})

    if request.method == "POST":
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("common:login")


def index_common(request):  # dashboard
    if request.method == "GET" and request.user.is_authenticated:
        graph_6w, count_text1, count_text2, count_text3 = graph_6week(request)

        return render(
            request,
            "common/index_common.html",
            context={
                "graph_6w": graph_6w,
                "count_text1": count_text1,
                "count_text2": count_text2,
                "count_text3": count_text3,
            },
        )

    if request.method == "POST" and request.user.is_authenticated:
        date = request.POST.get("date", "")
        graph_6w, count_text1, count_text2, count_text3 = graph_6week(request)
        (
            graph_week,
            AttendanceToTeacher,
            tabel_teacher,
            count_text5,
            count_text6,
            users,
        ) = graph_weekly(request, date)

        return render(
            request,
            "common/index_common.html",
            context={
                "graph_6w": graph_6w,
                "count_text1": count_text1,
                "count_text2": count_text2,
                "count_text3": count_text3,
                "graph_week": graph_week,
                "tabel_student": AttendanceToTeacher,
                "tabel_teacher": tabel_teacher,
                "users": users,
                "count_text5": count_text5,
                "count_text6": count_text6,
                "date": date,
            },
        )


def RegisterForm(request):
    teacher_name = request.user.username
    teachers = User.objects.all().exclude(username=teacher_name)

    members = Member.objects.filter(teacher=teacher_name)
    return render(
        request, "common/register.html", {"teachers": teachers, "members": members}
    )


def ApiRegister(request):
    if request.method == "POST" and request.user.is_authenticated:
        #     try :
        #         user = User.objects.get(username="임시선생님")
        #     except User.DoesNotExist:
        #         user = User.objects.create_user(username="임시선생님",password="dlatltjstodsla") #비번 임시선생님
        #         user.save()
        new_register = Member()
        # new_register.teacher = user
        # teacher_name = request.POST.get('teacher')
        # teacher = User.objects.get(username=teacher_name)
        teacher_name = request.user.username
        teacher = User.objects.get(username=teacher_name)
        new_register.teacher = teacher
        name = request.POST.get("name")
        if Member.objects.filter(name=name).exists():
            error_message = "이미 존재하는 이름입니다. 다른 이름을 선택해 주세요."
            return render(
                request, "common/register.html", {"error_message": error_message}
            )
        else:
            new_register.name = name
            new_register.grade = request.POST["grade"]
            new_register.gender = request.POST["gender"]
            new_register.save()
            return redirect("/register/")
    return redirect("/")


def ApiClimb(request):
    if request.method == "POST" and request.user.is_authenticated:
        member_id = request.POST.get("member_id")
        selected_teacher_id = request.POST.get("teacher_id")

        member = Member.objects.get(pk=member_id)
        # member = get_object_or_404(Member, pk=member_id)
        member.teacher = User.objects.get(pk=selected_teacher_id)
        member.save()
        return redirect("/register/")
    teachers = User.objects.all()
    return render(request, "common/register.html", {"teachers": teachers})


def ApiError(request):
    return render(request, "common/error.html", {})


def ApiSignup(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data["username"]
            raw_password1 = form.cleaned_data["password1"]
            raw_password2 = form.cleaned_data["password2"]
            print("ApiSignup Complete!", username, raw_password1)
            return redirect("common:login")

            # user = authenticate(
            #     user=username,
            #     password=raw_password1,
            # )
            # 문제 : 사용자 인증(authenticate)에서 none을 반환
            # authenticate가 기존에 있던 uiseok의 아이디와 비밀번호로도 인증하지 못함
            # 회원 가입만 처리하고 로그인은 사용자가 직접하는 방법 고려 화요일까지 -> 완료
            # if user is not None:
            #     print("user is not none!")
            #     login(request, user)

        else:
            print("폼이 유효하지 않습니다.")
            print(form.errors)
            return render(request, "common/signup.html", {"form": form})
    else:
        print("회원가입 실패")
        form = UserForm()
        return render(request, "common/signup.html", {"form": form})
