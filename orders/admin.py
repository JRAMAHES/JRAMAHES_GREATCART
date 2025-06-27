from django.contrib import admin
from .models import Order, OrderProduct, Payment

class OrderProductInline(admin.TabularInline):
    model = OrderProduct
    readonly_fields = ('product', 'quantity', 'product_price', 'ordered', 'user', 'payment')
    extra = 0

class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'full_name', 'phone', 'email', 'city', 'order_total', 'tax','status','is_ordered', 'created_at')
    search_fields = ('order_number', 'first_name', 'last_name', 'phone', 'email')
    list_filter = ('status', 'is_ordered', 'created_at')
    inlines = [OrderProductInline]

class OrderProductAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity', 'product_price', 'ordered', 'user', 'payment')
    search_fields = ('order__order_number', 'product__product_name', 'user__username')
    list_filter = ('ordered', 'created_at')

admin.site.register(Order, OrderAdmin)
admin.site.register(OrderProduct, OrderProductAdmin)
admin.site.register(Payment)



