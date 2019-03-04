from django.contrib import admin
from django.urls import path, include

from ivr_app import views

urlpatterns = [
    path('prueba', views.Payment.as_view(), name="exaple")
]