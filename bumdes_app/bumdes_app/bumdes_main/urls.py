from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls), # Halaman untuk input data
    path('', include('bumdes_app.urls')), # Menyambungkan ke dashboard BUMDES
]
