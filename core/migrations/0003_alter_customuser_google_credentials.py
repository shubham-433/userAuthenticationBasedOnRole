# Generated by Django 4.1 on 2023-05-05 08:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_customuser_google_credentials'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='google_credentials',
            field=models.CharField(blank=True, max_length=20000, null=True),
        ),
    ]
