from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils import timezone
from froala_editor.fields import FroalaField
from .helper import *
# Create your models here.

class CustomUser(AbstractUser):
    is_doctor = models.BooleanField(default=False)
    profilePic=models.ImageField(upload_to='profileImage',blank=True,null=True)
    address=models.CharField(null=True,blank=True,max_length=200)
    google_credentials=models.CharField(null=True,blank=True,max_length=20000)
     # Specify related names for the groups and user_permissions fields
    groups = models.ManyToManyField(
        'auth.Group',
        blank=True,
        related_name='customuser_set',
        related_query_name='customuser'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        blank=True,
        related_name='customuser_set',
        related_query_name='customuser'
    )



# for category 
class Category(models.Model):
    name=models.CharField(max_length=200)

    
    def __str__(self):
        return self.name  
        


# for post 

class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)
    

class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT ='DF', 'Draft'
        PUBLISHED ='PB','Published'
    title=models.CharField(max_length=250)
    slug=models.SlugField(max_length=1000,unique_for_date='publish',null=True,blank=True)
    # body=models.TextField()
    body=FroalaField()
    publish=models.DateField(default=timezone.now)
    author=models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='blog_posts')
    image=models.ImageField(upload_to='blogImage')
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now_add=True)
    status=models.CharField(max_length=2, choices=Status.choices,default=Status.DRAFT)
    category=models.ForeignKey(Category,on_delete=models.Case,related_name='postCategory')
    objects=models.Manager()  #default manage
    published= PublishedManager() #custom manage
    
    class Meta:
        ordering=['-publish']
        indexes=[models.Index(fields=['-publish']),]
    def __str__(self):
        return self.title
    def get_absolute_url(self):
        return reverse('post_detail',args=[self.publish.year,self.publish.month,self.publish.day,self.slug])
    
    def save(self,*args,**kwargs):
        self.slug=generate_slug(self.title)
        super(Post,self).save(*args,**kwargs)

