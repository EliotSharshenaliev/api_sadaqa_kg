from rest_framework import generics
from rest_framework.response import Response

from documents.service.subscription import request_payment_page_url
from documents.serializers.subscription import SubscriptionSerializer


class CreateCheckoutSessionView(generics.CreateAPIView):
    serializer_class = SubscriptionSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = request_payment_page_url(serializer.validated_data)
        return Response(data=data)


class ConfirmTransactionView(generics.CreateAPIView):
    def create(self, request, *args, **kwargs):
        print(request.data)
        return Response(200)
