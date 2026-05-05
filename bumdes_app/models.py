from django.db import models
from django.db.models import Sum
from datetime import date, timedelta

# Model untuk Pengaturan BUMDES (image_3.png -> "BUMDES PUTRA MANDALA MANDALAWANGI")
class BumdesSettings(models.Model):
    name = models.CharField(max_length=200, default="BUMDES PUTRA MANDALA MANDALAWANGI")
    address = models.TextField(default="Desa Mandalawangi Kec Leles kab Cianjur Jawa Barat Indonesia")
    logo = models.ImageField(upload_to='bumdes_logos/', blank=True, null=True)

    def __str__(self):
        return self.name

# Model untuk Produk (image_3.png & image_0.png "Nama Produk")
class Product(models.Model):
    UNIT_CHOICES = [
        ('KG', 'Kilogram'),
        ('TR','Tray (Telur)'),
        ('KR','Karung (Beras/Sembako)'),
        ('PCS','Pcs'),
        ('IKT','Ikat')
    ]
    
    name = models.CharField(max_length=200) # Contoh: Daging Ayam, Beras Cianjur
    # image_3.png -> "input data penjualan margin keuntungan harga beli dan harga jual"
    buy_price = models.DecimalField(max_digits=12, decimal_places=2) # Harga Beli/HPP
    sell_price = models.DecimalField(max_digits=12, decimal_places=2) # Harga Jual (default)
    unit = models.CharField(max_length=3, choices=UNIT_CHOICES, default='KG')

    def margin(self):
        return self.sell_price - self.buy_price

    def __str__(self):
        return self.name

# Model untuk Penjualan (Pemasokan) (Opsi Dapur MBG & Eceran di image_3.png & 15983485149783029553.jpeg)
class Sale(models.Model):
    INVOICE_TEMPLATES = [
        ('MBG', 'Template Dapur MBG (Detail)'),
        ('ECR', 'Template Eceran (Sederhana)')
    ]
    
    # image_3.png -> "semua bisa di edit nama tgl di sesuaikan"
    date = models.DateField(default=date.today) # Hari dan Tanggal
    customer_name = models.CharField(max_length=200, default="Dapur MBG - Cianjur") # Nama di Invoice
    
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    # image_3.png -> "margin keuntungan...harga jual"
    # Kita kunci harga jual saat transaksi, karena harga produk di database bisa berubah
    actual_sell_price = models.DecimalField(max_digits=12, decimal_places=2, null=True)

    # image_3.png -> "Invoice . Semua bisa di edit" & "kustomisasi"
    invoice_number = models.CharField(max_length=20, blank=True, unique=True)
    template_type = models.CharField(max_length=3, choices=INVOICE_TEMPLATES, default='MBG')

    def total_amount(self):
        return self.actual_sell_price * self.quantity

    # image_3.png -> "profit total...margin keuntungan"
    def profit(self):
        return (self.actual_sell_price - self.product.buy_price) * self.quantity

    def save(self, *args, **kwargs):
        # Generate nomor invoice otomatis jika belum ada
        if not self.invoice_number:
            prefix = "INV-MBG-" if self.template_type == 'MBG' else "INV-ECR-"
            # Nomor sederhana berdasarkan tanggal dan ID produk
            self.invoice_number = prefix + date.today().strftime("%Y%m%d") + "-" + str(self.product.id) # Sederhana
        super(Sale, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.invoice_number} - {self.customer_name}"

# Model untuk Arus Kas (Uang Masuk/Keluar) (image_0.png "Saldo Akhir", "Debet", "Kredit")
class Cashflow(models.Model):
    DATE_TYPE_CHOICES = (
        ('DEBET', 'Uang Masuk'),
        ('KREDIT', 'Uang Keluar'),
    )
    date = models.DateField(default=date.today)
    flow_type = models.CharField(max_length=6, choices=DATE_TYPE_CHOICES)
    description = models.CharField(max_length=200) # Misal: "Penjualan INV-MBG-..." atau "Beli Beras"
    # image_0.png -> total saldo harus dihitung dinamis
    amount = models.DecimalField(max_digits=12, decimal_places=2)
