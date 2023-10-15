from djstripe.models import Subscription
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from documents.serializers.subscription import CreteateSubscriptionSerializer, GetSubscriptionSerializer
from stripe_gateway.service import PaymentStripeGateway


class CreateSubscriptionCheckoutSessionView(generics.CreateAPIView):
    """
        Запрос для авторированных пользователей.
        Если пользователя уже имеется то возвращает ошибку,
        если нет то создается новая подписка на указонную сумму
    """
    serializer_class = CreteateSubscriptionSerializer
    permission_classes = [permissions.IsAuthenticated]
    stripe_class = PaymentStripeGateway

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        user = request.user

        if serializer.is_valid():
            data = self.stripe_class.request_payment_page_url(
                data=serializer.validated_data,
                user=user
            )
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetSubscriptionView(generics.RetrieveAPIView):
    queryset = Subscription.objects.all()
    serializer_class = GetSubscriptionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        try:
            return Subscription.objects.get(customer_id=self.request.user.stripe_id)
        except Subscription.DoesNotExist:
            return None

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance:
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        return Response({})


class SubscriptionDeleteView(generics.DestroyAPIView):
    queryset = Subscription.objects.all()
    serializer_class = Subscription
    permission_classes = [permissions.IsAuthenticated]
    stripe_class = PaymentStripeGateway

    def perform_destroy(self, instance):
        self.stripe_class.delete_subscription(instance.id)
        instance.delete()
