from djstripe.models import BalanceTransaction
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from documents.serializers.balance import BalanceTransactionSerializer
from documents.serializers.subscription import SubscriptionSerializer
from documents.services.subscription import request_payment_page_url


class SubscriptionCheckoutSessionView(generics.CreateAPIView):
    """
        Запрос для авторированных пользователей.
        Если пользователя уже имеется подписка то обновляется на нового,
        если нет то создается новая подписка на указонную сумму
    """
    serializer_class = SubscriptionSerializer
    # permissions_classes = (permissions.IsAuthenticated, )
    permission_classes = (permissions.IsAuthenticated, )

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        # user = request.user
        if serializer.is_valid():
            data = request_payment_page_url(data=serializer.validated_data)
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
