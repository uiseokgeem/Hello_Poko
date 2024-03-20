import json
import math

from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django_pandas.io import read_frame
import matplotlib.pyplot as plt
from openpyxl.workbook import Workbook

from .models import Attendance
from .models import Teacher, Member, GetImage
import matplotlib

matplotlib.use("Agg")
from matplotlib import pyplot as plt, ticker
from matplotlib import font_manager as fm
from matplotlib import rcParams
import numpy as np
from io import StringIO, BytesIO
from matplotlib.ticker import MaxNLocator
import pandas as pd
import os
from pathlib import Path
from datetime import datetime, timedelta


# Create your views here.


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
    # if request.method == "POST":
    # request.session["q"] = query
    query = request.POST["q"]
    request.session["q"] = query  # 선생님 이름
    print("session 확인", request.session["q"])
    date = request.POST["date"]
    # print("date 확인", date)

    if query:
        print("query 있음")
        names = Member.objects.all().filter(teacher__teacher_name=query)
    else:
        print("query 없음")
    poko_image = GetImage.objects.get(pk=2).image.url

    return render(
        request,
        "checking/attendnace_check.html",
        {"date": date, "names": names, "poko_image": poko_image},
    )


# attendance.html에서 입력값을 가져와서 저장하기


def chk(request):
    # 폼 입력값 가져와서 Attendance에 저장
    attendance = Attendance()
    attendance.name = request.POST["name"]
    attendance.attendance = request.POST["attendance"]
    attendance.date = request.POST["date"]
    attendance.teacher_name = request.session["q"]

    print(request.session["q"])  # request.POST["name"])
    # 학생들 이름 전부 가져오기
    names = Member.objects.all().filter(teacher__teacher_name=request.session["q"])

    # 출결 횟수 저장
    name = request.POST["name"]
    member_info = get_object_or_404(Member, name=name)
    if attendance.attendance == "출석":
        member_info.attendance += 1

    elif attendance.attendance == "결석":
        member_info.absent += 1

    member_info.save()
    attendance.save()
    # poko_image_chk = GetImage.objects.get(pk=4).image.url

    return render(
        request,
        "checking/attendnace_check.html",
        {"date": attendance.date, "names": names},
    )


