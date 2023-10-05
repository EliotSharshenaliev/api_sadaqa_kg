from django.urls import path

from webhooks.views import CustomerWebhookView, SubscriptionWebhookView

urlpatterns = [
    path(r'customer/', CustomerWebhookView.as_view()),
    path(r'subscription/', SubscriptionWebhookView.as_view()),
]
