# doctor/models.py
from django.db import models
from hospital.models import Hospital  # Import Hospital model

# doctor/models.py
from django.db import models
# from hospital.models import Hospital

# class Doctor(models.Model):
#     doc_id = models.AutoField(primary_key=True)
#     doc_name = models.CharField(max_length=30)
#     doc_age = models.IntegerField()
#     gender = models.CharField(max_length=10)
#     specialization = models.CharField(max_length=30)
#     qualification = models.CharField(max_length=30)
#     consulting_hours = models.CharField(max_length=20)
#     department = models.CharField(max_length=30)
#     status = models.CharField(max_length=20)
#     contact = models.IntegerField()
#
#     # ForeignKey linking the doctor to the hospital
#     hospital = models.ForeignKey(Hospital, to_field='h_id', db_column='h_id', on_delete=models.CASCADE)
#
#     class Meta:
#         managed = False  # Assuming you're working with an existing database table
#         db_table = 'doctor'  # Make sure this matches your actual table name


class Doctor(models.Model):
    doc_id = models.AutoField(primary_key=True)
    doc_name = models.CharField(max_length=50)
    doc_age = models.IntegerField()
    gender = models.CharField(max_length=10)
    specialization = models.CharField(max_length=30)
    consulting_hour = models.CharField(max_length=20)
    department = models.CharField(max_length=50)
    status = models.CharField(max_length=20)
    contact = models.BigIntegerField()
    # h_id = models.IntegerField()
    hospital = models.ForeignKey(Hospital, to_field='h_id', db_column='h_id', on_delete=models.CASCADE)
    qualification = models.CharField(max_length=30, blank=True, null=True)
    email = models.CharField(max_length=50, blank=True, null=True)
    consultation_fee = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'doctor'

