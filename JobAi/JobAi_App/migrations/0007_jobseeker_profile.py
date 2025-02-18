# Generated by Django 5.1.5 on 2025-02-06 06:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('JobAi_App', '0006_jobseeker_registration_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='jobseeker_profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('phone', models.CharField(blank=True, max_length=20, null=True)),
                ('dob', models.CharField(blank=True, max_length=50, null=True)),
                ('highest_qualification', models.CharField(blank=True, max_length=255, null=True)),
                ('job_preference', models.CharField(blank=True, max_length=255, null=True)),
                ('university', models.CharField(blank=True, max_length=255, null=True)),
                ('address', models.TextField(blank=True, null=True)),
                ('skills', models.TextField(blank=True, null=True)),
                ('resume', models.FileField(blank=True, null=True, upload_to='documents/')),
            ],
        ),
    ]
