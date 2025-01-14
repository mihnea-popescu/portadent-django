from pydantic import BaseModel
from typing import Optional
from api.models.scan_result import ScanResultSeverityType, ScanResultToothType
from api.models.scan import ScanRiskType


class ScanProcessToothResponseType(BaseModel):
    tooth_type: ScanResultToothType
    priority: ScanResultSeverityType
    summary: str


class ScanProcessResponseType(BaseModel):
    success: bool
    overall_priority: ScanRiskType
    overall_summary: str
    message: Optional[str]
    results: list[ScanProcessToothResponseType]
