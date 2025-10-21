from django.db import models

# Create your models here.
class Medicine(models.Model):
    m_id = models.AutoField(primary_key=True)
    medname = models.CharField(max_length=30)
    rate = models.FloatField()
    mfd = models.DateField()
    exd = models.DateField()

    class Meta:
        managed = False
        db_table = 'medicine'
