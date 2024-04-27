from django.contrib.auth import logout
from django.shortcuts import render, redirect
from checking.models import GetImage

# Graph
from graph.views import ApiGraph6week as graph_6week
from graph.views import ApiGraphRatiobyClass as graph_ratiobyclass
from graph.views import ApiGraphWeekly as graph_weekly


def logout_view(request):
    logout(request)
    return redirect("/")


def index_common(request):  # dashboard
    if request.method == "GET" and request.user.is_authenticated:
        poko_image = GetImage.objects.get(pk=2).image.url
        graph_6w, count_text1, count_text2, count_text3 = graph_6week(request)
        graph_rbc = graph_ratiobyclass(request)

        return render(
            request,
            "common/index_common.html",
            context={
                "poko_image": poko_image,
                "graph_6w": graph_6w,
                "graph_rbc": graph_rbc,
                "count_text1": count_text1,
                "count_text2": count_text2,
                "count_text3": count_text3,
            },
        )

    if request.method == "POST" and request.user.is_authenticated:
        date = request.POST.get("date", "")

        poko_image = GetImage.objects.get(pk=2).image.url
        graph_6w, count_text1, count_text2, count_text3 = graph_6week(request)
        graph_rbc = graph_ratiobyclass(request)
        (
            graph_week,
            tabel_student,
            tabel_teacher,
            count_text5,
            count_text6,
            users,
        ) = graph_weekly(request, date)

        return render(
            request,
            "common/index_common.html",
            context={
                "poko_image": poko_image,
                "graph_6w": graph_6w,
                "graph_rbc": graph_rbc,
                "count_text1": count_text1,
                "count_text2": count_text2,
                "count_text3": count_text3,
                "graph_week": graph_week,
                "tabel_student": tabel_student,
                "tabel_teacher": tabel_teacher,
                "users": users,
                "count_text5": count_text5,
                "count_text6": count_text6,
                "date": date,
            },
        )
