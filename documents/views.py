from djstripe.models import BalanceTransaction
from rest_framework import generics, permissions
from rest_framework.response import Response

from documents.serializers.balance import BalanceTransactionSerializer
from documents.service.subscription import request_payment_page_url
from documents.serializers.subscription import SubscriptionSerializer


class CreateCheckoutSessionView(generics.CreateAPIView):
    serializer_class = SubscriptionSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = request_payment_page_url(
            data=serializer.validated_data,
            user=request.user
        )
        return Response(data=data)


class ConfirmTransactionView(generics.CreateAPIView):
    def create(self, request, *args, **kwargs):
        print(request.data)
        return Response(200)


class BalanceTransactionList(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
    queryset = (
        BalanceTransaction.objects.all()
    )
    serializer_class = BalanceTransactionSerializer
