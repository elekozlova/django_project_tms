import os

from django.core.exceptions import EmptyResultSet
from django.http import HttpResponse, HttpRequest
from task4.models import Numbers
from django.views.decorators.csrf import csrf_exempt


def gen_random_name():
    return os.urandom(16).hex()


def get_user(request: HttpRequest):
    return request.COOKIES.get("user")


def get_number(user):
    try:
        obj = Numbers.objects.get(name = user)
        return obj.n
    except Numbers.DoesNotExist:
        obj = Numbers(name=user, n=0)
        obj.save()
        return obj.n


def add_number(user, number):
    try:
        obj = Numbers.objects.get(name = user)
        obj.n += int(number)
        obj.save()
        return obj.n
    except Numbers.DoesNotExist:
        obj = Numbers(name=user, n=number)
        obj.save()
        return obj.n


# def user_exists(user: str) -> bool:
#     n = get_number(user)
#     return n is not None
#
#
# def update_number(user: str, number: int) -> None:
#     old_number = get_number(user)
#     old_number += number
#     obj = Numbers(n=old_number)
#     obj.save()
#     return old_number
#
#
#
# def insert_new_user(user: str, number: int) -> None:
#     obj = Numbers.objects(name=user, n =number)
#     obj.save()
#
#
# def save_number(user: str, number: int) -> None:
#     if user_exists(user):
#         update_number(user, number)
#     else:
#         insert_new_user(user, number)

@csrf_exempt
def view(request: HttpRequest):

    user = get_user(request) or gen_random_name()
    data = request.body.decode()


    if data == "stop":
        result = get_number(user)
    else:
        add_number(user, int(data))
        result = data

    result = HttpResponse(f"Your number: {result}")
    result.set_cookie("user", user)

    return result


# @csrf_exempt
# def view(request:HttpRequest):
#     print(f"body - {request.body.decode()}")
#     print(f"COOKIES - {request.COOKIES}")
#     print(request.headers)
#     print(request.content_params)
#     print(request.GET)
#     print(request.POST)
#     print(request.META)
#     name = ''
#     try:
#         obj = Numbers.objects.get(name = name)
#         number = obj.n
#     except Numbers.DoesNotExist:
#         number = -1
#     return HttpResponse(str(number))






