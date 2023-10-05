from django.urls import path

from documents.views import SubscriptionCheckoutSessionView


urlpatterns = [
    path(r'subscription-session-checkout/', SubscriptionCheckoutSessionView.as_view(), name='subscription'),
]
