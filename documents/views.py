from rest_framework import generics
from rest_framework.response import Response

from documents.service.subscription import request_payment_page_url
from documents.serializers.subscription import SubscriptionSerializer


class CreateSubscriptionView(generics.CreateAPIView):
    serializer_class = SubscriptionSerializer


    def create(self, request, *args, **kwargs):
        data = request_payment_page_url(request)
        return Response(data=data)
