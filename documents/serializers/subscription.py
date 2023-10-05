from djstripe.enums import PlanInterval
from djstripe.models import Subscription
from rest_framework import serializers


class CreteateSubscriptionSerializer(serializers.Serializer):
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


class GetSubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = "__all__"
