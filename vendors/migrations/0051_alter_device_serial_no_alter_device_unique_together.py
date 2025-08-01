# Generated by Django 5.1.6 on 2025-07-17 12:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendors', '0050_advertisementimage_created_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='device',
            name='serial_no',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterUniqueTogether(
            name='device',
            unique_together={('serial_no', 'admin_outlet')},
        ),
    ]
