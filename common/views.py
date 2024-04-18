from django.contrib.auth import logout
from django.shortcuts import render, redirect
from checking.models import GetImage


def logout_view(request):
    logout(request)
    return redirect("/")


def index_common(request):
    poko_image = GetImage.objects.get(pk=2).image.url
    return render(
        request,
        "common/index_common.html",
        context={"poko_image": poko_image},
    )
