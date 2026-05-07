from django.db import models
from datetime import date

class Product(models.Model):
    name = models.CharField(max_length=200)
    buy_price = models.DecimalField(max_digits=12, decimal_places=2) # Harga Beli (HPP)
    sell_price_mbg = models.DecimalField(max_digits=12, decimal_places=2) # Harga Jual ke MBG
    sell_price_retail = models.DecimalField(max_digits=12, decimal_places=2) # Harga Eceran
    unit = models.CharField(max_length=50, default="Kg")

    def __str__(self):
        return self.name

class Sale(models.Model):
    TYPE_CHOICES = [('MBG', 'Dapur MBG'), ('RETAIL', 'Eceran')]
    date = models.DateField(default=date.today)
    day = models.CharField(max_length=20, blank=True) # Kolom Hari sesuai permintaan Anda
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    sale_type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    
    def total_price(self):
        price = self.product.sell_price_mbg if self.sale_type == 'MBG' else self.product.sell_price_retail
        return price * self.quantity

    def profit(self):
        margin = (self.product.sell_price_mbg if self.sale_type == 'MBG' else self.product.sell_price_retail) - self.product.buy_price
        return margin * self.quantity
