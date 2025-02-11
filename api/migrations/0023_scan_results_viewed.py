# Generated by Django 4.2.16 on 2025-01-07 20:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0022_remove_scan_tokens_used_alter_scanprocess_model'),
    ]

    operations = [
        migrations.AddField(
            model_name='scan',
            name='results_viewed',
            field=models.BooleanField(default=False, help_text='True if the scan has been processed and the results have been viewed'),
        ),
    ]
