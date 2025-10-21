from django.db import models

# Create your models here.

class Patient(models.Model):
    p_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    age = models.IntegerField()
    gender = models.CharField(max_length=10)
    address = models.CharField(max_length=500)
    phno = models.BigIntegerField()
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    repass = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'patient'



