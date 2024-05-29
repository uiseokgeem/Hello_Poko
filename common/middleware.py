from django.shortcuts import redirect, render
from django.urls import reverse


class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.user.is_authenticated :
            if request.path != reverse('account:login') and request.path != reverse('account:ApiSignup') and request.path != reverse('account:ApiUpdatePwd'):  # 로그인 페이지가 아닐 경우에만 리다이렉트
                return redirect(reverse('common:login'))
        else:
            pass
        response = self.get_response(request)
        return response

# middleware는 모든 요청에 대해 검사를 수행하게 되어 성능에 영향을 줄 수 있음.
# elif request.user.is_authenticated:
#     if request.user.check_password("poko0000!"):
#         if not request.path.startswith(reverse("common:login")):
#             return redirect(reverse("common:login"))
