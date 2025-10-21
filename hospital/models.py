# models.py in the hospital app
from django.db import models

# class Hospital(models.Model):
#     h_id = models.AutoField(primary_key=True)
#     hospitalname = models.CharField(max_length=30)
#     speciality = models.CharField(max_length=30)
#     department = models.CharField(max_length=500)
#     contact = models.IntegerField()
#     email = models.CharField(max_length=30)
#     address = models.CharField(max_length=50)
#     status = models.CharField(max_length=20)
#     password = models.CharField(max_length=50)
#     repass = models.CharField(max_length=50)
#
#     class Meta:
#         managed = False
#         db_table = 'hospital'
class Hospital(models.Model):
    h_id = models.AutoField(primary_key=True)
    hospitalname = models.CharField(max_length=50)
    speciality = models.CharField(max_length=30)
    contact = models.BigIntegerField()
    email = models.CharField(max_length=50)
    address = models.CharField(max_length=500)
    status = models.CharField(max_length=20)
    password = models.CharField(max_length=50)
    repass = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'hospital'

