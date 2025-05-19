import uuid
import stripe
from yookassa import Configuration, Payment
from currency_converter import CurrencyConverter

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.db import transaction
from django.forms import ValidationError
from django.contrib import messages
from django.urls import reverse_lazy, reverse
from django.views.generic import FormView

from orders.forms import CreateOrderForm
from orders.models import Order, OrderItem
from carts.models import Cart
from store.settings import STRIPE_SECRET_KEY, STRIPE_API_VERSION, YOOKASSA_SHOP_ID, YOOKASSA_SECRET_KEY

stripe.api_key = STRIPE_SECRET_KEY
stripe.api_version = STRIPE_API_VERSION

Configuration.account_id = YOOKASSA_SHOP_ID
Configuration.secret_key = YOOKASSA_SECRET_KEY


class CreateOrderView(LoginRequiredMixin, FormView):
    template_name = 'orders/create_order.html'
    form_class = CreateOrderForm
    success_url = reverse_lazy('users:profile')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Home - Оформление заказа'
        context['order'] = True
        return context

    def get_initial(self):
        initial = super().get_initial()
        initial['first_name'] = self.request.user.first_name
        initial['last_name'] = self.request.user.last_name
        initial['email'] = self.request.user.email
        initial['phone_number'] = self.request.user.phone_number
        return initial

    def form_valid(self, form):
        try:
            with transaction.atomic():
                user = self.request.user
                cart_items = Cart.objects.filter(user=user)
                payment_type = self.request.POST.get('payment_type')
                if cart_items.exists():
                    order = Order.objects.create(user=user, phone_number=form.cleaned_data['phone_number'],
                                                 requires_delivery=form.cleaned_data['requires_delivery'],
                                                 delivery_city=form.cleaned_data['delivery_city'],
                                                 delivery_street_house=form.cleaned_data['delivery_street_house'],
                                                 delivery_apartment=form.cleaned_data['delivery_apartment'],
                                                 delivery_door=form.cleaned_data['delivery_door'],
                                                 delivery_floor=form.cleaned_data['delivery_floor'],
                                                 payment_on_get=form.cleaned_data['payment_on_get'],
                                                 payment_type=form.cleaned_data['payment_type'],)
                    for cart_item in cart_items:
                        product = cart_item.product
                        name = cart_item.product.name
                        price = cart_item.product.discount_price()
                        quantity = cart_item.quantity

                        if product.quantity < quantity:
                            raise ValidationError(
                                f'Недостаточное количество товара на складе {name}, в наличии {product.quantity}')

                        OrderItem.objects.create(order=order, product=product, name=name, price=price,
                                                 quantity=quantity)
                        product.quantity -= quantity
                        product.save()
                    if payment_type == '0' or payment_type == '1':
                        match payment_type:
                            case '0':
                                session_data = {
                                    'mode': 'payment',
                                    'success_url': self.request.build_absolute_uri(reverse('users:profile')),
                                    'cancel_url': self.request.build_absolute_uri(reverse('orders:create_order')),
                                    'line_items': [],
                                }
                                for cart_item in cart_items:
                                    c = CurrencyConverter()
                                    session_data['line_items'].append({
                                        'price_data': {
                                            'unit_amount': int(c.convert(float(cart_item.product.discount_price()), 'RUB', 'USD') * 100),
                                            'currency': 'usd',
                                            'product_data': {
                                                'name': cart_item.product.name
                                            }
                                        },
                                        'quantity': cart_item.quantity,
                                    })
                                session_data['client_reference_id'] = order.id
                                session = stripe.checkout.Session.create(**session_data)
                                return redirect(session.url, code=303)

                            case '1':
                                idempotence_key = uuid.uuid4()
                                total_price = int(cart_items.total_price())
                                currency = 'RUB'
                                description = 'Товары в корзине'
                                payment = Payment.create({
                                    "amount": {
                                        "value": str(total_price),
                                        "currency": currency
                                    },
                                    "confirmation": {
                                        "type": "redirect",
                                        "return_url": self.request.build_absolute_uri(reverse('users:profile')),
                                    },
                                    "capture": True,
                                    "test": True,
                                    "description": description,
                                }, idempotence_key)
                                payment['client_reference_id'] = order.id
                                cart_items.delete()
                                confirmation_url = payment.confirmation.confirmation_url
                                return redirect(confirmation_url)

                    cart_items.delete()
                    messages.success(self.request, 'Заказ оформлен')
                    return redirect('users:profile')
        except ValidationError as e:
            messages.success(self.request, str(e))
            return render(self.request, 'orders/create_order.html', self.get_context_data())

    def form_invalid(self, form):
        messages.error(self.request, 'Заказ не оформлен. Произошла ошибка')
        return redirect('orders:create_order')
