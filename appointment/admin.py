from django.contrib import admin
from .models import *
# Register your models here.
@admin.register(Appointment)
class Postcategory(admin.ModelAdmin):
    list_display=['doctor','patient','appointment_date','appointment_start_time','appointment_end_time']