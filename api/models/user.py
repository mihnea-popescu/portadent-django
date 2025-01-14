from __future__ import annotations

from django.db import models
from django.contrib.auth.models import (AbstractBaseUser,
                                        UserManager as DjangoUserManager)
from django.utils import timezone as django_timezone
from datetime import datetime
import re
import random

from core.time.timezones import get_local_time


class UserQuerySet(models.QuerySet):
    def update(self, **kwargs):
        """Ensure that `updated_at` is automatically updated on bulk updates."""
        if 'updated_at' not in kwargs:
            kwargs['updated_at'] = django_timezone.now()
        return super().update(**kwargs)

    pass


class UserManager(DjangoUserManager.from_queryset(UserQuerySet)):
    """Custom manager for User model.

    NOTE: Manager must inherit from the DjangoUserManager generated from our
    UserQuerySet
    Docs: https://django.readthedocs.io/en/stable/topics/migrations.html#model-managers
    """

    def update_last_activity(self, user: User) -> int:
        now: datetime = django_timezone.now()

        return self.filter(id=user.id).update(last_activity=now)

    def create_user(self, email, password=None, **extra_fields):
        """Create and return a regular user with an email and password."""
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """Create and return a superuser with an email and password."""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser):
    username = models.CharField(max_length=150)
    email = models.EmailField(blank=True, null=True, db_index=True, unique=True)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)

    is_staff = models.BooleanField(default=False, help_text=("User can log into this admin site"))

    # Most recent locale settings from any user device
    #
    # Language is represented as a IETF BCP 47 language tag. Common tags
    # have this form: "<language_code>-<country_code>". E.g. en-us, en-gb
    language_tag = models.CharField(max_length=32, blank=True, null=True)
    country_code = models.CharField(max_length=8, blank=True, null=True)

    timezone = models.SmallIntegerField(
        default=0,
        blank=False,
        null=False,
        help_text="Most recent timezone used by user on any device",
    )

    subscribed = models.BooleanField(default=True, help_text="True if user wants to receive emails from us")

    last_activity = models.DateTimeField(default=django_timezone.now)

    questionnaire_answers = models.JSONField(blank=True, null=True, max_length=1000)

    created_at = models.DateTimeField(default=django_timezone.now)
    updated_at = models.DateTimeField(default=django_timezone.now)

    last_change_password_email_sent_at = models.DateTimeField(blank=True, null=True)

    # This field is just an UserManager, but with Union we can access
    # UserQuerySet methods via auto-complete
    objects: UserManager | UserQuerySet = UserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        app_label = "api"
        db_table = "auth_user"
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        """Override save method to update last_activity timestamp."""
        self.last_activity = django_timezone.now()
        self.updated_at = django_timezone.now()  # Ensure updated_at is also updated
        super().save(*args, **kwargs)

    def to_dict(self) -> dict:
        """Return dictionary representing details about the current User instance"""

        fields_to_get = [
            "id",
            "username",
            "first_name",
            "last_name",
            "photo",
        ]

        return {field: getattr(self, field) for field in fields_to_get}

    def generate_username(self, min_length: int = 3, max_length: int = 15) -> str:
        """Generate a unique username for a user based on their information.
        
        Creates a username using email, names, or default pattern with numeric suffix if needed.
        
        Args:
            min_length: Minimum allowed username length (default 3)
            max_length: Maximum allowed username length (default 15)
            
        Returns:
            A unique username string meeting the length requirements
            
        Raises:
            Exception: If user does not have an ID yet
        """
        if not self.pk:
            raise Exception("Cannot generate username - user must be saved first")
            
        # Get base components, defaulting to empty strings
        email_name = self.email.split('@')[0].lower() if self.email else ''
        first = self.first_name.lower() if self.first_name else ''
        last = self.last_name.lower() if self.last_name else ''
        
        # Clean components to only allow alphanumeric and underscore
        email_name = re.sub(r'[^a-z0-9_]', '', email_name)
        first = re.sub(r'[^a-z0-9_]', '', first)
        last = re.sub(r'[^a-z0-9_]', '', last)
        
        # Try different username patterns in order of preference
        username_options = [
            f"{first}{last}",
            email_name,
            first,
            last,
            f"user{self.pk}",
            f"portadent{self.pk}"
        ]
        
        # Use first valid option that meets minimum length
        base_username = next(
            (name for name in username_options 
             if name and len(name) >= min_length),
            f"portadent{self.pk}"  # Fallback default
        )
        
        # Truncate to max length
        base_username = base_username[:max_length]
        
        # Add numbers if needed to make unique
        final_username = base_username
        suffix = 1
        
        while User.objects.filter(username=final_username).exists():
            suffix_str = str(suffix)
            final_username = f"{base_username[:max_length-len(suffix_str)]}{suffix_str}"
            suffix += 1
            
        return final_username

    def local_time(self, utc_time: datetime) -> datetime:
        """Convert UTC to user's local time.

        It returns the UTC if the user doesn't have a timezone.
        """
        if not self.timezone:
            return utc_time

        user_local_time = get_local_time(utc_time, self.timezone)
        return user_local_time

    def has_perm(self, perm, obj=None):
        """Allow permissions only for staff users."""
        return self.is_staff

    def has_module_perms(self, app_label: str) -> bool:
        """
        Return True if the user has permissions to view the app `app_label`.
        Admin interface uses this to control access to app modules.
        """
        return self.is_staff
