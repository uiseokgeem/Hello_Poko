from . import views
from . import api
from django.urls import path, include

app_name = "blog"

urlpatterns = []

# urlpattern_api_v1 = [
#     path("", api.PostListAPIView.as_view(), name="post_list"),
#     path("<int:pk>", api.PostRetrieveAPIView.as_view(), name="post_detail"),
#     path("new/", api.PostCreateAPIView.as_view(), name="post_new"),
#     path("<int:pk>/edit/", api.PostUpdateAPIView.as_view(), name="post_edit"),
#     path("<int:pk>/delete/", api.PostDestroyAPIView.as_view(), name="post_delete"),
# ]
#
# urlpatterns += [
#     path("api/", include((urlpattern_api_v1, "api-v1"))),
# ]
