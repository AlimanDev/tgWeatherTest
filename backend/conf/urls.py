from django.contrib import admin
from django.urls import path

from weather.views import WeatherAPI

urlpatterns = [
    path('admin/', admin.site.urls),
    path('weather/', WeatherAPI.as_view(), name='weather')
]
