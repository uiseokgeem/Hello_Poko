from django.shortcuts import redirect, render
from django.urls import reverse


class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.user.is_authenticated:
            if not request.path.startswith(reverse("common:login")):
                return redirect(reverse("common:login"))  # 비인증 login url이 아닌 경우인 경우

        # middleware는 모든 요청에 대해 검사를 수행하게 되어 성능에 영향을 줄 수 있음.
        # elif request.user.is_authenticated:
        #     if request.user.check_password("poko0000!"):
        #         if not request.path.startswith(reverse("common:login")):
        #             return redirect(reverse("common:login"))

        response = self.get_response(request)
        return response
