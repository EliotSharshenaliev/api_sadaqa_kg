import stripe
from django.conf import settings
from django.urls import reverse
from djstripe.models import Price, Customer, Subscription, Product
from decimal import Decimal


def request_payment_page_url(request):
    user_selected_price = request.data.get("user_selected_price", False)
    user = request.user

    customer = stripe.Customer.create(
        description=user,
        email=user.email
    )
    djstripe_customer = Customer.sync_from_stripe_data(customer)

    product = stripe.Product.create(name="Authenication Fee")

    plan = stripe.Plan.create(
        amount=Decimal(user_selected_price),
        currency="KGS",
        interval="month",
        product=product.id,
    )

    # create subscription
    subscription = stripe.Subscription.create(
        customer=customer.id,
        items=[
            {
                'plan': plan.id,
            },
        ],
        expand=['latest_invoice.payment_intent'],
    )
    djstripe_subscription = Subscription.sync_from_stripe_data(subscription)

    if not user_selected_price:
        return {
            "type_response": "error",
            "payment_url": "",
            "timeout": 0
        }
    return {
        "data": subscription,
        "type_response": "success",
        "payment_url": "google.com",
        "timeout": 150
    }
