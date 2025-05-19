from django.db import models

from users.models import User
from goods.models import Products


class OrderItemQueryset(models.QuerySet):
    def total_price(self):
        return sum(cart.products_price() for cart in self)

    def total_quantity(self):
        if self:
            return sum(cart.quantity for cart in self)
        return 0


class Address_for_delivery(models.Model):
    delivery_city = models.TextField(blank=True, null=True)
    delivery_street_house = models.TextField(blank=True, null=True)
    delivery_apartment = models.TextField(blank=True, null=True)
    delivery_door = models.TextField(blank=True, null=True)
    delivery_floor = models.CharField(blank=True, null=True)

    class Meta:
        db_table = 'address_for_delivery'
        verbose_name = 'address'
        verbose_name_plural = 'addresses'

    def __str__(self):
        return f'City: {self.delivery_city}, street: {self.delivery_street_house}'


class Order(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.SET_DEFAULT, default=None, blank=True, null=True)
    created_timestamp = models.DateTimeField(auto_now_add=True)
    phone_number = models.CharField(max_length=20)
    requires_delivery = models.BooleanField(default=False)
    address_for_delivery = models.ForeignKey(to=Address_for_delivery, on_delete=models.CASCADE, blank=True, null=True)
    payment_on_get = models.BooleanField(default=False)
    payment_type = models.BooleanField(default=False)
    paid = models.BooleanField(default=False)
    status = models.CharField(max_length=50, default='В обработке')

    class Meta:
        db_table = 'order'
        verbose_name = 'order'
        verbose_name_plural = 'orders'
        ordering = ('id',)

    def __str__(self):
        return f'Order № {self.pk} by {self.user.username}'


class OrderItem(models.Model):
    order = models.ForeignKey(to=Order, on_delete=models.CASCADE)
    product = models.ForeignKey(to=Products, on_delete=models.SET_DEFAULT, default=None, null=True, blank=True)
    name = models.CharField(max_length=150)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    quantity = models.PositiveSmallIntegerField(default=0)
    created_timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'order_item'
        verbose_name = 'sold item'
        verbose_name_plural = 'sold items'
        ordering = ('id',)

    objects = OrderItemQueryset.as_manager()

    def product_price(self):
        return round((self.price * self.quantity),2)

    def __str__(self):
        return f"Item {self.name} | Order № {self.order.pk}"
