from django.contrib import admin
from carts.models import Cart

class CartTabAdmin(admin.TabularInline):
    model = Cart
    fields = ['product', 'quantity', 'created_timestamp']
    search_fields = ['product__name', 'created_timestamp']
    readonly_fields = ('created_timestamp',)
    extra = 1

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user_display', 'product', 'quantity', 'created_timestamp']
    list_filter = ['user', 'product__name', 'created_timestamp']

    def user_display(self, obj):
        if obj.user:
            return str(obj.user)
        return 'Anonymous user'