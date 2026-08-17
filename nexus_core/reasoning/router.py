from nexus_core.reasoning.state import InvestigationTask, TaskType


def route_task(task: InvestigationTask) -> str:
    routes = {
        TaskType.DATA_ANALYSIS: "data_analysis",
        TaskType.TEMPORAL_ANALYSIS: "temporal_analysis",
        TaskType.ROOT_CAUSE: "root_cause",
        TaskType.EVIDENCE_GATHERING: "evidence_gathering",
    }

    return routes[task.type]