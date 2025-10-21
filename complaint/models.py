from django.db import models
from patient.models import Patient

# Create your models here.

class Complaint(models.Model):
    c_id = models.AutoField(primary_key=True)
    patient = models.ForeignKey(Patient, to_field='p_id',db_column='p_id',on_delete=models.CASCADE)
    complaint = models.CharField(max_length=999)
    date = models.DateField()
    time = models.TimeField()
    reply = models.CharField(max_length=999)

    class Meta:
        managed = False
        db_table = 'complaint'

