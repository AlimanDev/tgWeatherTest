from django.contrib import admin
from django.urls import path

from apps.weather.views import get_weather

urlpatterns = [
    path('admin/', admin.site.urls),
    path('weather/', get_weather)
]
