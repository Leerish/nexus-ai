from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field

from nexus_core.investigation.models import (
    InvestigationPriority,
    InvestigationStatus,
)


class InvestigationCreate(BaseModel):
    question: str = Field(min_length=1, max_length=2000)
    priority: InvestigationPriority = InvestigationPriority.MEDIUM


class InvestigationResponse(BaseModel):
    id: UUID
    question: str
    status: InvestigationStatus
    priority: InvestigationPriority
    confidence_score: float | None
    created_at: datetime
    started_at: datetime | None
    completed_at: datetime | None
    result: dict | None
    model_config = {
        "from_attributes": True
    }