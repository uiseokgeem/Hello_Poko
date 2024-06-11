# Libray
import math
import pandas as pd
from io import StringIO, BytesIO
from datetime import datetime, timedelta
from django.http import HttpResponse

# Graph
from matplotlib import pyplot as plt, ticker
from matplotlib import font_manager as fm

# Models
from checking.models import Attendance, Member
from django.contrib.auth.models import User


def ApiGraph6week(request):
    # 현재 날짜 기준 최근 5주의 일요일 구하기
    current_date = datetime.now()  # 현재 요일 확인 (0: 월요일, 1: 화요일, ..., 6: 일요일)
    current_weekday = current_date.weekday()  # 요일, 현재 날짜에서 현재 요일을 뺀 후, 일요일까지의 날짜를 계산
    days_until_sunday = (current_weekday - 6) % 7
    pre_sunday = current_date - timedelta(days=days_until_sunday)
    presunday_text = pre_sunday.strftime("%m-%d")  # 직전 주일 날짜

    list_sunday = [pre_sunday]
    for i in range(
        1, 6
    ):  # 최근 주일 기준으로 확인할 주간 설정(현재코드에서는 5주+현재 주간), 단 조회하려는 주간에 데이터가 동일하게 있어야함, 출석인원 변동 고려
        list_sunday.append(pre_sunday - timedelta(weeks=i))
    date_strings = [dt.strftime("%Y-%m-%d") for dt in list_sunday]

    # 최근 5주간의 일요일 date 리스트로 데이터프레임 생성 후 병합하기
    empty_df = pd.DataFrame()
    for i in range(len(date_strings)):
        attendane_account = Attendance.objects.filter(date__icontains=date_strings[i])
        attendance_df = pd.DataFrame(list(attendane_account.values()))
        frames = [empty_df, attendance_df]
        empty_df = pd.concat(
            frames, ignore_index=True
        )  # 인원이 변동되어 데이터프레임의 길이가 맞지않아 concat이 되지 않을 것을 대비해 데이터프레임 형태 확인하기

    # 그래프에 표기 될 날짜 형식 변경
    empty_df["date"] = pd.to_datetime(empty_df["date"]).dt.strftime("%m-%d")

    # 주간별 출석인원 수 데이터프레임 생성
    attendance_counts = (
        empty_df[empty_df["attendance"] == "출석"]
        .groupby("date")
        .size()
        .reset_index(name="attendance")
    )

    path = "./static/AppleGothic.ttf"
    fontprop = fm.FontProperties(fname=path, size=11)

    # 폰트 속성 설정
    plt.rcParams["font.family"] = "AppleGothic"
    plt.rcParams["axes.unicode_minus"] = False

    # 그래프 그리기
    plt.figure(figsize=(10, 6))  # 10, 6
    plt.plot(
        attendance_counts["date"],
        attendance_counts["attendance"],
        marker="o",
        linestyle="-",
        color="lightcoral",
    )

    # 그래프에 데이터를 텍스트로 표기
    for date, count in zip(attendance_counts["date"], attendance_counts["attendance"]):
        plt.annotate(
            f"{count}명",
            (date, count),
            textcoords="offset points",
            xytext=(0, 10),
            ha="center",
            fontproperties=fontprop,
        )

    # y축의 범위를 정수로 표현하도록 설정
    plt.gca().yaxis.set_major_locator(ticker.MaxNLocator(integer=True))
    plt.yticks([])  # y축 눈금 비활성화

    # 바깥 테두리 제거
    for spine in plt.gca().spines.values():
        spine.set_visible(False)

    # 그래프를 SVG 문자열로 저장
    imgdata = StringIO()
    plt.savefig(imgdata, format="svg")
    imgdata.seek(0)

    # SVG 문자열을 가져와서 전달
    graph_6w = imgdata.getvalue()

    # information 출력 내용

    # 제적인원 구하기
    names_list = Member.objects.all().values_list("name", flat=True)
    # 직전 일요일 출석 인원수 구하기
    attendance_value = attendance_counts[attendance_counts["date"] == presunday_text]
    attendance_value = attendance_value["attendance"].values[0]
    # -> 반영 되어야 할 기간의 출석 데이터가 없으면 오류가 발생함

    names_count = len(names_list)
    current_date = current_date.strftime("%Y-%m-%d")
    year, month, day = current_date.split("-")  # 결과 내용에 활용할 오늘 날짜
    presunday_month, presunday_day = presunday_text.split("-")
    print(presunday_text, year, month, day)

    count_text1 = f" {year}년 {presunday_month}월 {presunday_day}일 주일 기준 6주간 출석 현황 입니다."
    count_text2 = f"{year}년 {month}월 {day}일 기준 제적 총 {names_count}명으로"
    count_text3 = (
        f"{presunday_month}월 {presunday_day}일 주일 출석은 총 {attendance_value}명 입니다."
    )

    return graph_6w, count_text1, count_text2, count_text3


