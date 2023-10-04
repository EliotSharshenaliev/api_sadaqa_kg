from django.urls import path
from rest_framework.routers import DefaultRouter

from documents.views import CreateCheckoutSessionView, ConfirmTransactionView, BalanceTransactionList

urlpatterns = [
    path(r'create-session-checkout/', CreateCheckoutSessionView.as_view(), name='create-subscription'),
]
