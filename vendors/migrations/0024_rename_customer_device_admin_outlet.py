# Generated by Django 5.1.6 on 2025-05-26 07:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vendors', '0023_device_customer_alter_device_serial_no_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='device',
            old_name='customer',
            new_name='admin_outlet',
        ),
    ]
