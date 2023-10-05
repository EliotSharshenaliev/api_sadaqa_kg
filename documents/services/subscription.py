import stripe
from django.conf import settings
from djstripe.models import Price, Customer

stripe.api_key = settings.STRIPE_SECRET_KEY


def create_or_get_price(amout, interval):
    try:
        amout = amout * 100
        price = Price.objects.get(
            unit_amount=amout,
            recurring={"interval": interval},
            product_id="prod_Ol3u6UlmK5FmVj"
        )
        return price.id
    except Price.DoesNotExist:
        price = stripe.Price.create(
            unit_amount=amout,
            currency="kgs",
            recurring={"interval": interval},
            product="prod_Ol3u6UlmK5FmVj"
        )
        return price.id


def get_or_create_custimer(user):
    try:
        return Customer.objects.get(
            description=user,
            email=user.email
        ), False
    except Customer.DoesNotExist:
        customer = stripe.Customer.create(
            description=user,
            email=user.email
        )
        return customer, True

    except Customer.MultipleObjectsReturned as e:
        return {}, False


def request_payment_page_url(data, user_id):
    try:
        user_selected_price = data["user_selected_price"]
        success_url = data["success_url"]
        cancel_url = data["cancel_url"]
        recurring_interval = data["recurring_interval"]

        price_id = create_or_get_price(
            amout=user_selected_price,
            interval=recurring_interval
        )

        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{'price': price_id, 'quantity': 1, }],
            customer=user_id,
            mode='subscription',
            success_url=success_url + '/success?session_id={CHECKOUT_SESSION_ID}',
            cancel_url=cancel_url + '/cancel',
        )

    except Exception as e:
        return {
            "checkout_url": "",
            "statuc": "error",
        }

    return {
        "checkout_url": checkout_session.url,
        "statuc": "success"
    }
