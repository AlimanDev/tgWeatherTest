import json

from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.decorators import api_view


@api_view(['GET'])
def get_weather(request):
    """
    Возвращает погоду города
    """
    if request.method == 'GET':

        return JsonResponse({'result': 'ok'})
