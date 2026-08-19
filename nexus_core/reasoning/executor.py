from datetime import datetime, timezone

from nexus_core.analysis.churn import (
    analyze_churn_by_segment_evidence,
)
from nexus_core.analysis.product_changes import (
    analyze_churn_by_product_changes_evidence,
)
from nexus_core.analysis.router import resolve_analysis
from nexus_core.analysis.satisfaction import (
    analyze_churn_by_satisfaction_evidence,
)
from nexus_core.analysis.temporal import (
    analyze_churn_by_quarter_evidence,
)

from nexus_core.reasoning.state import (
    InvestigationTask,
    TaskResult,
    TaskStatus,
    TaskType,
    WorkerState,
)

def execute_task(task: InvestigationTask) -> TaskResult:
    started_at = datetime.now(timezone.utc)

    try:
        if task.type in {
            TaskType.DATA_ANALYSIS,
            TaskType.TEMPORAL_ANALYSIS,
        }:
            analysis_type = resolve_analysis(task)

            if analysis_type == "churn_by_segment":
                evidence = analyze_churn_by_segment_evidence()

            elif analysis_type == "churn_satisfaction":
                evidence = analyze_churn_by_satisfaction_evidence()

            elif analysis_type == "product_change_churn":
                evidence = analyze_churn_by_product_changes_evidence()

            elif analysis_type == "temporal_churn":
                evidence = analyze_churn_by_quarter_evidence()

            else:
                raise ValueError(
                    f"Unsupported analysis task: {task.description}"
                )

            return TaskResult(
                task=task,
                result=f"{analysis_type} analysis completed.",
                status=TaskStatus.COMPLETED,
                started_at=started_at,
                completed_at=datetime.now(timezone.utc),
                evidence=evidence,
            )

        if task.type == TaskType.ROOT_CAUSE:
            raise ValueError(
                "ROOT_CAUSE tasks are handled by the root_cause "
                "graph node, not the task executor."
            )

        if task.type == TaskType.EVIDENCE_GATHERING:
            raise ValueError(
                "EVIDENCE_GATHERING is not currently supported."
            )

        raise NotImplementedError(
            f"Task type {task.type.value} is not implemented yet."
        )

    except Exception as exc:
        return TaskResult(
            task=task,
            result=str(exc),
            status=TaskStatus.FAILED,
            started_at=started_at,
            completed_at=datetime.now(timezone.utc),
            evidence=[],
        )

def worker_node(state: WorkerState) -> dict:
    result = execute_task(state["task"])

    return {
        "results": [result],
    }