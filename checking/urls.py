from . import views
from django.urls import path
from .views import chk

urlpatterns = [
    path("", views.index),
    path("index/", views.index),  # 뒤로가기
    path("produce/", views.attendace_produce),
    path("date/", views.date),
    path("check/", views.chk),
    path("index_detail/", views.index_detail),
    # path("attendance_detail/", views.attendance_detail),
    # path("attendance_group/", views.attendance_group),
    # path("ind/", views.attendance_ind),
    path("check_modi/", views.check_modi),
    path("download_excel/", views.result_excel, name="download_excel"),
]
