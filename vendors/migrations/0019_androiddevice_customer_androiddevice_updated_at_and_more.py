# Generated by Django 5.1.6 on 2025-05-22 08:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendors', '0018_androiddevice_mac_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='androiddevice',
            name='customer',
            field=models.ForeignKey(default=7, on_delete=django.db.models.deletion.CASCADE, to='vendors.adminoutlet'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='androiddevice',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='androiddevice',
            name='vendor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='vendors.vendor'),
        ),
    ]
