import re

from nexus_core.reasoning.state import (
    ClaimAssessment,
    ClaimStatus,
    Evidence,
)


PERCENTAGE_CLAIM_PATTERN = re.compile(
    r"(?P<value>\d+(?:\.\d+)?)\s*%"
)


def extract_percentage_claim(question: str) -> float | None:
    match = PERCENTAGE_CLAIM_PATTERN.search(question)

    if not match:
        return None

    return float(match.group("value"))


def validate_churn_claim(
    question: str,
    evidence: list[Evidence],
) -> ClaimAssessment:

    claimed_value = extract_percentage_claim(question)

    if claimed_value is None:
        return ClaimAssessment(
            claim=question,
            observed_value=None,
            observed_unit=None,
            status=ClaimStatus.NOT_APPLICABLE,
            explanation=(
                "No explicit percentage claim was found in the "
                "investigation question."
            ),
            evidence_indices=[],
            confidence=1.0,
        )

    temporal_indices = [
        index
        for index, item in enumerate(evidence)
        if item.type == "quarter_over_quarter_change"
    ]

    if not temporal_indices:
        return ClaimAssessment(
            claim=f"{claimed_value}% increase",
            observed_value=None,
            observed_unit="relative_percent",
            status=ClaimStatus.INSUFFICIENT_EVIDENCE,
            explanation=(
                "The investigation question contains a percentage claim, "
                "but no quarter-over-quarter churn evidence was found."
            ),
            evidence_indices=[],
            confidence=1.0,
        )

    evidence_index = temporal_indices[-1]
    temporal_evidence = evidence[evidence_index]

    observed_change = temporal_evidence.data.get(
        "relative_change"
    )

    if observed_change is None:
        return ClaimAssessment(
            claim=f"{claimed_value}% increase",
            observed_value=None,
            observed_unit="relative_percent",
            status=ClaimStatus.INSUFFICIENT_EVIDENCE,
            explanation=(
                "Quarter-over-quarter evidence was found, but it does "
                "not contain a relative churn change value."
            ),
            evidence_indices=[evidence_index],
            confidence=1.0,
        )

    observed_percentage = float(observed_change) * 100

    tolerance = 0.5

    if abs(observed_percentage - claimed_value) <= tolerance:
        status = ClaimStatus.SUPPORTED

        explanation = (
            f"The observed quarter-over-quarter churn increase was "
            f"{observed_percentage:.2f}%, which is consistent with "
            f"the {claimed_value:.2f}% increase stated in the question."
        )

    else:
        status = ClaimStatus.CONFLICTING

        explanation = (
            f"The observed quarter-over-quarter churn increase was "
            f"{observed_percentage:.2f}%, which differs from the "
            f"{claimed_value:.2f}% increase stated in the question."
        )

    return ClaimAssessment(
        claim=f"{claimed_value}% increase",
        observed_value=observed_percentage,
        observed_unit="relative_percent",
        status=status,
        explanation=explanation,
        evidence_indices=[evidence_index],
        confidence=1.0,
    )