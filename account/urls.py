from . import views
from django.urls import path
from .views import CustomLoginView

app_name = "account"

urlpatterns = [
    path("", CustomLoginView.as_view(template_name="account/login.html")),
    path(
        "login/",
        CustomLoginView.as_view(template_name="account/login.html"),
        name="login",
    ),
    path("logout/", views.ApiLogoutView, name="ApiLogoutView"),
    path("signup/", views.ApiSignup, name="ApiSignup"),
    path("update_pwd", views.ApiUpdatePwd, name="ApiUpdatePwd"),
]