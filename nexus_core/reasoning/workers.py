from nexus_core.reasoning.state import (
    InvestigationState,
    TaskResult,
    TaskType,
)


def execute_data_analysis(
    state: InvestigationState,
) -> dict:
    task = next(
        task
        for task in state["tasks"]
        if task.type == TaskType.DATA_ANALYSIS
    )

    result = TaskResult(
        task=task,
        result=f"Data analysis task queued: {task.description}",
    )

    return {
        "results": [result],
    }


def execute_temporal_analysis(
    state: InvestigationState,
) -> dict:
    task = next(
        task
        for task in state["tasks"]
        if task.type == TaskType.TEMPORAL_ANALYSIS
    )

    result = TaskResult(
        task=task,
        result=f"Temporal analysis task queued: {task.description}",
    )

    return {
        "results": [result],
    }


def execute_evidence_gathering(
    state: InvestigationState,
) -> dict:
    task = next(
        task
        for task in state["tasks"]
        if task.type == TaskType.EVIDENCE_GATHERING
    )

    result = TaskResult(
        task=task,
        result=f"Evidence gathering task queued: {task.description}",
    )

    return {
        "results": [result],
    }


def execute_root_cause(
    state: InvestigationState,
) -> dict:
    task = next(
        task
        for task in state["tasks"]
        if task.type == TaskType.ROOT_CAUSE
    )

    result = TaskResult(
        task=task,
        result=f"Root cause task queued: {task.description}",
    )

    return {
        "results": [result],
    }