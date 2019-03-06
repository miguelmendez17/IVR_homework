from django.urls import path

from ivr_app import views

urlpatterns = [
    path('', views.PaymentView.as_view())
]
