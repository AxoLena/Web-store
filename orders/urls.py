from django.urls import path

from orders.webhooks import stripe_webhook
from orders import views

app_name = 'orders'

urlpatterns = [
    path('create-order/', views.CreateOrderView.as_view(), name='create_order'),
    path('webhook-stripe/', stripe_webhook, name='webhook-stripe')
]
