from rest_framework import serializers
from djstripe.models import BalanceTransaction


class BalanceTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = BalanceTransaction
        fields = "__all__"
