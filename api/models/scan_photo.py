from __future__ import annotations

from django.db import models
from enum import Enum
from api.models import BaseModel, AppQuerySet, AppManager
from django_resized import ResizedImageField
import os
import uuid
from datetime import datetime


class ScanPhotoType(Enum):
    FRONT = "FRONT"
    RIGHT = "RIGHT"
    LEFT = "LEFT"
    LOWER = "LOWER"
    UPPER = "UPPER"

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]


def file_directory_path(instance, filename):
    now = datetime.now()
    return 'scan_photos/{0}/{1}/{2}/{3}{4}'.format(now.year, now.month, instance.scan.hash, str(uuid.uuid4()),
                                                   os.path.splitext(filename)[1])


class ScanPhotoQuerySet(AppQuerySet):
    def delete(self):
        """Override delete method to remove files before deleting instances."""
        for instance in self:
            print(instance)
            if instance.file:
                if os.path.isfile(instance.file.path):
                    os.remove(instance.file.path)
        return super().delete()

    pass


class ScanPhotoManager(AppManager.from_queryset(ScanPhotoQuerySet)):
    pass


class ScanPhoto(BaseModel):
    scan = models.ForeignKey("Scan", on_delete=models.CASCADE, related_name="scan_photos")
    type = models.CharField(choices=ScanPhotoType.choices(), default=ScanPhotoType.FRONT.value, max_length=50)
    file = ResizedImageField(size=[512, 1024], upload_to=file_directory_path, blank=True,
                             null=True)

    objects: ScanPhotoManager | ScanPhotoQuerySet = ScanPhotoManager()

    def __str__(self):
        return f"{self.scan.user.username}-scan-{self.scan_id}-photo-{self.id}"

    def delete(self, *args, **kwargs):
        if self.file:
            if os.path.isfile(self.file.path):
                os.remove(self.file.path)
        super().delete(*args, **kwargs)
