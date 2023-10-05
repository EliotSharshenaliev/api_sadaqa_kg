from django.urls import path

from documents.views import (
    CreateSubscriptionCheckoutSessionView,
    GetSubscriptionView
)

urlpatterns = [
    path(
        r'create-subscription/',
        CreateSubscriptionCheckoutSessionView.as_view(),
        name='create-subscription'
    ),
    path(
        r'get-subscription/',
        GetSubscriptionView.as_view(),
        name='get-subscription'
    )
]
