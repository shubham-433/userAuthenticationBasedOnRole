from django.contrib import admin
from .models import *
# Register your models here.
@admin.register(CustomUser)
class ad(admin.ModelAdmin):
    list_display=['username']

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display=['title','slug','author','publish','status']
    list_filter=['status','created','publish']
    search_fields=['title','body']
    # prepopulated_fields={'slug':('title',)}
    raw_id_fields=['author']
    date_hierarchy='publish'
    ordering=['status','publish']

@admin.register(Category)
class Postcategory(admin.ModelAdmin):
    list_display=['name']