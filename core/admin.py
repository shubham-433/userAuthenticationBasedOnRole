from django.contrib import admin
from .models import *
# Register your models here.
@admin.register(CustomUser)
class ad(admin.ModelAdmin):
    list_display=['username']