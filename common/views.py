from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from checking.models import GetImage, Member
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from common.forms import UserForm
from checking.models import GetImage

# Graph
from graph.views import ApiGraph6week as graph_6week
from graph.views import ApiGraphWeekly as graph_weekly

# Authenticate
from django.contrib.auth.hashers import make_password

raw_password = "user_password"
hashed_password = make_password(raw_password)


def logout_view(request):
    logout(request)
    return redirect("/")


def index_common(request):  # dashboard
    if request.method == "GET" and request.user.is_authenticated:
        poko_image = GetImage.objects.get(pk=1).image.url
        graph_6w, count_text1, count_text2, count_text3 = graph_6week(request)

        return render(
            request,
            "common/index_common.html",
            context={
                "poko_image": poko_image,
                "graph_6w": graph_6w,
                "count_text1": count_text1,
                "count_text2": count_text2,
                "count_text3": count_text3,
            },
        )

    if request.method == "POST" and request.user.is_authenticated:
        date = request.POST.get("date", "")

        poko_image = GetImage.objects.get(pk=1).image.url
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
                "poko_image": poko_image,
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
    teachers = User.objects.all()
    return render(request, "common/register.html", {"teachers": teachers})


def ApiRegister(request):
    if request.method == "POST":
        #     try :
        #         user = User.objects.get(username="임시선생님")
        #     except User.DoesNotExist:
        #         user = User.objects.create_user(username="임시선생님",password="dlatltjstodsla") #비번 임시선생님
        #         user.save()

        new_register = Member()
        # new_register.teacher = user
        teacher_name = request.POST.get("teacher")
        print(teacher_name)
        teacher = User.objects.get(username=teacher_name)
        new_register.teacher = teacher
        new_register.name = request.POST["name"]
        new_register.grade = request.POST["grade"]
        new_register.gender = request.POST["gender"]
        new_register.save()

    return redirect("/")


def ApiError(request):
    return render(request, "common/error.html", {})


def signup(request):
    print("회원가입 작동확인")
    if request.method == "POST":
        print("POST 요청 확인")
        form = UserForm(request.POST)
        print("from 생성 확인")
        if form.is_valid():
            print("회원가입 작성 중")
            form.save()
            username = form.cleaned_data["username"]
            print("username 확인", username)
            raw_password1 = form.cleaned_data["password1"]
            raw_password2 = form.cleaned_data["password2"]
            email = form.cleaned_data["email"]
            print("raw_password1 확인", raw_password1)
            print("raw_password2 확인", raw_password2)
            print("회원가입 작성 완료")

            return redirect("common:login")

            # user = authenticate(
            #     user=username,
            #     password=raw_password1,
            # )
            # 문제 : 사용자 인증(authenticate)에서 none을 반환
            # authenticate가 기존에 있던 uiseok의 아이디와 비밀번호로도 인증하지 못함

            # 회원 가입만 처리하고 로그인은 사용자가 직접하는 방법 고려 화요일까지 -> 완료

            # print("authenticate 완료")
            # print("user type확인", type(user), user)
            # if user is not None:
            #     print("user is not none!")
            #     login(request, user)

    else:
        print("회원가입 실패")
        form = UserForm()
        return render(request, "common/signup.html", {"form": form})
