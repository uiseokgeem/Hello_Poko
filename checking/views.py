from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from .models import Attendance, Member, GetImage
from django.contrib.auth.models import User
import matplotlib
from django.utils import timezone

matplotlib.use("Agg")


def index(request):
    poko_image = GetImage.objects.get(pk=2).image.url
    return render(request, "checking/index.html", {"poko_image": poko_image})


def index_detail(request):
    poko_image = GetImage.objects.get(pk=2).image.url
    return render(request, "checking/index_detail.html", {"poko_image": poko_image})


def ApiAttendanceProduce(request):
    if request.user.is_authenticated:
        teacher_name = request.user.first_name + request.user.last_name
        # print(teacher_name)
        poko_image = GetImage.objects.get(pk=3).image.url
        return render(
            request,
            "checking/attendance_produce.html",
            context={"poko_image": poko_image, "teacher_name": teacher_name},
        )


def ApiAttendanceList(request):
    if request.method == "POST" and request.user.is_authenticated:
        date = request.POST.get("date", "")
        user_name = request.user.username  # 로그인 정보를 통해 선생님 이름 가져오기

        user_students = (
            Member.objects.all()
            .filter(teacher=user_name)
            .values_list("name", flat=True)
        )
        user_students = sorted(list(user_students))

        return render(
            request,
            "checking/attendance_check.html",
            {"date": date, "user_students": user_students},
        )
    else:
        return HttpResponse("잘못된 접근입니다.")


def ApiAttendanceChecking(request):
    # 출석체크 여부 확인
    if request.method == "POST" and request.user.is_authenticated:
        checked_name = request.POST["name"]
        checked_date = request.POST["date"]
        if Attendance.objects.filter(name=checked_name, date=checked_date).exists():
            noti = Attendance.objects.filter(name=checked_name, date=checked_date)
            poko_image = GetImage.objects.get(pk=3).image.url
            attendance_noti_text = (
                f"{checked_name} 학생은 {noti[0].attendance}으로 확인이 완료 되었습니다!"
            )

            return render(
                request,
                "checking/attendance_noti.html",
                {
                    "attendance_noti_text": attendance_noti_text,
                    "checked_name": checked_name,
                    "checked_date": checked_date,
                    "poko_image": poko_image,
                },
            )

        # 출석 입력이 없다면 form 입력값 가져오기
        user_name = request.user.username
        # teacher = User.objects.get(username=user_name)  # 외래키 필드의 값은 객체 상태로 저장한다.
        member_str = request.POST["name"]
        member = Member.objects.get(name=member_str)
        date = request.POST["date"]
        attendance = request.POST["attendance"]

        # form 입력값을 Attendance의 각 필드에 저장
        attendance = Attendance.objects.create(
            # teacher=teacher,
            name=member,
            date=date,
            attendance=attendance,
        )

        # 출석 입력 후 명단에 표시 될 학생 이름
        user_students = (
            Member.objects.all()
            .filter(teacher=user_name)
            .values_list("name", flat=True)
        )
        user_students = sorted(list(user_students))

        # 츨석결과를 Member의 attendance에  출결 횟수 저장
        name = request.POST.get("name", "")
        member_info = get_object_or_404(Member, name=name)
        if member_info.attendance == "출석":
            member_info.attendance += 1

        elif member_info.attendance == "결석":
            member_info.absent += 1

        member_info.save()
        attendance.save()

        return render(
            request,
            "checking/attendance_check.html",
            {
                "date": attendance.date,
                "user_students": user_students,
            },
        )

    else:
        return HttpResponse("잘못된 접근 입니다.")


def ApiAttendanceModify(request):
    # 수정 필요가 확인 있는 이름
    if request.method == "GET" and request.user.is_authenticated:
        checked_name = request.GET["name"]
        checked_date = request.GET["date"]

        # 수정할 이름
        modi = Attendance.objects.filter(name=checked_name, date=checked_date)
        modi_name = modi[0].name
        modi_date = modi[0].date
        modi_attendance = modi[0].attendance
        poko_image = GetImage.objects.get(pk=3).image.url
        return render(
            request,
            "checking/attendance_noti.html",
            context={
                "modi_name": modi_name,
                "modi_attendance": modi_attendance,
                "modi_date": modi_date,
                "poko_image": poko_image,
            },
        )

    # 수정 된 이름
    if request.method == "POST" and request.user.is_authenticated:
        modied_name = request.POST["modi_name"]
        modied_date = request.POST["modi_date"]
        modied_attendance = request.POST["modi_attendance"]
        modied = Attendance.objects.filter(name=modied_name, date=modied_date)

        if modied.exists():  # 해당하는 객체가 존재하는 경우
            modied_instance = modied.first()  # 필터링된 첫 번째 객체를 가져온다.
            modied_instance.attendance = modied_attendance  # attendance 값을 변경합니다.
            modied_instance.save()  # 변경 사항을 저장한다.

        modied_attendance = modied[0].attendance  # 변경 된 attendance 재선언

        attendance_modied_text = (
            f"{modied_name} 학생은 {modied_attendance}으로 수정이 완료 되었습니다!"
        )
        poko_image = GetImage.objects.get(pk=3).image.url
        return render(
            request,
            "checking/attendance_noti.html",
            {
                "attendance_modied_text": attendance_modied_text,
                "poko_image": poko_image,
            },
        )


# def ApiRegister(request):
#     if request.method == "POST":
#         new_register = Register()
#         new_register.name = request.POST['name']
#         new_register.gender = request.POST['gender']
#         new_register.birth = request.POST['birth']
#         new_register.phone_number = request.POST['phone_number']
#         new_register.email = request.POST['email']
#         new_register.address = request.POST['address']
#         new_register.register_at = timezone.now()
#         new_register.funnels = request.POST['funnels']
#         new_register.save()
#
#     return redirect("/")
