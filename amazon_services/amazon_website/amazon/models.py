from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.utils import timezone
import random
# Files that interact with the database. PostgreSQL
# Create your models here.


class Commodity(models.Model):
    commodity_id = models.AutoField(primary_key=True)
    description = models.TextField()
    count = models.IntegerField()

class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    description = models.TextField()

class Warehouse(models.Model):
    warehouse_id = models.AutoField(primary_key=True)
    location_x = models.IntegerField()
    location_y = models.IntegerField()

class Package(models.Model):
    package_id = models.AutoField(primary_key = True)
    destination_x = models.IntegerField()
    destination_y = models.IntegerField()
    user_id = models.IntegerField(null=True)
    status = models.TextField(default="purchase")
    truck_id = models.IntegerField(null=True, default=0)
    
class Order(models.Model):
    order_id = models.AutoField(primary_key = True)
    product = models.ForeignKey(Product, on_delete = models.CASCADE, null=True)
    quantity = models.IntegerField()
    warehouse = models.ForeignKey(Warehouse, on_delete = models.CASCADE)
    package = models.ForeignKey(Package, on_delete = models.CASCADE)
    
class Request(models.Model):
    request_id = models.AutoField(primary_key = True)
    type = models.TextField(default="purchase")
    status = models.TextField(default="open")
    pk_id = models.ForeignKey(Package, on_delete = models.CASCADE, db_column="pk_id")
    

'''

class Cart(models.Model):
    product = models.ForeignKey(Commodity, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

class Shipment(models.Model):
    shipment_id = models.AutoField(primary_key = True)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
    destination_x = models.IntegerField()
    destination_y = models.IntegerField()
    status = models.CharField(max_length = 200, null=True, default="ordering")
    create_time = models.DateTimeField(default=timezone.now)
    truck_id = models.IntegerField(null=True)
'''