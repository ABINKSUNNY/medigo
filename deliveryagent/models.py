from django.db import models


class Deliveryagent(models.Model):
    da_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=500)
    age = models.IntegerField()
    phno = models.BigIntegerField()
    email = models.CharField(max_length=100)
    gender = models.CharField(max_length=20)
    license = models.CharField(max_length=200)
    pha_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'deliveryagent'
