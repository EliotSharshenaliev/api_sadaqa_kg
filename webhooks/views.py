from djstripe.models import Customer, Subscription
from rest_framework import generics, views
from rest_framework.response import Response


class CustomerCreatedWebhookView(views.APIView):

    @classmethod
    def post(cls, request, *args, **kwargs):
        try:
            event = request.data
            if event['type'] == 'customer.created':
                customer_data = event["data"]["object"]
                Customer.sync_from_stripe_data(customer_data)
        except KeyError or Exception:
            return Response(400)

        return Response(200)


class SubscriptionCreatedWebhookView(views.APIView):
    @classmethod
    def post(cls, request, *args, **kwargs):
        try:
            event = request.data
            if event['type'] == 'customer.subscription.created':
                customer_data = event["data"]["object"]
                Subscription.sync_from_stripe_data(customer_data)
        except KeyError or Exception:
            return Response(400)

        return Response(200)
