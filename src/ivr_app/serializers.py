from rest_framework import serializers

from ivr_app.models import Card


class CardSerializer(serializers.ModelSerializer):
    """
    This is the card serializer. We can use '__all__' in the fields. But in this
    case, we would have to take the date into account. And this should be generated automatically
    """
    class Meta:
        model = Card
        fields = ('cc_num', 'cvc', 'exp_month', 'exp_year', 'amount', 'description')
