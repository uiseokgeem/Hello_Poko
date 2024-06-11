from django.urls import path
from . import views

app_name = "common"

urlpatterns = [
    path("manager/", views.ApiIndexManager, name="ApiIndexManager"),
    path("user/", views.ApiIndexUser, name="ApiIndexUser"),
    # path("register/", views.RegisterForm),
    path("register/create/", views.ApiNewRegister, name="ApiNewRegister"),
    path("register/climb/", views.ApiClimb),
    path("error/", views.ApiError, name="ApiError"),
    # 5월 22일 기준 사용하지 않는 url
    # path("register/update/{q.id}", views.ApiRegisterUpdate),
    # path(
    #     "update_pwd/",
    #     CustomPasswordResetView.as_view(template_name="common/update_pwd.html"),
    #     name="CustomPasswordResetView",
    # ),
    # path(
    #         "update_pwd/done/",
    #         CustomPasswordChangeDoneView.as_view(),
    #         name="CustomPasswordChangeDoneView",
    #     ),
    # 5월 28일 회원가입 로그인 체계 구현으로 accounts app으로 이전
    # path("", CustomLoginView.as_view(template_name="common/login.html")),
    # path(
    #     "login/",
    #     CustomLoginView.as_view(template_name="common/../templates/accounts/login.html"),
    #     name="login",
    # ),
    # path("update_pwd", views.ApiUpdatePwd, name="ApiUpdatePwd"),
    # path("logout/", views.ApiLogoutView, name="ApiLogoutView"),
    # path("signup/", views.ApiSignup, name="ApiSignup"),
]
