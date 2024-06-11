from . import views
from . import api
from django.urls import path, include
from .views import CustomLoginView

app_name = "accounts"

# View
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
    path("reset_pwd", views.ApiResetPwd.as_view(), name="ApiResetPwd"),
    path(
        "reset/<uidb64>/<token>/",
        views.ApiResetPwdConfirm.as_view(),
        name="ApiResetPwdConfirm",
    ),
]

# DRF
account_api_v1 = [
    path("send_email/", api.SendEmailAPIView.as_view(), name="send_email"),
    path(
        "confirm_email/<str:url_code>/",
        api.ConfirmEmailAPIView.as_view(),
        name="confirm_email",
    ),
    path("register/", api.CustomResisterAPIView.as_view(), name="register"),
    # path("register/", include("dj_rest_auth.registration.urls"), name="register"),
]

urlpatterns += [
    path("api/", include((account_api_v1, "accounts-v1"))),
]
