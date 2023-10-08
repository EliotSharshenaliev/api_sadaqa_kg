import logging

import stripe
from django.conf import settings
from djstripe.models import Price, Subscription, Session

stripe.api_key = settings.STRIPE_SECRET_KEY

logger = logging.getLogger(__name__)


class BaseGateway:
    __instances = {}

    def __new__(cls, *args, **kwargs):
        if cls not in cls.__instances:
            cls.__instances[cls] = super(BaseGateway, cls).__new__(cls)
        return cls.__instances[cls]


class StripeGateway(BaseGateway):

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

    @classmethod
    def delete_subscription(cls, subs_id):
        response = stripe.Subscription.delete(
            subs_id,
        )
        Subscription.sync_from_stripe_data(response)
