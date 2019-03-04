from django.shortcuts import render

# Create your views here.
from requests import Response
from rest_framework import status
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated

from ivr_app.models import Card
from ivr_app.serializers import PaymentSerializer


class Payment(RetrieveAPIView):
    # Display reminder details
    queryset = Card.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        payment = super(Payment, self).get_queryset()
        payment = payment.filter(user="fadsf")
        return payment

    def post(self, request):
        serializer = PaymentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            article_saved = serializer.save()
        return "hoasdf"