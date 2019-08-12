from django.urls import path
from myApp.views import WebhookView, ContactUpdate, OrderDetail

urlpatterns = [
    path('shopify/', WebhookView.as_view(), name='shopify'),
    path('orders/', OrderDetail.as_view(), name='orders'),
    path('update/<int:pk>', ContactUpdate.as_view(), name='order_update'),
]
