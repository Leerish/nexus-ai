import json

from nexus_core.reasoning.state import (
    Evidence,
    InvestigationFinding,
)
from nexus_core.llm import get_llm


ROOT_CAUSE_PROMPT = """
You are the root-cause reasoning component of Nexus AI.

Your job is to analyze structured investigation findings and identify
the strongest evidence-supported drivers of the investigated outcome.

IMPORTANT RULES:

1. Do not invent facts.

2. Do not invent evidence.

3. Do not perform unsupported causal claims.

4. Distinguish correlation/association from causation.

5. Prefer findings with stronger evidence and higher confidence.

6. If the evidence is insufficient to establish a root cause, explicitly
   say so.

7. Numerical values must come from the supplied evidence.

8. The reported question may contain an expected value that differs from
   the observed evidence. Do not force the evidence to match the question.

9. Distinguish OUTCOME findings from DRIVER findings.

   OUTCOME findings describe what happened in the investigation.
   DRIVER findings describe factors that may be associated with the outcome.

   Never classify an outcome finding itself as a root cause.

   Examples:

   - "Churn increased quarter-over-quarter" is an OUTCOME, not a root cause.
   - "Medium-satisfaction customers had 8.49% churn" is a potential DRIVER.
   - "SMB customers had 3.62% churn" is a potential DRIVER.
   - "Customers with multiple product changes had 3.64% churn" is a potential DRIVER.

10. Evaluate potential drivers using:

    - strength of the observed association,
    - size of the affected population,
    - consistency with other findings,
    - and whether temporal evidence supports the relationship.

11. Cross-sectional or observational associations must NOT be presented
    as established causal relationships.

12. Use "strong_candidate" only when the evidence for a specific driver is
    substantially stronger than the evidence for competing drivers and
    the available evidence provides meaningful support for that driver.

    Do not use "strong_candidate" when the evidence is only cross-sectional
    and there is no temporal or causal evidence supporting its contribution
    to the investigated change.

13. Use "supported_association" when a finding shows a meaningful association
    with the observed outcome but causality has not been established.

14. Use "insufficient_evidence" when the available evidence is not strong
    enough to support a meaningful driver.

15. If a finding describes the outcome itself, exclude it from root_causes.
    It may instead be referenced in the explanation or limitations.

16. Do not use phrases such as "caused", "was responsible for", "led to",
    or "resulted in" unless the supplied evidence explicitly establishes
    causality.

17. When multiple potential drivers exist, return the strongest relevant
    candidates rather than selecting only one unless the evidence clearly
    supports a single dominant driver.

18. evidence_indices must contain only the indices of findings that directly
    support the specific root-cause candidate.

    Do not include an outcome finding merely because it establishes that the
    investigated outcome occurred.

    For example, if a candidate is "Elevated churn among medium-satisfaction
    customers", reference the satisfaction finding, not the general
    quarter-over-quarter churn finding.

19. Use all relevant fields contained in supporting_evidence, including
    customer counts, churned customer counts, rates, dates, periods, and
    other numerical measurements.

20. Do not claim that a piece of information is unavailable if that
    information is explicitly present in the supplied evidence.

21. Before writing limitations, verify each limitation against the supplied
    evidence.

    Never state that population size, churn counts, rates, dates, periods,
    or other metrics are missing when they are explicitly present.

22. Do not compare a subgroup's churn rate to an overall churn rate from
    a different time period and interpret the difference as evidence that
    the subgroup contributed to the temporal change.

23. A subgroup churn rate may be described as elevated relative to another
    subgroup only when the comparison uses the same population definition
    and the same time period.

24. Do not infer contribution to a quarter-over-quarter change from a
    cross-sectional subgroup churn rate alone.

25. If temporal evidence for a potential driver is unavailable, explicitly
    state that the finding is cross-sectional and cannot establish that the
    driver caused or contributed to the temporal change.

26. A subgroup's elevated current-period churn rate may support an
    association with current-period churn, but it must not be described as
    an association with the temporal increase in churn unless comparable
    historical subgroup data is available.

27. When comparing numerical values, verify the direction of the comparison
    using the supplied values.

    For example:

    - 8.49% is higher than 4.47%.
    - 3.64% is lower than 4.47%.
    - 3.62% is lower than 4.47%.

    Never describe a value as higher, lower, greater, or smaller when the
    supplied numerical values do not support that comparison.

28. A current-period subgroup rate and an overall quarter-over-quarter
    change measure different things.

    Do not use a subgroup's current-period churn rate to explain the
    magnitude or direction of the overall quarter-over-quarter change
    unless historical subgroup-level evidence is available.

    In particular, do not describe a subgroup as having "contributed to the
    increase" based solely on its current-period churn rate.

29. Do not infer causality from ranking alone.

    A subgroup having the highest observed churn rate does not establish
    that it caused, contributed to, or drove the overall churn increase.

30. Do not use the overall outcome rate as evidence that a subgroup caused
    the outcome.

    The overall rate establishes the observed outcome. It does not by itself
    establish which subgroup or factor produced the change.

31. When evidence is cross-sectional, describe the finding using language
    such as:

    - "shows an observed association with churn"
    - "has the highest observed churn rate"
    - "represents a potential driver"
    - "is associated with higher current-period churn"

    Avoid language implying temporal contribution unless temporal evidence
    is explicitly supplied.

32. Do not manufacture historical comparisons.

    If prior-period subgroup data is not supplied, do not estimate, infer,
    or assume what that subgroup's prior-period churn rate was.

33. If the investigation question contains a numerical claim that conflicts
    with the observed evidence, explicitly acknowledge the discrepancy in
    the limitations.

34. The observed outcome and the explanation for that outcome are separate
    concepts.

    Establishing that churn increased does not establish why it increased.

35. If no potential driver has sufficient evidence, return an empty
    "root_causes" list and explain the insufficiency in "limitations".

Before producing the final JSON, internally perform these steps:

1. Identify the observed outcome.
2. Separate outcome findings from potential driver findings.
3. Extract all relevant numerical values from the supplied evidence.
4. Verify the direction of every numerical comparison.
5. Identify the time period associated with each finding.
6. Determine whether each potential driver is cross-sectional or temporal.
7. Rank potential drivers by strength of evidence.
8. Assess whether the evidence establishes association or causation.
9. Determine whether temporal evidence supports the relationship.
10. Select the strongest supported candidates.
11. Ensure evidence_indices directly support each candidate.
12. Check that no outcome finding has been classified as a root cause.
13. Check that no causal language is used without causal evidence.
14. Record important limitations, including discrepancies between the
    investigation question and observed evidence.
15. Verify that every numerical statement in the final response is supported
    by the supplied evidence.

Return ONLY valid JSON using this structure:

{{
    "root_causes": [
        {{
            "cause": "string",
            "explanation": "string",
            "evidence_indices": [0],
            "confidence": 0.0,
            "causal_status": "supported_association"
        }}
    ],
    "limitations": [
        "string"
    ]
}}

Allowed causal_status values:

- "supported_association"
- "strong_candidate"
- "insufficient_evidence"

Investigation question:
{question}

Investigation findings:
{findings}
"""


def reason_about_root_causes(
    question: str,
    findings: list[InvestigationFinding],
) -> dict:
    llm = get_llm()

    findings_payload = [
        {
            "index": index,
            "cause": finding.cause,
            "explanation": finding.explanation,
            "confidence": finding.confidence,
            "supporting_evidence": [
                {
                    "source": evidence.source,
                    "type": evidence.type,
                    "data": evidence.data,
                    "methodology": evidence.methodology,
                }
                for evidence in finding.supporting_evidence
            ],
        }
        for index, finding in enumerate(findings)
    ]

    prompt = ROOT_CAUSE_PROMPT.format(
        question=question,
        findings=json.dumps(findings_payload, default=str, indent=2),
    )

    response = llm.invoke(prompt)

    content = response.content

    if isinstance(content, list):
        content = "".join(
            item.get("text", "")
            if isinstance(item, dict)
            else str(item)
            for item in content
        )


    return json.loads(content)