from django.shortcuts import redirect, render
from django.urls import reverse


class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.user.is_authenticated:
            if not request.path.startswith(reverse("common:login")):
                if (
                    request.path == reverse("common:Apisignup")
                    and request.method == "GET"
                ):  # 비인증 회원가입 작성인 경우
                    return render(request, "common/signup.html")
                elif (
                    request.path == reverse("common:Apisignup")
                    and request.method == "POST"
                ):  # 비인증 회원가입 작성 후인 경우
                    pass  # 바로 이동하게 하면 되는 것이었다!
                else:
                    print("비인증 login url이 아닌 경우")
                    return redirect(reverse("common:login"))  # 비인증 login url이 아닌 경우인 경우

        response = self.get_response(request)
        return response