def attendance_detail(request):
    if request.method == "POST":
        date = request.POST.get("date", "")
        # 데이터 프레임 만들기
        filter_date = Attendance.objects.filter(date__icontains=date)
        df = pd.DataFrame(data=filter_date.values())  # 조회한 날짜 기준으로 df 생성

        result = (
            df.groupby(["teacher_name", "attendance"]).size().unstack()
        )  # 출석/결석 2개의 값을 보여주기 위해 groupby 사용한 후 unstack으로 데이터프레임으로 전환
        result = result[["결석", "출석"]]  # 그래프 가독성을 위한 순서 바꾸기

        ## 폰트 설정, 적용되는지 확인 필요
        path = "/Users/ui-seok/Dev/poko/static/AppleGothic.ttf"
        fontprop = fm.FontProperties(fname=path, size=11)
        plt.rcParams["font.family"] = "AppleGothic"
        plt.rcParams["axes.unicode_minus"] = False

        # 그래프 그리기
        ax = result.plot(
            kind="barh",
            stacked=False,
            figsize=(9, 5),
            color=["lightcoral", "lightblue"],
        )
        # 바깥 테두리 제거
        for spine in plt.gca().spines.values():
            spine.set_visible(False)

        # 그래프 제목 및 축 레이블 설정
        plt.xticks(rotation="horizontal", fontproperties=fontprop)
        ax.set_ylabel("")
        ax.xaxis.set_major_locator(ticker.NullLocator())  # x축 눈금 비활성화
        ax.grid(False)
        plt.legend(["결석", "출석"], loc="upper right", prop=fontprop)

        # 그래프에 텍스트로 데이터 표기
        for index, value in enumerate(result["결석"]):
            # 결석이 없는 경우 value nan값으로 그래프 표기가 되지 않음
            # math.isnan() 함수를 사용하여 NaN을 체크하고, NaN이 아닌 경우에만 변환을 시도.
            if not math.isnan(value):
                ax.text(
                    value,
                    index,
                    f"{int(value)}명",
                    ha="left",
                    va="center",
                    fontproperties=fontprop,
                )

            for index, value in enumerate(result["출석"]):
                if not math.isnan(value):
                    ax.text(
                        value,
                        index,
                        f"{int(value)}명",
                        ha="right",
                        va="center",
                        fontproperties=fontprop,
                    )

        # 그래프를 SVG 문자열로 저장
        imgdata = StringIO()
        plt.savefig(imgdata, format="svg")
        imgdata.seek(0)

        # SVG 문자열을 가져와서 전달
        graph = imgdata.getvalue()
        plt.close()

        #######################출결 결과 요약##########################
        # 조회한 주의 출석 총인원 수
        week_count = Attendance.objects.filter(date__icontains=date)
        week_count_df = pd.DataFrame(list(week_count.values()))
        week_count_df = (
            week_count_df.groupby("attendance").size().reset_index(name="count")
        )
        # 결석과 출석의 count 값 불러오기
        absent_count = week_count_df[week_count_df["attendance"] == "결석"][
            "count"
        ].values[0]
        present_count = week_count_df[week_count_df["attendance"] == "출석"][
            "count"
        ].values[0]
        # 리스트로 반환됨, [0]지정 필수

        # 조회한 주의 이름 출석결석 table tab 표기
        tabel_student = Attendance.objects.filter(date__icontains=date)
        tabel_teacher = Teacher.objects.all()

        # names = Member.objects.all().filter(teacher__teacher_name=request.session["q"])

        # html 로직 테스트
        check = []
        for teacher in tabel_teacher:
            teacher.teacher_name
            for student in tabel_student:
                if student.teacher_name == teacher.teacher_name:
                    check.append(student.name)

        # count_text4 = f"{date}의 주일 예배 반별 출석/결석 현황 입니다."
        count_text5 = f"{date}의 주일 예배 출석 {present_count}명/결석 {absent_count}명 입니다."

    else:
        ######################## 두번쨰 그래프 생성 ########################

        ######################## 현재 날짜 기준 최근 5주의 일요일 구하기 ########################
        current_date = datetime.now()  # 현재 요일 확인 (0: 월요일, 1: 화요일, ..., 6: 일요일)
        current_weekday = (
            current_date.weekday()
        )  # 요일, 현재 날짜에서 현재 요일을 뺀 후, 일요일까지의 날짜를 계산
        days_until_sunday = (current_weekday - 6) % 7  # 메모 참조
        pre_sunday = current_date - timedelta(days=days_until_sunday)
        print(pre_sunday.strftime("%Y-%m-%d"))
        presunday_text = pre_sunday.strftime("%m-%d")

        list_sunday = [pre_sunday]
        for i in range(1, 6):
            # 최근 주일 기준으로 확인할 주간 설정(현재코드에서는 5주+현재 주간), 단 조회하려는 주간에 데이터가 동일하게 있어야함, 출석인원 변동 고려
            list_sunday.append(pre_sunday - timedelta(weeks=i))
        date_strings = [dt.strftime("%Y-%m-%d") for dt in list_sunday]
        print("날짜 확인", len(date_strings), date_strings)

        ######################## 현재 날짜 기준 최근 5주의 일요일 구하기 ########################
        # 최근 5주간의 일요일 date 리스트로 데이터프레임 생성 후 병합하기
        empty_df = pd.DataFrame()
        for i in range(len(date_strings)):
            attendane_account = Attendance.objects.filter(
                date__icontains=date_strings[i]
            )
            attendance_df = pd.DataFrame(list(attendane_account.values()))
            frames = [empty_df, attendance_df]
            empty_df = pd.concat(frames, ignore_index=True)
            # 인원이 변동되어 데이터프레임의 길이가 맞지않아 concat이 되지 않을 것을 대비해 데이터프레임 형태 확인하기

        empty_df["date"] = pd.to_datetime(empty_df["date"]).dt.strftime(
            "%m-%d"
        )  # 그래프에 표기 될 날짜 형식 변경
        attendance_counts = (
            empty_df[empty_df["attendance"] == "출석"]
            .groupby("date")
            .size()
            .reset_index(name="attendance")
        )

        path = "/Users/ui-seok/Dev/poko/static/AppleGothic.ttf"
        fontprop = fm.FontProperties(fname=path, size=11)
        plt.rcParams["font.family"] = "AppleGothic"
        plt.rcParams["axes.unicode_minus"] = False

        # 그래프 그리기
        plt.figure(figsize=(10, 6))
        plt.plot(
            attendance_counts["date"],
            attendance_counts["attendance"],
            marker="o",
            linestyle="-",
            color="lightcoral",
        )

        # 그래프에 데이터를 텍스트로 표기
        for date, count in zip(
            attendance_counts["date"], attendance_counts["attendance"]
        ):
            plt.annotate(
                f"{count}명",
                (date, count),
                textcoords="offset points",
                xytext=(0, 10),
                ha="center",
            )

        # y축의 범위를 정수로 표현하도록 설정
        plt.gca().yaxis.set_major_locator(ticker.MaxNLocator(integer=True))

        # y축 눈금의 값에 '명' 추가
        tick_labels = [f"{int(val)}명" for val in plt.gca().get_yticks()]
        plt.gca().set_yticklabels(tick_labels)

        # plt.title("날짜별 출석 수")
        # plt.xlabel("날짜")
        # plt.ylabel("출석 인원")
        plt.yticks([])  # y축 눈금 비활성화

        # 바깥 테두리 제거
        for spine in plt.gca().spines.values():
            spine.set_visible(False)

        # 그래프를 SVG 문자열로 저장
        imgdata = StringIO()
        plt.savefig(imgdata, format="svg")
        imgdata.seek(0)

        # SVG 문자열을 가져와서 전달
        count_graph = imgdata.getvalue()

        ############### 총 인원 요약 ################
        names_list = Member.objects.all().values_list("name", flat=True)  # 제적인원 구하기
        # 지난 일요일 출석 인원수 구하기
        # print("요일 확인", presunday_text)
        attendance_value = attendance_counts[
            attendance_counts["date"] == presunday_text
        ]
        # print("확인", attendance_value)
        attendance_value = attendance_value["attendance"].values[0]
        # -> 반영 되어야 할 기간의 출석 데이터가 없으면 오류가 발생함

        names_count = len(names_list)
        count_text1 = f"{presunday_text} 주일 기준 지난 6주간 출석 현황 입니다."
        count_text2 = f"{current_date.strftime('%Y-%m-%d')} 기준 제적 총 {names_count} 명으로"
        count_text3 = f"{presunday_text} 주일 예배 출석 인원은 총 {attendance_value}명 입니다."

        return render(
            request,
            "checking/attendance_detail.html",
            context={
                "count_graph": count_graph,
                "count_text1": count_text1,
                "count_text2": count_text2,
                "count_text3": count_text3,
            },
        )

    return render(
        request,
        "checking/attendance_detail.html",
        {
            "date": date,
            "filter_date": filter_date,
            "name": "이름",
            "chk": "출결",
            "graph": graph,
            # "count_text4": count_text4,
            "count_text5": count_text5,
            "tabel_teacher": tabel_teacher,
            "table_student": tabel_student,
        },
    )


