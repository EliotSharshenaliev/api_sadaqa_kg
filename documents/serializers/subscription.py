from rest_framework import serializers
from djstripe.models import Price


class SubscriptionSerializer(serializers.Serializer):
    user_selected_price = serializers.DecimalField(max_digits=10, decimal_places=2)



