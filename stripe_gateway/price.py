import logging

import stripe
from django.conf import settings
from djstripe.models import Price

stripe.api_key = settings.STRIPE_SECRET_KEY

logger = logging.getLogger(__name__)


class PriceStripeGateway:
    @classmethod
    def create_or_get_price(cls, amount, interval):
        try:
            amount = amount * 100
            price = Price.objects.get(
                unit_amount=amount,
                recurring={"interval": interval},
                product_id="prod_Omc0Igw8EeFM1g"
            )
            return price.id
        except Price.DoesNotExist:
            price = stripe.Price.create(
                unit_amount=amount,
                currency="kgs",
                recurring={"interval": interval},
                product="prod_Omc0Igw8EeFM1g"
            )
            Price.sync_from_stripe_data(price)
            return price.id
