from django.db import models
from patient.models import Patient
from doctor.models import Doctor
# Create your models here.

class Prescription(models.Model):
    pres_id = models.AutoField(primary_key=True)
    # doc_id = models.IntegerField()
    # p_id = models.IntegerField()
    doctor = models.ForeignKey(Doctor, to_field='doc_id', db_column='doc_id', on_delete=models.CASCADE, default=1)
    patient = models.ForeignKey(Patient, to_field='p_id', db_column='p_id', on_delete=models.CASCADE)
    prescription = models.CharField(max_length=500)
    date = models.DateField()
    time = models.TimeField()

    class Meta:
        managed = False
        db_table = 'prescription'
