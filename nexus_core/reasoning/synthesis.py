from nexus_core.reasoning.state import (
    Evidence,
    InvestigationFinding,
)


def synthesize_evidence(
    evidence: list[Evidence],
) -> list[InvestigationFinding]:
    findings: list[InvestigationFinding] = []

    for item in evidence:
        if item.type == "quarter_over_quarter_change":
            current = item.data["current_churn_rate"]
            previous = item.data["previous_churn_rate"]
            relative_change = item.data["relative_change"]

            findings.append(
                InvestigationFinding(
                    cause="Churn increased quarter-over-quarter",
                    explanation=(
                        f"Churn increased from "
                        f"{previous:.2%} to {current:.2%}, "
                        f"representing a {relative_change:.2%} "
                        f"relative increase."
                    ),
                    supporting_evidence=[item],
                    confidence=1.0,
                )
            )

        elif item.type == "satisfaction_churn_analysis":
            band = item.data["satisfaction_band"]
            churn_rate = item.data["churn_rate"]

            if band == "medium" and churn_rate > 0.05:
                findings.append(
                    InvestigationFinding(
                        cause="Elevated churn among medium-satisfaction customers",
                        explanation=(
                            f"Customers in the medium satisfaction band "
                            f"had a churn rate of {churn_rate:.2%}."
                        ),
                        supporting_evidence=[item],
                        confidence=0.85,
                    )
                )

        elif item.type == "product_change_churn_analysis":
            band = item.data["product_change_band"]
            churn_rate = item.data["churn_rate"]

            if band == "multiple" and churn_rate > 0.03:
                findings.append(
                    InvestigationFinding(
                        cause="Higher churn among customers experiencing multiple product changes",
                        explanation=(
                            f"Customers with multiple product changes "
                            f"had a churn rate of {churn_rate:.2%}."
                        ),
                        supporting_evidence=[item],
                        confidence=0.75,
                    )
                )

        elif item.type == "aggregate":
            segment = item.data.get("segment")
            churn_rate = item.data.get("churn_rate")

            if segment == "SMB" and churn_rate is not None:
                findings.append(
                    InvestigationFinding(
                        cause="SMB customers have the highest observed segment churn",
                        explanation=(
                            f"SMB customers had an observed churn rate "
                            f"of {churn_rate:.2%}."
                        ),
                        supporting_evidence=[item],
                        confidence=0.70,
                    )
                )

    return findings