from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = "common"

urlpatterns = [
    path("", views.index_common, name="index_common"),
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="common/login.html"),
        name="login",
    ),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.RegisterForm),
    path("register/create/", views.ApiRegister),
    path("register/climb/", views.ApiClimb),
    # path("register/update/{q.id}", views.ApiRegisterUpdate),
    path("error/", views.ApiError, name="ApiError"),
    path("signup/", views.ApiSignup, name="ApiSignup"),
]
