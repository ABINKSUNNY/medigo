from django.db import models
from doctor.models import Doctor
from patient.models import Patient
# # Create your models here.

class Chat(models.Model):
    ch_id = models.AutoField(primary_key=True)
    p_id = models.ForeignKey(Patient,to_field='p_id',db_column='p_id',on_delete=models.CASCADE)
    # doc_id = models.IntegerField()
    doctor = models.ForeignKey(Doctor, to_field='doc_id',  db_column='doc_id', on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    chat = models.CharField(max_length=500)
    to_type = models.CharField(max_length=30)
    from_type = models.CharField(max_length=30)
    seen = models.IntegerField(blank=True, null=True,default=0)

    class Meta:
        managed = False
        db_table = 'chat'
