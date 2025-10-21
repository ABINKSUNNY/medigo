from django.db import models
from patient.models import Patient
from pharmacy.models import Pharmacy

# adjust if your Patient model is elsewhere

class Product(models.Model):
    name = models.CharField(max_length=255)
    brand = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    # pha_id = models.IntegerField()
    pharmacy = models.ForeignKey(Pharmacy, to_field='pha_id', db_column='pha_id', on_delete=models.CASCADE,default=1)

    def __str__(self):
        return self.name

class CartItem(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, null=True)
    session_key = models.CharField(max_length=40, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    prescription_image = models.ImageField(upload_to='prescriptions/', blank=True, null=True)

    def get_total_price(self):
        return self.product.price * self.quantity

# class Purchase(models.Model):
#     pu_id = models.BigAutoField(primary_key=True)
#     patient = models.ForeignKey(Patient, on_delete=models.SET_NULL, null=True)
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     quantity = models.PositiveIntegerField()
#     price = models.DecimalField(max_digits=8, decimal_places=2)
#     payment_id = models.CharField(max_length=100)
#     order_id = models.CharField(max_length=100,unique=True)
#     total_amount = models.DecimalField(max_digits=10, decimal_places=2)
#     timestamp = models.DateTimeField(auto_now_add=True)
#     # pha_id = models.IntegerField(blank=True, null=True)
#     pharmacy = models.ForeignKey(Pharmacy, to_field='pha_id', db_column='pha_id', on_delete=models.CASCADE, default=1)
#     status = models.CharField(max_length=20, blank=True, null=True)
#

class Purchase(models.Model):
    pu_id = models.BigAutoField(primary_key=True)
    patient = models.ForeignKey(Patient, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.CharField(max_length=255)  # Stores "Name xQty, Name xQty"
    payment_id = models.CharField(max_length=100)
    order_id = models.CharField(max_length=100, unique=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    pharmacy = models.ForeignKey(Pharmacy, to_field='pha_id', db_column='pha_id', on_delete=models.CASCADE, default=1)
    status = models.CharField(max_length=20, blank=True, null=True)
    product_ids = models.TextField(blank=True, null=True)
    prescription_image = models.ImageField(upload_to='prescriptions/', blank=True, null=True)
