from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('', home_view ),
    path('whois_ip', whois_ip, name='whois_ip'),
]