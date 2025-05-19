from django.http import JsonResponse
from django.views import View

from carts.mixins import CartMixin
from carts.models import Cart
from goods.models import Products


class CartAddView(CartMixin, View):
    def post(self, request):
        product_id = request.POST.get('product_id')
        product = Products.objects.get(id=product_id)
        cart = self.get_cart(request, product=product)
        if cart:
            cart.quantity += 1
            cart.save()
        else:
            Cart.objects.create(user=request.user if request.user.is_authenticated else None,
                                session_key=request.session.session_key if not request.user.is_authenticated else None,
                                product=product, quantity=1)
        response_data = {
            'message': 'Товар добавлен в корзину',
            'cart_items_html': self.render_cart(request)
        }

        return JsonResponse(response_data)


class CartChangeView(CartMixin, View):
    def post(self, request):
        cart_id = request.POST.get('id')
        cart = self.get_cart(request, cart_id=cart_id)
        cart.quantity = request.POST.get('quantity')
        cart.save()

        response_data = {
            'message': 'Корзина обновлена',
            'cart_items_html': self.render_cart(request),
            'quantity': cart.quantity
        }

        return JsonResponse(response_data)


class CartRemoveView(CartMixin, View):
    def post(self, request):
        cart_id = request.POST.get('id')
        cart = self.get_cart(request, cart_id=cart_id)
        quantity = cart.quantity
        if cart:
            cart.delete()

        response_data = {
            'message': 'Товар удален из корзины',
            'cart_items_html': self.render_cart(request),
            'quantity_deleted': quantity
        }

        return JsonResponse(response_data)