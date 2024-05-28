from django.shortcuts import redirect
from django.urls import reverse


class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.user.is_authenticated:
            if not request.path.startswith(reverse("account:login")):
                if (
                    request.path == reverse("account:ApiUpdatePwd")
                    and request.method == "GET"
                ):
                    print("비인증 초기비밀번호 계정")
                    pass
                elif (
                    request.path == reverse("account:ApiUpdatePwd")
                    and request.method == "POST"
                ):
                    pass
                else:
                    print("비인증 login url이 아닌 경우")
                    return redirect(reverse("account:login"))

        response = self.get_response(request)
        return response


# middleware는 모든 요청에 대해 검사를 수행하게 되어 성능에 영향을 줄 수 있음.
# elif request.user.is_authenticated:
#     if request.user.check_password("poko0000!"):
#         if not request.path.startswith(reverse("common:login")):
#             return redirect(reverse("common:login"))
