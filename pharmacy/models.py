from django.db import models

# Create your models here.


class Pharmacy(models.Model):
    pha_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=500)
    email = models.CharField(max_length=50)
    contact = models.BigIntegerField()
    licence = models.CharField(max_length=200)
    place = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    repass = models.CharField(max_length=50)
    status = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pharmacy'


