from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = "common"

urlpatterns = [
    path("", views.index_common,name = 'index_common'),
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="common/login.html"),
        name="login",
    ),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.RegisterForm),
    path("register/create/", views.ApiRegister, name='ApiRegister')

]
