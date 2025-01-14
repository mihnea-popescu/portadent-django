from __future__ import annotations

from django.db import models
from enum import Enum
from api.models import BaseModel, AppQuerySet, AppManager


class ScanProcessModelType(Enum):
    CHATGPT_4o = "chatgpt-4o"
    CHATGPT_4o_mini = "chatgpt-4o-mini"

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]


class ScanProcessQuerySet(AppQuerySet):
    pass


class ScanProcessManager(AppManager.from_queryset(ScanProcessQuerySet)):
    pass


class ScanProcess(BaseModel):
    scan = models.ForeignKey("Scan", on_delete=models.CASCADE, related_name="scan_processes")
    model = models.CharField(choices=ScanProcessModelType.choices(), default=ScanProcessModelType.CHATGPT_4o.value,
                             max_length=70)
    tokens_used = models.IntegerField(blank=True, null=True)

    objects: ScanProcessManager | ScanProcessQuerySet = ScanProcessManager()

    def __str__(self):
        return f"{self.scan.user.username}-scan-{self.scan_id}-process-{self.id}"
