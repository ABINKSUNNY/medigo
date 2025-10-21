from django.db import models
from deliveryagent.models import Deliveryagent
from patient.models import Patient
from pharmacy.models import Pharmacy
from cart.models import Purchase

# Create your models here.
# class Delivery(models.Model):
#     de_id = models.AutoField(primary_key=True)
#     status = models.CharField(max_length=30, blank=True, null=True)
#     date = models.DateField(blank=True, null=True)
#     time = models.TimeField(blank=True, null=True)
#     # da_id = models.IntegerField(blank=True, null=True)
#     deliveryagent= models.ForeignKey(Deliveryagent, to_field='da_id', db_column='da_id', on_delete=models.CASCADE,default=1)
# #
#     # pu_id = models.IntegerField(blank=True, null=True)
#     purchase = models.ForeignKey(Purchase, to_field='pu_id', db_column='pu_id', on_delete=models.CASCADE,default=1)
#
# #
#     class Meta:
#         managed = False
#         db_table = 'delivery'



class Delivery(models.Model):
    de_id = models.AutoField(primary_key=True)
    status = models.CharField(max_length=30)
    date = models.DateField()
    time = models.TimeField()
    # da_id = models.IntegerField()
    # pu_id = models.IntegerField()
    deliveryagent = models.ForeignKey(Deliveryagent, to_field='da_id', db_column='da_id', on_delete=models.CASCADE, default=1)
    purchase = models.ForeignKey(Purchase, to_field='pu_id', db_column='pu_id', on_delete=models.CASCADE, default=1)
    pha_id = models.ForeignKey(Pharmacy,to_field='pha_id', db_column='pha_id', on_delete=models.CASCADE)
    p_id = models.ForeignKey(Patient,to_field='p_id', db_column='p_id', on_delete=models.CASCADE)

    class Meta:
        managed = False
        db_table = 'delivery'




