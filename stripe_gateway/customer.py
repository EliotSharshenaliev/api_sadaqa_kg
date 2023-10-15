import logging

import stripe
from django.conf import settings
from django.contrib.auth.models import User
from djstripe.models import Customer

logger = logging.getLogger(__name__)


class CustomerStripeGateway:
    def check_user_in_stripe(self) -> User | None:
        try:
            if response := stripe.Customer.search(
                    query=f"name:'{self.firstname}' AND metadata['user_id']:'{self.id}'"
            ):
                logger.error(response)
                self.stripe_user = True
        except Exception or None as e:
            logger.error(e.args)
            return None

    def create_user_stripe(self) -> bool:
        try:
            stripe.api_key = settings.STRIPE_SECRET_KEY
            description = self.get_full_name()
            customer = stripe.Customer.create(
                description=description,
                name=self.firstname,
                email=self.email,
                phone=self.phone,
                metadata={
                    'user_id': self.id,
                },
            )
            self.stripe_id = customer.id
            self.stripe_user = True
            Customer.sync_from_stripe_data(customer)
            return customer.id
        except Exception as e:
            logger.error("Error: %s " % e.args)
            self.stripe_user = False
            return False

    def delete_stripe_customer(self) -> bool:
        try:
            stripe.api_key = settings.STRIPE_SECRET_KEY
            customer = stripe.Customer.delete(self.stripe_id)
        except Exception as e:
            logger.info(e)

        return True

    def update_stripe_customer(self) -> bool:
        try:
            stripe.api_key = settings.STRIPE_SECRET_KEY
            description = self.get_full_name()
            customer: dict = stripe.Customer.modify(
                self.stripe_id,
                description=description,
                name=self.firstname,
                email=self.email,
                phone=self.phone,
            )
            Customer.sync_from_stripe_data(customer)
            return customer.get("id", False)
        except Exception as e:
            logger.error("Error: %s " % e.args)
            return False
