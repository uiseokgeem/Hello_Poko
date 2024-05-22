from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import CustomLoginView


app_name = "common"

urlpatterns = [
    path("", CustomLoginView.as_view(template_name="common/login.html")),
    path("manager/", views.ApiIndexManager, name="ApiIndexManager"),
    path("user/", views.ApiIndexUser, name="ApiIndexUser"),
    path(
        "login/",
        CustomLoginView.as_view(template_name="common/login.html"),
        name="login",
    ),
    path("update_pwd", views.ApiUpdatePwd, name="ApiUpdatePwd"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.RegisterForm),
    path("register/create/", views.ApiRegister),
    path("register/climb/", views.ApiClimb),
    path("error/", views.ApiError, name="ApiError"),
    path("signup/", views.ApiSignup, name="ApiSignup"),
    # 5월 22일 기준 사용하지 않는 url
    # path("register/update/{q.id}", views.ApiRegisterUpdate),
    # path(
    #     "update_pwd/",
    #     CustomPasswordResetView.as_view(template_name="common/update_pwd.html"),
    #     name="CustomPasswordResetView",
    # ),
]
