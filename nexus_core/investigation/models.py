from datetime import datetime
from enum import Enum
from uuid import UUID, uuid4

from sqlalchemy import DateTime, Enum as SQLEnum, Float, String, func
from sqlalchemy.dialects.postgresql import JSONB, UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column

from nexus_core.database.base import Base


class InvestigationStatus(str, Enum):
    PENDING = "pending"
    PLANNING = "planning"
    RUNNING = "running"
    VALIDATING = "validating"
    COMPLETED = "completed"
    FAILED = "failed"
    ARCHIVED = "archived"


class InvestigationPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class Investigation(Base):
    __tablename__ = "investigations"

    id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )

    question: Mapped[str] = mapped_column(
        String(2000),
        nullable=False,
    )

    status: Mapped[InvestigationStatus] = mapped_column(
        SQLEnum(InvestigationStatus, name="investigation_status"),
        default=InvestigationStatus.PENDING,
        nullable=False,
    )

    priority: Mapped[InvestigationPriority] = mapped_column(
        SQLEnum(InvestigationPriority, name="investigation_priority"),
        default=InvestigationPriority.MEDIUM,
        nullable=False,
    )

    confidence_score: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )
    
    result: Mapped[dict | None] = mapped_column(
        JSONB,
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    started_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    completed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    
    