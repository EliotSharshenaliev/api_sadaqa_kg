import stripe
from django.urls import reverse
from djstripe.models import Price, Customer, Subscription
from decimal import Decimal

from djstripe.settings import djstripe_settings


def create_subscription(request):
    # to initialise Stripe.js on the front end
    # context = {
    #     "STRIPE_PUBLIC_KEY": djstripe_settings.STRIPE_PUBLIC_KEY
    # }

    # get the id of the Model instance of djstripe_settings.djstripe_settings.get_subscriber_model()
    # here we have assumed it is the Django User model. It could be a Team, Company model too.
    # note that it needs to have an email field.

    # example of how to insert the SUBSCRIBER_CUSTOMER_KEY: id in the metadata
    # to add customer.subscriber to the newly created/updated customer.
    # metadata = {
    #     f"{djstripe_settings.SUBSCRIBER_CUSTOMER_KEY}": request.user.id
    # }

    try:
        # retreive the Stripe Customer.
        customer = Customer.objects.get(subscriber=request.user)

        # ! Note that Stripe will always create a new Customer Object if customer id not provided
        # ! even if customer_email is provided!
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            customer=customer.id,
            # payment_method_types=["bacs_debit"],  # for bacs_debit
            # payment_intent_data={
            #     "setup_future_usage": "off_session",
                # so that the metadata gets copied to the associated Payment Intent and Charge Objects
                # "metadata": metadata,
            # },
            line_items=[
                {
                    "price_data": {
                        "currency": "usd",
                        # "currency": "gbp",  # for bacs_debit
                        "unit_amount": 2000,
                        "product_data": {
                            "name": "Sample Product Name",
                            "images": ["https://i.imgur.com/EHyR2nP.png"],
                            "description": "Sample Description",
                        },
                    },
                    "quantity": 1,
                },
            ],
            mode="payment",
            success_url="success.com",
            cancel_url="cancel.com",
            # metadata=metadata,
        )

    except Customer.DoesNotExist:
        return False

    # context["CHECKOUT_SESSION_ID"] = session.id
    print(session)
    return True

    # user = request.user
    # user_selected_price = request.POST.get('user_selected_price')
    #
    # price = Price.create(
    #     unit_amount=Decimal(user_selected_price),
    #     currency='kgs',
    #     recurring={"interval": "month"},
    #     product_data={"name": "Authorization Fee"},
    # )
    #
    # customer, created = Customer.get_or_create(subscriber=user)
    # customer.subscribe(items=[{"price": price}])
    #
    # print(customer, created)