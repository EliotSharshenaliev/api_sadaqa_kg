import logging

import stripe
from django.conf import settings
from djstripe.models import Subscription

stripe.api_key = settings.STRIPE_SECRET_KEY

logger = logging.getLogger(__name__)


class SubscriptionStripeGateway:
    @classmethod
    def delete_subscription(cls, subs_id):
        response = stripe.Subscription.delete(
            subs_id,
        )
        Subscription.sync_from_stripe_data(response)
