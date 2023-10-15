import logging

import stripe
from django.conf import settings
from djstripe.models import Session

from stripe_gateway.customer import CustomerStripeGateway
from stripe_gateway.price import PriceStripeGateway
from stripe_gateway.subscription import SubscriptionStripeGateway

stripe.api_key = settings.STRIPE_SECRET_KEY

logger = logging.getLogger(__name__)


class PaymentStripeGateway(CustomerStripeGateway, SubscriptionStripeGateway, PriceStripeGateway):

    def request_payment_page_url(self, data, user):
        try:
            user_selected_price = data["user_selected_price"]
            success_url = data["success_url"]
            cancel_url = data["cancel_url"]
            recurring_interval = data["recurring_interval"]

            price_id = self.create_or_get_price(
                amount=user_selected_price,
                interval=recurring_interval
            )

            checkout_session = stripe.checkout.Session.create(
                customer=user.stripe_id,
                payment_method_types=['card'],
                line_items=[{'price': price_id, 'quantity': 1, }],
                mode='subscription',
                success_url=success_url + '/success?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=cancel_url + '/cancel',
            )
            Session.sync_from_stripe_data(checkout_session)

        except Exception as e:
            logger.error("Error: %s" % e.args)
            return {
                "checkout_url": "",
                "statuc": "error",
            }

        return {
            "checkout_url": checkout_session.url,
            "statuc": "success"
        }