def ApiGraphRatiobyClass(request):
    # 퍼센티지 계산에 필요한 attendance, absent + teacher_name 데이터 확보
    attendance_data = Member.objects.all()

    # 데이터 프레임 만들기
    attendance_df = pd.DataFrame(columns=["name", "attendance", "absent"])

    for i in range(len(attendance_data)):
        attendance_dict = {
            "teacher_id": attendance_data[i].teacher_id,
            "name": attendance_data[i].name,
            "attendance": attendance_data[i].attendance_count,
            "absent": attendance_data[i].absent_count,
        }
        attendance_df = attendance_df._append(attendance_dict, ignore_index=True)

    print("수정확인", attendance_df)

    # user model 테이블 생성

    users = User.objects.all()  # User모델에서 그래프에 반영할 teacher_name 생성
    user_df = pd.DataFrame(columns=["teacher_id", "teacher_name"])

    for user in users:
        user_info = [
            user.username,
            user.first_name + user.last_name,
        ]
        user_df = user_df._append(
            pd.Series(user_info, index=user_df.columns), ignore_index=True
        )

    print("user_df 확인", user_df)

    df = pd.merge(
        attendance_df, user_df, on="teacher_id", how="left"
    )  # teacher_id 기준으로 merge

    print("확인", df)

    # 데이터 프레임 연산을 통해 전체 출결횟수 합기준 출석률과 결석률 계산
    attendance_sum = (
        attendance_df.groupby("teacher_id")[["attendance", "absent"]]
        .sum()
        .reset_index()
    )  # attendance 횟수와 absent 횟수 각각 총합 계산

    print("attendance_sum, 확인", attendance_sum)

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
        attendance_sum.groupby("teacher_id")[["attendance_ratio", "absent_ratio"]]
        .sum()
        .reset_index()
    )

    # user_df를 통해 teacher_id로 teacher_name 생성 후 그래프 생성

    ## 폰트 설정
    path = "./static/AppleGothic.ttf"
    fontprop = fm.FontProperties(fname=path, size=11)

    ## 폰트 속성 설정
    plt.rcParams["font.family"] = "AppleGothic"
    plt.rcParams["axes.unicode_minus"] = False

    # 그래프 그리기
    ax = attendance_grouped.plot(
        x="teacher_id",
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

    # 범례 추가 및 설정
    plt.legend(["출석", "결석"], loc="upper right", prop=fontprop)

    # 그래프를 SVG 문자열로 저장
    imgdata = StringIO()
    plt.savefig(imgdata, format="svg")
    imgdata.seek(0)

    # SVG 문자열을 가져와서 전달
    graph_rbc = imgdata.getvalue()

    return graph_rbc


def ApiGraphWeekly(request, date):
    if request.method == "POST":
        date = request.POST.get("date", "")

        # models.py 수정후 새로운 ApiGraphWeekly 로직
        users = User.objects.all()  #

        AttendanceToTeacher = (
            Attendance.objects.select_related("name__teacher")
            .values(
                "name__teacher__username",
                "name__teacher__first_name",
                "name__teacher__last_name",
                "name__name",
                "attendance",
                "date",
            )
            .filter(date__icontains=date)
        ).order_by("attendance")

        AttendanceToTeacher_df = pd.DataFrame(data=AttendanceToTeacher)
        AttendanceToTeacher_df["teacher_name"] = (
            AttendanceToTeacher_df["name__teacher__first_name"]
            + AttendanceToTeacher_df["name__teacher__last_name"]
        )

        print("AttendanceToTeacher_df 확인", AttendanceToTeacher_df)

        # 출석/결석 2개의 값을 보여주기 위해 groupby 사용한 후 unstack으로 데이터프레임으로 전환
        result = (
            AttendanceToTeacher_df.groupby(["teacher_name", "attendance"])
            .size()
            .unstack()
        )
        result = result[["결석", "출석"]]  # 그래프 가독성을 위한 순서 바꾸기

        ## 폰트 설정, 적용되는지 확인 필요
        path = "./static/AppleGothic.ttf"
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
        plt.yticks(rotation="horizontal", fontproperties=fontprop)
        ax.set_ylabel("")
        ax.xaxis.set_major_locator(ticker.NullLocator())  # x축 눈금 비활성화
        ax.grid(False)
        plt.legend(["결석", "출석"], loc="lower right", prop=fontprop)

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
        graph_weekly = imgdata.getvalue()
        plt.close()

        # information 출력 내용

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

        # 조회한 주의 이름 출석결석 table tab 표기
        tabel_teacher = list(AttendanceToTeacher_df["teacher_name"].values)
        year, month, day = date.split("-")

        # 알림창 내용
        count_text5 = f"{year}년 {month}월 {day}일 주간 출결 입니다."
        count_text6 = f"출석 {present_count}명/결석 {absent_count}명 입니다."

        return (
            graph_weekly,
            AttendanceToTeacher,
            tabel_teacher,
            count_text5,
            count_text6,
            users,
        )


def ApiGraphIndividual(request):
    try:
        if request.user.is_authenticated:
            teacher_name = request.user

        inv_rate = Member.objects.filter(teacher=teacher_name).values()
        inv_rate_df = pd.DataFrame(data=inv_rate)

        # 데이터 프레임 연산을 통해 전체 출결일수합기준 출석률과 결석률 계산
        df_sum = (
            inv_rate_df.groupby("name")[["attendance_count", "absent_count"]]
            .sum()
            .reset_index()
        )  # attendance 횟수와 absent 횟수 각각 총합 계산
        df_sum["total"] = df_sum["attendance_count"] + df_sum["absent_count"]

        # 전체 출결일수에서 attendance 횟수와 absent 횟수의 비율을 계산 및 attendance_ratio, absent_ratio 컬럼 추가
        df_sum["attendance_ratio"] = df_sum["attendance_count"] / df_sum["total"]
        df_sum["absent_ratio"] = df_sum["absent_count"] / df_sum["total"]

        df_grouped = (
            df_sum.groupby("name")[["attendance_ratio", "absent_ratio"]]
            .sum()
            .reset_index()
        )

        ## 폰트 설정, 적용되는지 확인 필요
        path = "./static/AppleGothic.ttf"
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
            ax.text(
                x + width / 2, y + height, f"{height:.1f}", ha="center", va="bottom"
            )

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
        graph_ind = imgdata.getvalue()

        #######################################################

        # 전체기간 개인 날짜별 출결 현황 table tab 표기
        table_data = (
            Attendance.objects.select_related("name__teacher")
            .values(
                "name__teacher__username",
                "name__name",
                "attendance",
                "date",
            )
            .filter(name__teacher__username=teacher_name)
            .order_by("-date")
        )

        inv_date_df = pd.DataFrame(data=table_data.values())
        print(inv_date_df)

        table_student = Member.objects.filter(teacher=teacher_name)
        result = inv_date_df.groupby(["name_id", "date"])["attendance"].max().unstack()
        result.columns = pd.to_datetime(result.columns).strftime("%m-%d")

        index_values = result.index
        columns_names = result.columns

        print(result)
        print("Index values:", index_values)
        print("Column names:", columns_names)

        # 개인별 출결일 결과 텍스트 생성
        # inv_date = Attendance.objects.filter(teacher_name=query)
        # inv_date_df = pd.DataFrame(data=inv_date.values())

        # result["date"] = pd.to_datetime(result["date"])
        # result["date"] = result["date"].dt.strftime("%m-%d")
        #
        # # request.session["result_df"] = result.to_json()  # 엑셀 다운로드에 필요한 result
        # # print(inv_date_df)
        # print(result)

        return graph_ind, result
    except:
        return HttpResponse("데이터가 없습니다.")


def ApiResultExcel(request):
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
