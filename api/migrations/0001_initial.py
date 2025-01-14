# Generated by Django 4.2.16 on 2024-10-23 18:32

import api.models.user
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="User",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("password", models.CharField(max_length=128, verbose_name="password")),
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                ("username", models.CharField(max_length=150, unique=True)),
                (
                    "email",
                    models.EmailField(
                        blank=True,
                        db_index=True,
                        max_length=254,
                        null=True,
                        unique=True,
                    ),
                ),
                ("first_name", models.CharField(blank=True, max_length=150)),
                ("last_name", models.CharField(blank=True, max_length=150)),
                (
                    "is_staff",
                    models.BooleanField(
                        default=False, help_text="User can log into this admin site"
                    ),
                ),
                (
                    "language_tag",
                    models.CharField(blank=True, max_length=32, null=True),
                ),
                ("country_code", models.CharField(blank=True, max_length=8, null=True)),
                (
                    "timezone",
                    models.SmallIntegerField(
                        default=0,
                        help_text="Most recent timezone used by user on any device",
                    ),
                ),
                (
                    "subscribed",
                    models.BooleanField(
                        default=True,
                        help_text="True if user wants to receive emails from us",
                    ),
                ),
                (
                    "last_activity",
                    models.DateTimeField(default=django.utils.timezone.now),
                ),
                ("created_at", models.DateTimeField(default=django.utils.timezone.now)),
                ("updated_at", models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
                "verbose_name": "User",
                "verbose_name_plural": "Users",
                "db_table": "auth_user",
            },
            managers=[
                ("objects", api.models.user.UserManager()),
            ],
        ),
    ]
