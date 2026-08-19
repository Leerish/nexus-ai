from enum import StrEnum
from typing import TypedDict

from uuid import UUID , uuid4

from pydantic import BaseModel, Field

from datetime import datetime

from typing import Any



class TaskType(StrEnum):
    DATA_ANALYSIS = "data_analysis"
    TEMPORAL_ANALYSIS = "temporal_analysis"
    ROOT_CAUSE = "root_cause"
    EVIDENCE_GATHERING = "evidence_gathering"

class TaskStatus(StrEnum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


class InvestigationTask(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    type: TaskType
    description: str = Field(min_length=1, max_length=1000)


class PlannerOutput(BaseModel):
    tasks: list[InvestigationTask] = Field(min_length=1, max_length=8)
    
class Evidence(BaseModel):
    source: str
    type: str
    data: dict[str, Any]
    query: str | None = None
    methodology: str | None = None
    confidence: float | None = Field(
        default=None,
        ge=0.0,
        le=1.0,
    )


class TaskResult(BaseModel):
    task: InvestigationTask
    result: str | None = None
    status: TaskStatus = TaskStatus.PENDING
    started_at: datetime | None = None
    completed_at: datetime | None = None
    evidence: list[Evidence] = Field(default_factory=list)
    

class InvestigationState(TypedDict):
    investigation_id: str
    question: str
    tasks: list[InvestigationTask]
    results: list[TaskResult]
    
    
class WorkerState(TypedDict):
    task: InvestigationTask
    
        
class InvestigationFinding(BaseModel):
    cause: str
    explanation: str
    supporting_evidence: list[Evidence] = Field(default_factory=list)
    confidence: float = Field(
        ge=0.0,
        le=1.0,
    )

class ClaimStatus(StrEnum):
    SUPPORTED = "supported"
    CONFLICTING = "conflicting"
    INSUFFICIENT_EVIDENCE = "insufficient_evidence"
    NOT_APPLICABLE = "not_applicable"


class ClaimAssessment(BaseModel):
    claim: str

    observed_value: float | None = None

    observed_unit: str | None = None

    status: ClaimStatus

    explanation: str

    evidence_indices: list[int] = Field(
        default_factory=list
    )

    confidence: float = Field(
        ge=0.0,
        le=1.0,
    )


class InvestigationConclusion(BaseModel):
    summary: str

    findings: list[InvestigationFinding] = Field(
        default_factory=list
    )

    claim_assessment: ClaimAssessment | None = None
    
class RootCauseCandidate(BaseModel):
    cause: str
    explanation: str
    evidence_indices: list[int] = Field(default_factory=list)
    confidence: float = Field(
        ge=0.0,
        le=1.0,
    )
    causal_status: str


class RootCauseAnalysis(BaseModel):
    root_causes: list[RootCauseCandidate] = Field(
        default_factory=list
    )
    limitations: list[str] = Field(
        default_factory=list
    )

    
class InvestigationState(TypedDict):
    investigation_id: str
    question: str
    tasks: list[InvestigationTask]
    results: list[TaskResult]
    conclusion: InvestigationConclusion | None
    root_cause_analysis: RootCauseAnalysis | None
    
class InvestigationState(TypedDict):
    investigation_id: str
    question: str
    tasks: list[InvestigationTask]
    results: list[TaskResult]
    conclusion: InvestigationConclusion | None
    root_cause_analysis: RootCauseAnalysis | None
    report: str | None