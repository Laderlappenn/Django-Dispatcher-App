from django.db import models

from django.db import models

class Delivery(models.Model):
    customer_name = models.CharField(max_length=100)
    customer_address = models.CharField(max_length=200)
    delivery_address = models.CharField(max_length=200)
    delivery_status = models.CharField(max_length=20)
    delivery_time = models.DateTimeField(auto_now_add=True)

class Name(models.Model):
    name = models.CharField(max_length=100)

    def str(self):
        return self.name