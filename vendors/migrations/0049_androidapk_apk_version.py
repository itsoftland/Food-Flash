# Generated by Django 5.1.6 on 2025-07-16 06:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendors', '0048_alter_userprofile_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='androidapk',
            name='apk_version',
            field=models.CharField(blank=True, max_length=255, null=True, unique=True),
        ),
    ]
