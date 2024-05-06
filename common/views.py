from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from common.forms import UserForm
from checking.models import GetImage

# Graph
from graph.views import ApiGraph6week as graph_6week
from graph.views import ApiGraphWeekly as graph_weekly


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


def signup(request):
    print("회원가입 작동확인")
    if request.method == "POST":
        print("POST 요청 확인")
        form = UserForm(request.POST)
        if form.is_valid():
            print("회원가입 작성 내용")
            form.save()
            username = form.cleaned_data["username"]
            raw_password = form.cleaned_data["password1"]
            user = authenticate(user=username, password=raw_password)
            login(request, user)
            return redirect("common:index_common")
    else:
        print("회원가입 실패")
        form = UserForm()
        return render(request, "common/signup.html", {"form": form})
