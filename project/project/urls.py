
from django.contrib import admin
from django.http import HttpRequest
from django.http import HttpResponse
from django.urls import path
from task4.views import view


def hello_world(request: HttpRequest):
    return HttpResponse("hello world")

urlpatterns = [
    path('admin/', admin.site.urls),
    path("hw/", hello_world),
    path("task4/", view),
]
