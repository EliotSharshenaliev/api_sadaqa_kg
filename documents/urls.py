from django.urls import path

from documents.views import CreateSubscriptionView

urlpatterns = [
    path(r'create-payment/', CreateSubscriptionView.as_view({'post': 'create'}), name='create-subscription'),
]
