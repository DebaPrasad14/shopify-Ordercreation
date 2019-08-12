from django.db import models


class Order(models.Model):
    orderno     = models.IntegerField()
    customer_name   = models.CharField(max_length=64)
    customer_phone = models.CharField(max_length=15)
    customer_email = models.EmailField()
    total_price = models.FloatField()
    subtotal_price = models.FloatField()

    def get_absolute_url(self):
        return u"/app/orders/"
