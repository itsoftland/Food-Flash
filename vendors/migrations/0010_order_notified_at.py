# Generated by Django 5.1.6 on 2025-04-23 12:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendors', '0009_alter_feedback_category_alter_feedback_feedback_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='notified_at',
            field=models.DateTimeField(blank=True, default=None, null=True),
        ),
    ]
