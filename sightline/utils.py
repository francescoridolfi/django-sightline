from django.http.request import HttpRequest
import datetime

def get_ip_addr(request: HttpRequest):

    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')

    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def get_user_agent(request: HttpRequest):

    return request.headers.get("User-Agent", "")

def timestamp_to_str(date: datetime.datetime) -> str:
    return date.strftime("%d/%m/%Y %H:%M:%S")

def time_compraration(
        timestamp: datetime.datetime,
        reference:datetime.datetime,
        interval: int):
    return timestamp >= reference + datetime.timedelta(seconds=interval)