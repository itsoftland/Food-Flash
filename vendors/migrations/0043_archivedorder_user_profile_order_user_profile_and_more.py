# Generated by Django 5.1.6 on 2025-07-15 04:59

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendors', '0042_userprofile'),
    ]

    operations = [
        migrations.AddField(
            model_name='archivedorder',
            name='user_profile',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='vendors.userprofile'),
        ),
        migrations.AddField(
            model_name='order',
            name='user_profile',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user_profile_orders', to='vendors.userprofile'),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('preparing', 'Preparing'), ('ready', 'Ready'), ('created', 'Created')], default='preparing', max_length=20),
        ),
    ]
