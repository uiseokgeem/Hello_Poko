from django.urls import path, include
from . import views

urlpatterns = []

urlpattern_api_v1 = [
    path("", views.TitleListAPIView.as_view(), name="title_list"),
]
# path("<int:pk>", views.post_detail, name="post_detail"),
urlpatterns += [
    path("api_report/", include((urlpattern_api_v1, "api-v1"))),
]
