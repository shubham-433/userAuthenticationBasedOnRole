from django.db import models
from django.conf import settings

# Create your models here.
from django.db import models

class Appointment(models.Model):
    doctor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name='doctor_appointment_list')
    patient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    speciality = models.CharField(max_length=255)
    appointment_date = models.DateTimeField(blank=True,null=True)
    appointment_start_time = models.DateTimeField()
    appointment_end_time = models.DateTimeField()
    
   

    def __str__(self):
        return f'{self.doctor} - {self.appointment_date} - {self.appointment_start_time}'