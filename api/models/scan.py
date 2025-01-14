from __future__ import annotations

from django.db import models
from enum import Enum
from api.models import BaseModel
import secrets
from . import AppManager, AppQuerySet


class ScanSourceType(Enum):
    WEB_APP = "WEB_APP"
    MOBILE_APP = "MOBILE_APP"

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]


class ScanStatusType(Enum):
    INITIALIZED = "INITIALIZED"
    PHOTOS_FINISHED = "PHOTOS_FINISHED"
    FINISHED = "FINISHED"
    ERROR = "ERROR"

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]


class ScanRiskType(Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]


class ScanQuerySet(AppQuerySet):
    pass


class ScanManager(AppManager.from_queryset(ScanQuerySet)):
    pass


class Scan(BaseModel):
    status = models.CharField(choices=ScanStatusType.choices(), default=ScanStatusType.INITIALIZED.value, max_length=50)

    source = models.CharField(choices=ScanSourceType.choices(), default=ScanSourceType.WEB_APP.value, max_length=50)

    hash = models.CharField(blank=True, null=True, max_length=100)

    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="scans")

    summary = models.CharField(blank=True, null=True, max_length=500)

    risk = models.CharField(choices=ScanRiskType.choices(), blank=True, null=True, max_length=25)

    # This will be shown to users
    error_message = models.CharField(blank=True, null=True, max_length=500)

    # This will be kept internally
    internal_error_message = models.CharField(blank=True, null=True, max_length=500)

    results_viewed = models.BooleanField(default=False,
                                         help_text="True if the scan has been processed and the results have been viewed")

    objects: ScanManager | ScanQuerySet = ScanManager()

    def __str__(self):
        return f"scan-{self.user.username}-{self.user_id}-{self.id}"

    def generateHash(self) -> str:
        """Generate a unique 40-character hash for the Scan model."""
        while True:
            # Generate a 40-character random string
            random_string = secrets.token_hex(20)  # 20 bytes = 40 characters in hexadecimal

            # Check if the hash is unique
            if not Scan.objects.filter(hash=random_string).exists():
                return random_string
                break

        return self.hash

    def hasAllPhotos(self) -> bool:
        """Returns True if all the photos required for the scan have been created"""
        from api.models import ScanPhoto, ScanPhotoType

        for scan_photo_type in ScanPhotoType.choices():
            if not ScanPhoto.objects.filter(scan_id=self.id, type=scan_photo_type[0]).exists():
                return False
        return True
