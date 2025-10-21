# models.py in the appointment app
from django.db import models
from hospital.models import Hospital
from doctor.models import Doctor
from patient.models import Patient

# class Appointment(models.Model):
#     a_id = models.AutoField(primary_key=True)
#     patient = models.ForeignKey(Patient, to_field='p_id', db_column='p_id', on_delete=models.CASCADE)
#     hospital = models.ForeignKey(Hospital, to_field='h_id', db_column='h_id', on_delete=models.CASCADE)
#     doctor = models.ForeignKey(Doctor, to_field='doc_id', db_column='doc_id', on_delete=models.CASCADE)
#     date = models.DateField(blank=True, null=True)
#     time = models.TimeField(blank=True, null=True)
#     status = models.CharField(max_length=20, blank=True, null=True)
#     type = models.CharField(max_length=20, blank=True, null=True)
#
#     class Meta:
#         managed = False
#         db_table = 'appointment'
class Appointment(models.Model):
    a_id = models.AutoField(primary_key=True)
    # p_id = models.IntegerField()
    # h_id = models.IntegerField()
    # doc_id = models.IntegerField()
    patient = models.ForeignKey(Patient, to_field='p_id', db_column='p_id', on_delete=models.CASCADE)
    hospital = models.ForeignKey(Hospital, to_field='h_id', db_column='h_id', on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, to_field='doc_id', db_column='doc_id', on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    status = models.CharField(max_length=20)
    type = models.CharField(max_length=20)
    payment_id = models.CharField(max_length=20, blank=True, null=True)
    amount = models.IntegerField(blank=True, null=True)
    payment_date = models.DateField(blank=True, null=True)
    payment_time = models.TimeField(blank=True, null=True)
    is_seen = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'appointment'


