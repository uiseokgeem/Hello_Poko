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
