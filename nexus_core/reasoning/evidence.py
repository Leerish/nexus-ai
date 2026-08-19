from nexus_core.reasoning.state import (
    Evidence,
    TaskResult,
)


def collect_evidence(results: list[TaskResult]) -> list[Evidence]:
    evidence: list[Evidence] = []

    for result in results:
        if result.status.value != "completed":
            continue

        evidence.extend(result.evidence)

    return evidence