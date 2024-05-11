from django.shortcuts import redirect, render
from django.urls import reverse


class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.user.is_authenticated:
            if not request.path.startswith(reverse("common:login")):
                if (
                    request.path == reverse("common:ApiSignup")
                    and request.method == "GET"
                ):  # 비인증 회원가입
                    print("비인증 회원가입작성-정상")
                    return render(request, "common/signup.html")
                elif (
                    request.path == reverse("common:ApiSignup")
                    and request.method == "POST"
                ):  # 비인증 회원 가입 후
                    pass  # 바로 이동하게 하면 되는 것이었다!
                    print("비인증 회원 가입 후")
                    # return redirect("common:signup")  # view로 Post 값을 보내라 -> 실패
                else:
                    print("비인증 login url이 아닌 경우")
                    return redirect(reverse("common:login"))  # 비인증 login url이 아닌 경우

        response = self.get_response(request)
        return response
