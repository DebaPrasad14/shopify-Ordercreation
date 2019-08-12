from django.contrib import admin
from .models import Order


# Register your models here.
class OrderAdmin(admin.ModelAdmin):
    list_display= ['orderno', 'customer_name','customer_phone','customer_email','total_price','subtotal_price']

admin.site.register(Order,OrderAdmin)
