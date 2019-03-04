from django.contrib.auth.models import User, Group
from rest_framework import serializers

from ivr_app.models import Card


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = '__all__'
