from nexus_core.reasoning.state import (
    ClaimStatus,
    InvestigationState,
)


def _format_percentage(value: float | None) -> str:
    if value is None:
        return "N/A"

    return f"{value:.2f}%"


def build_investigation_report(
    state: InvestigationState,
) -> str:
    question = state["question"]
    conclusion = state["conclusion"]
    root_cause_analysis = state["root_cause_analysis"]

    if conclusion is None:
        raise ValueError(
            "Investigation conclusion is required to build the report."
        )

    if root_cause_analysis is None:
        raise ValueError(
            "Root-cause analysis is required to build the report."
        )

    lines: list[str] = []

    lines.append("NEXUS AI — INVESTIGATION REPORT")
    lines.append("=" * 60)
    lines.append("")

    # ---------------------------------------------------------
    # Question
    # ---------------------------------------------------------

    lines.append("QUESTION")
    lines.append("-" * 60)
    lines.append(question)
    lines.append("")

    # ---------------------------------------------------------
    # Executive Summary
    # ---------------------------------------------------------

    lines.append("EXECUTIVE SUMMARY")
    lines.append("-" * 60)

    claim = conclusion.claim_assessment

    if claim is not None:
        if claim.status == ClaimStatus.CONFLICTING:
            lines.append(
                f"The stated claim of {claim.claim} is not supported "
                f"by the observed evidence."
            )

            if claim.observed_value is not None:
                lines.append(
                    f"The observed value was "
                    f"{_format_percentage(claim.observed_value)}."
                )

        elif claim.status == ClaimStatus.SUPPORTED:
            lines.append(
                f"The stated claim of {claim.claim} is consistent "
                f"with the observed evidence."
            )

        else:
            lines.append(claim.explanation)
    else:
        lines.append(conclusion.summary)

    lines.append("")

    # ---------------------------------------------------------
    # Claim Validation
    # ---------------------------------------------------------

    if claim is not None:
        lines.append("CLAIM VALIDATION")
        lines.append("-" * 60)

        lines.append(f"Claim: {claim.claim}")
        lines.append(f"Status: {claim.status.value}")

        if claim.observed_value is not None:
            lines.append(
                f"Observed: {_format_percentage(claim.observed_value)}"
            )

        lines.append(f"Confidence: {claim.confidence:.2f}")
        lines.append(f"Explanation: {claim.explanation}")
        lines.append("")
        
    # ---------------------------------------------------------
    # Key Evidence
    # ---------------------------------------------------------

    lines.append("KEY EVIDENCE")
    lines.append("-" * 60)

    for index, finding in enumerate(
        conclusion.findings,
        start=1,
    ):
        lines.append(
            f"{index}. {finding.cause}"
        )

        for evidence in finding.supporting_evidence:
            data = evidence.data

            if "segment" in data:
                lines.append(
                    f"   Segment: {data['segment']}"
                )

            if "satisfaction_band" in data:
                lines.append(
                    f"   Satisfaction band: {data['satisfaction_band']}"
                )

            if "product_change_band" in data:
                lines.append(
                    f"   Product changes: {data['product_change_band']}"
                )

            if "customers" in data:
                lines.append(
                    f"   Customers: {data['customers']}"
                )

            if "churned_customers" in data:
                lines.append(
                    f"   Churned customers: "
                    f"{data['churned_customers']}"
                )

            if "churn_rate" in data:
                lines.append(
                    f"   Churn rate: "
                    f"{data['churn_rate'] * 100:.2f}%"
                )

            if "previous_churn_rate" in data:
                lines.append(
                    f"   Previous quarter churn: "
                    f"{data['previous_churn_rate'] * 100:.2f}%"
                )

            if "current_churn_rate" in data:
                lines.append(
                    f"   Current quarter churn: "
                    f"{data['current_churn_rate'] * 100:.2f}%"
                )

            if "relative_change" in data:
                lines.append(
                    f"   Relative change: "
                    f"{data['relative_change'] * 100:.2f}%"
                )

            lines.append("")

    # ---------------------------------------------------------
    # Root Cause Analysis
    # ---------------------------------------------------------

    lines.append("ROOT-CAUSE ANALYSIS")
    lines.append("-" * 60)

    if root_cause_analysis.root_causes:
        for index, root_cause in enumerate(
            root_cause_analysis.root_causes,
            start=1,
        ):
            lines.append(
                f"{index}. {root_cause.cause}"
            )
            lines.append(
                f"   Explanation: {root_cause.explanation}"
            )
            lines.append(
                f"   Confidence: {root_cause.confidence:.2f}"
            )
            lines.append(
                f"   Causal status: {root_cause.causal_status}"
            )
            lines.append(
                f"   Supporting findings: "
                f"{root_cause.evidence_indices}"
            )
            lines.append("")
    else:
        lines.append(
            "No evidence-supported root cause was identified."
        )
        lines.append("")

    # ---------------------------------------------------------
    # Investigation Findings
    # ---------------------------------------------------------

    lines.append("OBSERVED FINDINGS")
    lines.append("-" * 60)

    for index, finding in enumerate(
        conclusion.findings,
        start=1,
    ):
        lines.append(
            f"{index}. {finding.cause}"
        )
        lines.append(
            f"   {finding.explanation}"
        )
        lines.append(
            f"   Confidence: {finding.confidence:.2f}"
        )
        lines.append("")

    # ---------------------------------------------------------
    # Limitations
    # ---------------------------------------------------------

    lines.append("LIMITATIONS")
    lines.append("-" * 60)

    if root_cause_analysis.limitations:
        for limitation in root_cause_analysis.limitations:
            lines.append(
                f"- {limitation}"
            )
    else:
        lines.append(
            "- No additional limitations were reported."
        )

    lines.append("")

    # ---------------------------------------------------------
    # Conclusion
    # ---------------------------------------------------------

    lines.append("CONCLUSION")
    lines.append("-" * 60)

    if root_cause_analysis.root_causes:
        primary = root_cause_analysis.root_causes[0]

        lines.append(
            f"The strongest observed association was: "
            f"{primary.cause}."
        )

        lines.append(
            "However, the available observational evidence does "
            "not establish causality."
        )
    else:
        lines.append(
            "The available evidence is insufficient to establish "
            "a root cause."
        )

    return "\n".join(lines)