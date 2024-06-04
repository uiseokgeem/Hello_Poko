from . import views
from . import api
from django.urls import path, include

app_name = "blog"

urlpatterns = []

urlpattern_api_v1 = [
    path("", api.post_list, name="post_list"),
    path("<int:pk>", api.post_detail, name="post_detail"),
]

urlpatterns += [
    path("api/", include((urlpattern_api_v1, "api-v1"))),
]
