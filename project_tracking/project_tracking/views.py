import datetime

# from django.views.generic import View
from django.http import JsonResponse


def main_page(request):
    return JsonResponse(
        {'status': 'OK',
         'message': 'test response',
         'datetime': datetime.datetime.now().strftime("%H:%M:%S %d.%m.%Y")})
