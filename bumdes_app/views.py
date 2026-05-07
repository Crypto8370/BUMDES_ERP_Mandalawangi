from django.shortcuts import render
from .models import Sale
from django.db.models import Sum

def dashboard(request):
    # Mengambil data untuk Rekapan Profit Mingguan sesuai blueprint Anda
    total_profit = Sale.objects.aggregate(Sum('profit'))['profit__sum'] or 0
    sales = Sale.objects.all().order_by('-date')
    
    context = {
        'total_profit': total_profit,
        'sales': sales,
        'bank_balance': 11029.00 # Data dari laporan BRI Anda
    }
    return render(request, 'dashboard.html', context)
