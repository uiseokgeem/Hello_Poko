from . import views
from django.urls import path

urlpatterns = [
    path("", views.index_attendance),
    path("produce/", views.ApiAttendanceProduce),
    path("date/", views.ApiAttendanceList),
    path("check/", views.ApiAttendanceChecking),
    path("check_modi/", views.ApiAttendanceModify),
    # 5월 10일 기준 사용하지 않는 url
    # path("index_detail/", views.index_detail),
    # path("attendance_detail/", views.attendance_detail),
    # path("attendance_group/", views.attendance_group),
    # path("ind/", views.attendance_ind),
    # path("download_excel/", views.result_excel, name="download_excel"),
]
