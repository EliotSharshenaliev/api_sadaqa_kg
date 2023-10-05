from djstripe.models import Customer, Subscription
from rest_framework import generics
from rest_framework.response import Response


class CustomerWebhookView(generics.CreateAPIView):
    def create(self, request, *args, **kwargs):
        try:
            customer_data = request.data["data"]["object"]
            Customer.sync_from_stripe_data(customer_data)
        except KeyError or Exception:
            return Response(400)

        return Response(200)


class SubscriptionWebhookView(generics.CreateAPIView):
    def create(self, request, *args, **kwargs):
        try:
            subscription_data = request.data["data"]["object"]
            Subscription.sync_from_stripe_data(subscription_data)
        except KeyError or Exception:
            return Response(400)

        return Response(200)
