from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer
from rest_framework.generics import ListAPIView
from report.serializers import TitleListSerializer
from rest_framework.utils.serializer_helpers import ReturnDict


class TitleListAPIView(ListAPIView):
    serializer_class = TitleListSerializer

    def get_queryset(self):
        return TitleListSerializer.get_optimized_queryset(self.request)  # self?

    # 응답데이터 구조 변경하기위한 list() 메서드 오버라이드
    def list(self, request: Request, *args, **kwargs):
        response: Response = super().list(request, *args, **kwargs)

        if isinstance(request.accepted_renderer, (JSONRenderer, BrowsableAPIRenderer)):
            response.data = ReturnDict(
                {
                    "ok": True,
                    "result": response.data,
                },
                serializer=response.data.serializer,
            )
        return response


post_list_view = TitleListAPIView.as_view()
