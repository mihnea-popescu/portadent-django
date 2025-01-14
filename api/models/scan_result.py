from __future__ import annotations

from django.db import models
from enum import Enum
from api.models import BaseModel
from . import AppManager, AppQuerySet


class ScanResultToothType(Enum):
    TOOTH_11 = "11"  # Right maxillary central incisor
    TOOTH_12 = "12"  # Right maxillary lateral incisor
    TOOTH_13 = "13"  # Right maxillary canine
    TOOTH_14 = "14"  # Right maxillary 1st premolar
    TOOTH_15 = "15"  # Right maxillary 2nd premolar
    TOOTH_16 = "16"  # Right maxillary 1st molar
    TOOTH_17 = "17"  # Right maxillary 2nd molar
    TOOTH_18 = "18"  # Right maxillary 3rd molar

    TOOTH_21 = "21"  # Left maxillary central incisor
    TOOTH_22 = "22"  # Left maxillary lateral incisor
    TOOTH_23 = "23"  # Left maxillary canine
    TOOTH_24 = "24"  # Left maxillary 1st premolar
    TOOTH_25 = "25"  # Left maxillary 2nd premolar
    TOOTH_26 = "26"  # Left maxillary 1st molar
    TOOTH_27 = "27"  # Left maxillary 2nd molar
    TOOTH_28 = "28"  # Left maxillary 3rd molar

    TOOTH_31 = "31"  # Right mandibular central incisor
    TOOTH_32 = "32"  # Right mandibular lateral incisor
    TOOTH_33 = "33"  # Right mandibular canine
    TOOTH_34 = "34"  # Right mandibular 1st premolar
    TOOTH_35 = "35"  # Right mandibular 2nd premolar
    TOOTH_36 = "36"  # Right mandibular 1st molar
    TOOTH_37 = "37"  # Right mandibular 2nd molar
    TOOTH_38 = "38"  # Right mandibular 3rd molar

    TOOTH_41 = "41"  # Left mandibular central incisor
    TOOTH_42 = "42"  # Left mandibular lateral incisor
    TOOTH_43 = "43"  # Left mandibular canine
    TOOTH_44 = "44"  # Left mandibular 1st premolar
    TOOTH_45 = "45"  # Left mandibular 2nd premolar
    TOOTH_46 = "46"  # Left mandibular 1st molar
    TOOTH_47 = "47"  # Left mandibular 2nd molar
    TOOTH_48 = "48"  # Left mandibular 3rd molar
    GUM_UPPER_LEFT_OUTSIDE = 'GUM_UPPER_LEFT_OUTSIDE'
    GUM_UPPER_FRONT_OUTSIDE = 'GUM_UPPER_FRONT_OUTSIDE'
    GUM_UPPER_RIGHT_OUTSIDE = 'GUM_UPPER_RIGHT_OUTSIDE'
    GUM_LOWER_LEFT_OUTSIDE = 'GUM_LOWER_LEFT_OUTSIDE'
    GUM_LOWER_FRONT_OUTSIDE = 'GUM_LOWER_FRONT_OUTSIDE'
    GUM_LOWER_RIGHT_OUTSIDE = 'GUM_LOWER_RIGHT_OUTSIDE'
    ROOF = 'ROOF'
    TONGUE = 'TONGUE'

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]


class ScanResultSeverityType(Enum):
    HIGH = 'high'
    MEDIUM = 'medium'
    LOW = 'low'

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]


class ScanResultQuerySet(AppQuerySet):
    pass


class ScanResultManager(AppManager.from_queryset(ScanResultQuerySet)):
    pass


class ScanResult(BaseModel):
    scan = models.ForeignKey("Scan", on_delete=models.CASCADE, related_name="scan_results")

    tooth_type = models.CharField(choices=ScanResultToothType.choices(), default=ScanResultToothType.TOOTH_11.value,
                                  max_length=50)

    severity = models.CharField(choices=ScanResultSeverityType.choices(), default=ScanResultSeverityType.LOW.value,
                                max_length=50)

    details = models.CharField(blank=True, null=True, max_length=500)

    objects: ScanResultManager | ScanResultQuerySet = ScanResultManager()

    def __str__(self):
        return f"{self.scan.user.username}-scan-{self.scan_id}-result-{self.id}"
