import os
import json

from django.core.exceptions import PermissionDenied
from django.http import HttpResponse, HttpRequest, JsonResponse
from django.views.decorators.http import require_http_methods
from task4.models import Numbers
from django.views.decorators.csrf import csrf_exempt

#"MY_VERSION"


def get_user(request: HttpRequest):
    return request.headers.get("x-user")


def set_user_name(response: HttpResponse, name: str) -> None:
     response.headers["x-user"] = name


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
        obj.n += number
        obj.save()
        return obj.n
    except Numbers.DoesNotExist:
        obj = Numbers(name=user, n=number)
        obj.save()
        return obj.n


def validate_number(number: int) -> None:
    lower_bound, upper_bound = -100, 100
    if not (lower_bound <= number <= upper_bound):
        raise ValueError(f"number {number} is not in range {(lower_bound, upper_bound)}")


def parse_payload(request: HttpRequest) :
    if not request.body:
        raise ValueError("non-empty body is required")

    try:
        payload = json.loads(request.body)
    except json.JSONDecodeError as err:
        raise ValueError(f"malformed payload: {request.body!r} ({err})") from err

    if isinstance(payload, int):
        validate_number(payload)
    elif payload != "stop":
        raise ValueError(
            f"value {payload!r} is not acceptable: MUST be either int, or 'stop'"
        )

    return payload

class UnprocessableEntityResponse(JsonResponse):
    status_code = 422


@csrf_exempt
@require_http_methods(["POST"])
def view(request: HttpRequest) -> HttpResponse:
    name = get_user(request)
    if not name:
        raise PermissionDenied(json.dumps("header X-USER is not set"))

    try:
        payload = parse_payload(request)
    except ValueError as err:
        response = UnprocessableEntityResponse(str(err), safe=False)
    else:
        if isinstance(payload, int):
            current = add_number(name, payload)
        elif payload == "stop":
            current = get_number(name)
        else:
            current = None

        response = JsonResponse(
            current,
            safe=False,
        )

    set_user_name(response, name)
    return response






