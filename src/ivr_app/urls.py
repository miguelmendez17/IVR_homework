from django.urls import path

from ivr_app import views

urlpatterns = [
    path('payment/', views.PaymentView.as_view())
]
