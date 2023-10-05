from djstripe.models import Subscription
from rest_framework import generics, status, permissions, views
from rest_framework.response import Response
from documents.serializers.subscription import CreteateSubscriptionSerializer, GetSubscriptionSerializer
from documents.services.subscription import request_payment_page_url


class CreateSubscriptionCheckoutSessionView(generics.CreateAPIView):
    """
        Запрос для авторированных пользователей.
        Если пользователя уже имеется то возвращает ошибку,
        если нет то создается новая подписка на указонную сумму
    """
    serializer_class = CreteateSubscriptionSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        user = request.user

        try:
            Subscription.objects.get(customer_id=user.stripe_id)
            data = {
                "message": "User has subscribed already",
                "checkout_url": "",
                "statuc": "error",
            }
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
        except Subscription.DoesNotExist:
            if serializer.is_valid():
                data = request_payment_page_url(
                    data=serializer.validated_data,
                    user_id=user.stripe_id
                )
                return Response(data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetSubscriptionView(generics.RetrieveAPIView):
    queryset = Subscription.objects.all()
    serializer_class = GetSubscriptionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return Subscription.objects.get(customer_id=self.request.user.stripe_id)
