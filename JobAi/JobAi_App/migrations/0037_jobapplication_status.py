# Generated by Django 5.1.5 on 2025-03-13 10:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('JobAi_App', '0036_rename_jobseeker_jobnotification_jobseeker_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobapplication',
            name='status',
            field=models.TextField(default='Applied'),
        ),
    ]
