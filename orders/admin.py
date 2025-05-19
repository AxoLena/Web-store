from django.contrib import admin

from orders.models import Order, OrderItem

class OrderItemTabAdmin(admin.TabularInline):
    model = OrderItem
    fields = ('name', 'price', 'quantity')
    search_fields = ('name',)
    extra = 0

class OrderTabAdmin(admin.TabularInline):
    model = Order
    fields = ['requires_delivery', 'status', 'payment_on_get', 'created_timestamp']
    readonly_fields = ['created_timestamp']
    extra = 0

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'name', 'price', 'quantity')
    search_fields = ('order', 'product', 'name')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'requires_delivery', 'status', 'payment_on_get', 'created_timestamp']
    search_fields = ['id']
    readonly_fields = ['created_timestamp']
    list_filter = ['status', 'created_timestamp']
    inlines = (OrderItemTabAdmin,)

