from langgraph.graph import END, START, StateGraph

from nexus_core.reasoning.planner import plan_investigation
from nexus_core.reasoning.executor import execute_task

from nexus_core.reasoning.evidence import collect_evidence
from nexus_core.reasoning.synthesis import synthesize_evidence
from nexus_core.reasoning.root_cause import reason_about_root_causes

from nexus_core.reasoning.state import (
    InvestigationState,
    InvestigationConclusion,
    RootCauseAnalysis,
)
from nexus_core.reasoning.claim_validation import (
    validate_churn_claim,
)

from nexus_core.reasoning.report import build_investigation_report


def planner_node(state: InvestigationState) -> dict:
    tasks = plan_investigation(state["question"])

    return {
        "tasks": tasks,
        "results": [],
        "conclusion": None,
        "root_cause_analysis": None,
    }


def execute_tasks(state: InvestigationState) -> dict:
    results = [
        execute_task(task)
        for task in state["tasks"]
    ]

    return {
        "results": results,
    }


def synthesis_node(state: InvestigationState) -> dict:
    evidence = collect_evidence(state["results"])

    findings = synthesize_evidence(evidence)

    return {
        "conclusion": InvestigationConclusion(
            summary="Evidence synthesis completed.",
            findings=findings,
        )
    }


def root_cause_node(state: InvestigationState) -> dict:
    conclusion = state["conclusion"]

    if conclusion is None:
        raise ValueError(
            "Cannot perform root-cause analysis without a conclusion."
        )

    raw_analysis = reason_about_root_causes(
        question=state["question"],
        findings=conclusion.findings,
    )

    analysis = RootCauseAnalysis.model_validate(
        raw_analysis
    )

    return {
        "root_cause_analysis": analysis,
    }

def claim_validation_node(state: InvestigationState) -> dict:
    evidence = collect_evidence(state["results"])

    claim_assessment = validate_churn_claim(
        question=state["question"],
        evidence=evidence,
    )

    conclusion = state["conclusion"]

    if conclusion is None:
        raise ValueError(
            "Investigation conclusion is required before claim validation."
        )

    conclusion.claim_assessment = claim_assessment

    return {
        "conclusion": conclusion,
    }
    
def report_node(state: InvestigationState) -> dict:
    report = build_investigation_report(state)

    return {
        "report": report,
    }
    

builder = StateGraph(InvestigationState)

builder.add_node("planner", planner_node)
builder.add_node("execute_tasks", execute_tasks)
builder.add_node("synthesis", synthesis_node)
builder.add_node("claim_validation", claim_validation_node)
builder.add_node("root_cause", root_cause_node)
builder.add_node("report", report_node)

builder.add_edge(START, "planner")
builder.add_edge("planner", "execute_tasks")
builder.add_edge("execute_tasks", "synthesis")
builder.add_edge("synthesis", "claim_validation")
builder.add_edge("claim_validation", "root_cause")
builder.add_edge("root_cause", "report")
builder.add_edge("report", END)

investigation_graph = builder.compile()