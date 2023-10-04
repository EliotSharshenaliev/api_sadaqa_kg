from djstripe.enums import PlanInterval
from rest_framework import serializers


class SubscriptionSerializer(serializers.Serializer):
    user_selected_price = serializers.IntegerField(
        required=True
    )
    success_url = serializers.CharField(
        required=True,
        max_length=255
    )
    cancel_url = serializers.CharField(
        required=True,
        max_length=255
    )
    recurring_interval = serializers.ChoiceField(choices=PlanInterval.choices)
