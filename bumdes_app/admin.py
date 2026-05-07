from django.contrib import admin
from .models import Product, Sale

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'buy_price', 'sell_price_mbg', 'unit')

@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ('date', 'day', 'product', 'quantity', 'sale_type', 'total_price', 'profit')
    list_filter = ('sale_type', 'date')