def attendance_group(request):  # 전체기간 반별 출결률 조회
    # 퍼센티지 계산에 필요한 attendance, absent + teacher,name 데이터 확보
    attendance_data = Member.objects.all()
    # print("확인 입니다.", attendance_data[0].teacher, attendance_data[0].name)

    # 데이터 프레임 만들기
    attendance_df = pd.DataFrame(columns=["teacher", "name", "attendance", "absent"])
    for i in range(len(attendance_data)):
        attendance_dict = {
            "teacher": str(attendance_data[i].teacher),
            "name": attendance_data[i].name,
            "attendance": attendance_data[i].attendance,
            "absent": attendance_data[i].absent,
        }
        attendance_df = attendance_df._append(attendance_dict, ignore_index=True)

    # 데이터 프레임 연산을 통해 전체 출결횟수 합기준 출석률과 결석률 계산
    attendance_sum = (
        attendance_df.groupby("teacher")[["attendance", "absent"]].sum().reset_index()
    )  # attendance 횟수와 absent 횟수 각각 총합 계산
    attendance_sum["total"] = (
        attendance_sum["attendance"] + attendance_sum["absent"]
    )  # 전체 출결횟수 = attendance 횟수 총합 + absent  횟수 총합
    # print(attendance_sum)

    # 전체 출결일수에서 attendance 횟수와 absent 횟수의 비율을 계산 후 attendance_ratio, absent_ratio 컬럼 추가
    attendance_sum["attendance_ratio"] = (
        attendance_sum["attendance"] / attendance_sum["total"]
    )  # 에러 발생 새로운 col '조계원' col에 대한 데이터가 없어 연산을 실행하지 못함 -> 해당 데이터가 없어도 연산이 실행 되게끔 해야함.
    attendance_sum["absent_ratio"] = attendance_sum["absent"] / attendance_sum["total"]

    attendance_grouped = (
        attendance_sum.groupby("teacher")[["attendance_ratio", "absent_ratio"]]
        .sum()
        .reset_index()
    )

    print(attendance_grouped)

    ## 폰트 설정, 적용되는지 확인 필요
    path = "/Users/ui-seok/Dev/poko/static/AppleGothic.ttf"
    fontprop = fm.FontProperties(fname=path, size=11)
    plt.rcParams["font.family"] = "AppleGothic"
    plt.rcParams["axes.unicode_minus"] = False

    # 그래프 그리기
    ax = attendance_grouped.plot(
        x="teacher",
        kind="bar",
        color=["lightblue", "lightcoral"],
        figsize=(8, 4),
        stacked=True,
    )

    # 바깥 테두리 제거
    for spine in plt.gca().spines.values():
        spine.set_visible(False)

    # 그래프에 텍스트 표기 하기
    for p in ax.patches:
        height = p.get_height()
        width = p.get_width()
        x, y = p.get_xy()
        ax.text(x + width / 2, y + height, f"{height:.1f}", ha="center", va="bottom")

    # 그래프 제목 및 축 레이블 설정
    plt.xticks(
        rotation="horizontal",
        fontproperties=fontprop,
    )
    plt.yticks([])  # y축 눈금 비활성화
    plt.xlabel("")
    # plt.ylabel("출석/결석 비율")
    # plt.title("전체 기간 반별 출석/결석 비율")
    # 범례 추가 및 설정
    plt.legend(["출석", "결석"], loc="upper right", prop=fontprop)

    # 그래프를 SVG 문자열로 저장
    imgdata = StringIO()
    plt.savefig(imgdata, format="svg")
    imgdata.seek(0)

    # SVG 문자열을 가져와서 전달
    graph = imgdata.getvalue()

    return render(
        request,
        "checking/attendance_group.html",
        {"graph": graph},
    )


