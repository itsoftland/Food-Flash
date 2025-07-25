# Generated by Django 5.1.6 on 2025-07-22 04:59

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendors', '0053_archivedorder_created_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChatMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message_id', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('token_no', models.IntegerField()),
                ('created_date', models.DateField()),
                ('sender', models.CharField(choices=[('user', 'User'), ('manager', 'Manager')], max_length=10)),
                ('message_text', models.TextField(blank=True, null=True)),
                ('audio_file', models.FileField(blank=True, null=True, upload_to='chat/audio/')),
                ('is_read', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('reply_to', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='replies', to='vendors.chatmessage')),
                ('vendor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='chat_messages', to='vendors.vendor')),
            ],
            options={
                'ordering': ['created_at'],
                'indexes': [models.Index(fields=['vendor', 'token_no', 'created_date'], name='vendors_cha_vendor__1c51ef_idx')],
                'constraints': [models.UniqueConstraint(fields=('vendor', 'token_no', 'created_date', 'message_id'), name='unique_chat_message_per_order')],
            },
        ),
    ]
