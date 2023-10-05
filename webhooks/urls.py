from django.urls import path

from webhooks.views import CustomerCreatedWebhookView, SubscriptionCreatedWebhookView

urlpatterns = [
    path(r'customer-created/', CustomerCreatedWebhookView.as_view()),
    path(r'subscription-created/', SubscriptionCreatedWebhookView.as_view()),
]
