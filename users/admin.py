from django.contrib import admin
from users.models import User
from carts.admin import CartTabAdmin
from orders.admin import OrderTabAdmin

# Register your models here.

# admin.site.register(User)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email']
    search_fields = ['username', 'email', 'first_name', 'last_name']

    inlines = [CartTabAdmin, OrderTabAdmin]