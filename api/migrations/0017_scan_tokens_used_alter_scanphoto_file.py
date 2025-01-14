# Generated by Django 4.2.16 on 2024-12-13 23:38

import api.models.scan_photo
from django.db import migrations, models
import django_resized.forms


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0016_scan_internal_error_message'),
    ]

    operations = [
        migrations.AddField(
            model_name='scan',
            name='tokens_used',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='scanphoto',
            name='file',
            field=django_resized.forms.ResizedImageField(blank=True, crop=None, force_format=None, keep_meta=True, null=True, quality=-1, scale=None, size=[512, 1024], upload_to=api.models.scan_photo.file_directory_path),
        ),
    ]
