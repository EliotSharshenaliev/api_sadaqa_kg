from django.urls import path

from documents.views import CreateCheckoutSessionView, ConfirmTransactionView

urlpatterns = [
    path(r'create-session-checkout/', CreateCheckoutSessionView.as_view(), name='create-subscription'),
    path(r'confirm-transaction/', ConfirmTransactionView.as_view(), name="confirm-transaction-after-checkout")
]
