# Generated by Django 5.0.3 on 2024-06-11 13:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_users'),
    ]

    operations = [
        migrations.AddField(
            model_name='gedung',
            name='image',
            field=models.ImageField(null=True, upload_to='uploads/'),
        ),
    ]
