from django.contrib.auth import logout
from django.shortcuts import render, redirect
from checking.models import GetImage, Member
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

# Graph
from graph.views import ApiGraph6week as graph_6week
from graph.views import ApiGraphRatiobyClass as graph_ratiobyclass
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

def RegisterForm(request):
    teachers = (
        User.objects.all()
        )
    return render(request, "common/register.html", {"teachers" : teachers})

def ApiRegister(request):
    if request.method == "POST":
    #     try :
    #         user = User.objects.get(username="임시선생님")
    #     except User.DoesNotExist:
    #         user = User.objects.create_user(username="임시선생님",password="dlatltjstodsla") #비번 임시선생님
    #         user.save()

        new_register = Member()
        # new_register.teacher = user
        teacher_name = request.POST.get('teacher')
        print(teacher_name)
        teacher = User.objects.get(username=teacher_name)
        new_register.teacher = teacher
        new_register.name = request.POST['name']
        new_register.grade = request.POST['grade']
        new_register.gender = request.POST['gender']
        new_register.save()

    return redirect("/")

def ApiError(request):
    return render(request, "common/error.html", {})