def attendance_ind(request):
    query = request.POST["q_ind"]
    request.session["q_ind"] = query  # 선생님 이름

    teacher = Teacher.objects.filter(teacher_name=query)
    teacher_id = teacher.values("id")[0]["id"]

    inv_rate = Member.objects.filter(teacher_id=teacher_id).values()
    inv_rate_df = pd.DataFrame(data=inv_rate)

    # 데이터 프레임 연산을 통해 전체 출결일수합기준 출석률과 결석률 계산
    df_sum = (
        inv_rate_df.groupby("name")[["attendance", "absent"]].sum().reset_index()
    )  # attendance 횟수와 absent 횟수 각각 총합 계산
    df_sum["total"] = df_sum["attendance"] + df_sum["absent"]

    # 전체 출결일수에서 attendance 횟수와 absent 횟수의 비율을 계산 및 attendance_ratio, absent_ratio 컬럼 추가
    df_sum["attendance_ratio"] = df_sum["attendance"] / df_sum["total"]
    df_sum["absent_ratio"] = df_sum["absent"] / df_sum["total"]

    df_grouped = (
        df_sum.groupby("name")[["attendance_ratio", "absent_ratio"]].sum().reset_index()
    )

    ## 폰트 설정, 적용되는지 확인 필요
    path = "/Users/ui-seok/Dev/poko/static/AppleGothic.ttf"
    fontprop = fm.FontProperties(fname=path, size=11)
    plt.rcParams["font.family"] = "AppleGothic"
    plt.rcParams["axes.unicode_minus"] = False

    # 그래프 그리기
    ax = df_grouped.plot(
        x="name",
        kind="bar",
        color=["lightblue", "lightcoral"],
        figsize=(8, 4),
        stacked=True,
    )

    # 바깥 테두리 제거
    for spine in plt.gca().spines.values():
        spine.set_visible(False)

    # 그래프에 텍스트 표기 하기
    for p in ax.patches:
        height = p.get_height()
        width = p.get_width()
        x, y = p.get_xy()
        ax.text(x + width / 2, y + height, f"{height:.1f}", ha="center", va="bottom")

    # 그래프 제목 및 축 레이블 설정
    plt.xticks(
        rotation="horizontal",
        fontproperties=fontprop,
    )
    plt.xlabel("")
    plt.ylabel("")
    plt.yticks([])  # y축 눈금 비활성화
    # plt.title("전체 기간 개인 출석/결석 비율")
    plt.legend(["출석", "결석"], loc="upper right", prop=fontprop)

    # 그래프를 SVG 문자열로 저장
    imgdata = StringIO()
    plt.savefig(imgdata, format="svg")
    imgdata.seek(0)

    # SVG 문자열을 가져와서 전달
    graph = imgdata.getvalue()

    #######################################################
    # 전체기간 개인 날짜별 출결 현황 table tab 표기
    table_data = Attendance.objects.filter(teacher_name__icontains=query).order_by(
        "-date"
    )
    teacher_data = Teacher.objects.filter(teacher_name__icontains=query)
    teacher_key = str(teacher_data.values("id")[0]["id"])
    print("유형 확인", type(teacher_data))
    print("문자열로 변환된 teacher_key:", type(teacher_key))
    table_student = Member.objects.filter(teacher=teacher_key)

    # 개인별 출결일 결과 텍스트 생성
    inv_date = Attendance.objects.filter(teacher_name=query)
    inv_date_df = pd.DataFrame(data=inv_date.values())
    result = inv_date_df.groupby(["name", "date"])["attendance"].max().unstack()

    result.columns = pd.to_datetime(result.columns).strftime("%m-%d")

    index_values = result.index
    columns_names = result.columns

    print("Index values:", index_values)
    print("Column names:", columns_names)

    # result["date"] = pd.to_datetime(result["date"])
    # result["date"] = result["date"].dt.strftime("%m-%d")

    request.session["result_df"] = result.to_json()
    # print(inv_date_df)
    print(result)

    return render(
        request,
        template_name="checking/attendance_ind.html",
        context={
            "graph": graph,
            "query": query,
            "table_data": table_data,
            "table_student": table_student,
        },
    )


def result_excel(request):
    # 세션에서 데이터프레임 가져오기
    df_json = request.session.get("result_df", None)

    if df_json:
        # JSON 형태의 데이터프레임을 다시 DataFrame으로 변환
        result_down = pd.read_json(StringIO(df_json))

        # Excel 파일로 변환
        excel_file = BytesIO()
        result_down.to_excel(excel_file, index=True, header=True, engine="openpyxl")
        excel_file.seek(0)

        # HttpResponse로 반환
        response = HttpResponse(
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        response["Content-Disposition"] = "attachment; filename=output_modified.xlsx"
        response.write(excel_file.getvalue())

        return response
