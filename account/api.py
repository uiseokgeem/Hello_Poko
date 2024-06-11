# 이메일 인증 api
from rest_framework import status
from rest_framework.response import Response
from rest_framework.request import Request
from django.contrib.auth.views import PasswordResetView
from django.contrib.auth.forms import PasswordResetForm
from rest_framework.views import APIView
from django.core.mail import send_mail
from .serializers import SendEmailSerializer
import random
import string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes


class SendEmailAPIView(APIView):
    def post(self, request):
        serializer = SendEmailSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]

            code = "".join(random.choices(string.ascii_uppercase + string.digits, k=6))
            url_code = urlsafe_base64_encode(force_bytes(code))

            # note : RESTful API와 같은 상황에서는 상태를 유지하지 않는(stateless) 방식이 일반적이라고 함.
            # api-test.http 요청 시 session none으로 출력 됨.

            # url_session = urlsafe_base64_encode(
            #     force_bytes(request.session.get("session_d"))
            # )

            protocol = "http"  # 서비스 프로토콜 = rquest.is_secure
            domain = "localhost:8000"  # 서비스 도메인 = request.get_host()
            code_confirm_url = f"{protocol}://{domain}/api/confirm_email/{url_code}/"
            print(code_confirm_url)

            send_mail(
                "안녕하세요. POKO 입니다!",
                f"회원가입을 위한 코드입니다. {code}, {code_confirm_url}",
                "es468@naver.com",  # 발신자 이메일
                [email],
                fail_silently=False,
            )

            return Response(
                {"message": "입력한 이메일로 코드가 인증코드가 발송 되었습니다."},
                status=status.HTTP_200_OK,
            )
        return Response(
            data={"message": "이메일 주소가 올바르지 않습니다. 다시 시도해주세요."},
            status=status.HTTP_400_BAD_REQUEST,
        )


class ConfirmEmailAPIView(APIView):
    def get(self, request, url_code):
        check_url_code = urlsafe_base64_decode(url_code).decode()  # 디코딩 확인용

        return Response(
            {"message": f"CODE 입력확인: {check_url_code}"}, status=status.HTTP_200_OK
        )

    def post(self, request, url_code):  # 입력한 인증 코드로 post 요청
        check_url_code = urlsafe_base64_decode(url_code).decode()  #

        # 여기에 URL 코드 검증 및 이메일 인증 로직을 추가합니다.
        # 예: 코드가 유효한지, 이미 사용되었는지, 유효 기간이 지났는지 등
        # 예를 들어, 캐시에 저장한 코드를 확인하는 경우:
        # email = url_code
        # email = cache.get(url_code)
        # if email:
        #     # cache.delete(url_code)  # 일회성 코드 사용 후 삭제
        #     return Response(
        #         {"message": "Email confirmed successfully"}, status=status.HTTP_200_OK
        #     )
        # else:
        #     return Response(
        #         {"error": "Invalid or expired code"}, status=status.HTTP_400_BAD_REQUEST
        #     )

    # return Response({'message': 'Email confirmation not implemented yet'}, status=status.HTTP_200_OK)
