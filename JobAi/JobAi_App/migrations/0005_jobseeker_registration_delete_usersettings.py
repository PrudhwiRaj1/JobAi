# Generated by Django 5.1.5 on 2025-02-06 00:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('JobAi_App', '0004_remove_company_created_at_remove_company_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Jobseeker_Registration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('password', models.CharField(max_length=255)),
            ],
        ),
        migrations.DeleteModel(
            name='UserSettings',
        ),
    ]
