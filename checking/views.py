from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render

from .models import Attendance
from .models import Teacher, Member, GetImage
import matplotlib

matplotlib.use("Agg")
from io import StringIO, BytesIO
import pandas as pd


def index(request):
    poko_image = GetImage.objects.get(pk=2).image.url
    return render(request, "checking/index.html", {"poko_image": poko_image})


def index_detail(request):
    poko_image = GetImage.objects.get(pk=2).image.url
    return render(request, "checking/index_detail.html", {"poko_image": poko_image})


def attendace_produce(request):
    poko_image = GetImage.objects.get(pk=3).image.url
    return render(
        request, "checking/attendance_produce.html", context={"poko_image": poko_image}
    )


def date(request):
    if request.method == "POST":
        # 선생님 이름과 날짜를 세션에 저장
        query = request.POST.get("q", "")
        request.session["q"] = query  # 선생님 이름
        date = request.POST.get("date", "")

        names = (
            Member.objects.all()
            .filter(teacher__teacher_name=request.session["q"])
            .values_list("name", flat=True)
        )
        names = sorted(list(names))
        print(names)

        return render(
            request, "checking/attendance_check.html", {"date": date, "names": names}
        )
    else:
        return HttpResponse("잘못된 접근입니다.")


def check_modi(request):
    if request.method == "GET":
        checked_name = request.GET["name"]
        checked_date = request.GET["date"]
        print(checked_name, checked_date)
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

    if request.method == "POST":
        modied_name = request.POST["modi_name"]
        modied_date = request.POST["modi_date"]
        modied_attendance = request.POST["modi_attendance"]
        modied = Attendance.objects.filter(name=modied_name, date=modied_date)

        if modied.exists():  # 해당하는 객체가 존재하는 경우
            modied_instance = modied.first()  # 필터링된 첫 번째 객체를 가져옵니다.
            modied_instance.attendance = modied_attendance  # attendance 값을 변경합니다.
            modied_instance.save()  # 변경 사항을 저장합니다.
        # print("변경 된 attendance", modied[0].attendance)
        modied_attendance = modied[0].attendance  # 변경된 attendance 재선언
        # referer = request.META.get("HTTP_REFERER")
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


def chk(request):
    if request.method == "POST":
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

        # 폼 입력값 가져와서 Attendance의 Attendance에 저장
        attendance = Attendance()
        attendance.name = request.POST["name"]
        attendance.attendance = request.POST["attendance"]
        attendance.date = request.POST["date"]
        attendance.teacher_name = request.session["q"]

        # 명단에 표시 될 학생이름
        names = (
            Member.objects.all()
            .filter(teacher__teacher_name=request.session["q"])
            .values_list("name", flat=True)
        )
        names = sorted(list(names))

        # Member의 attendance에  출결 횟수 저장
        name = request.POST.get("name", "")
        member_info = get_object_or_404(Member, name=name)
        if attendance.attendance == "출석":
            member_info.attendance += 1

        elif attendance.attendance == "결석":
            member_info.absent += 1

        member_info.save()
        attendance.save()

        return render(
            request,
            "checking/attendance_check.html",
            {
                "date": attendance.date,
                "names": names,
            },
        )

    else:
        return HttpResponse("잘못된 접근 입니다.")
