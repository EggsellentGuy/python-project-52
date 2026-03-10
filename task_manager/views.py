from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return render(request, "index.html")


def test_error(request):
    a = None
    a.hello()
    return HttpResponse("ok")
