from langgraph.graph import END, START, StateGraph

from nexus_core.reasoning.planner import plan_investigation

from nexus_core.reasoning.workers import (
    execute_data_analysis,
    execute_evidence_gathering,
    execute_root_cause,
    execute_temporal_analysis,
)

from nexus_core.reasoning.state import (
    InvestigationState,
    TaskType,
    
)

from nexus_core.reasoning.executor import execute_task , worker_node
from langgraph.types import Send


def planner_node(state: InvestigationState) -> dict:
    tasks = plan_investigation(state["question"])

    return {
        "tasks": tasks,
        "results": [],
    }


def execute_tasks(state: InvestigationState) -> dict:
    results = [
        execute_task(task)
        for task in state["tasks"]
    ]

    return {
        "results": results,
    }

def dispatch_tasks(state: InvestigationState):
    return [
        Send(
            "worker",
            {
                "task": task,
            },
        )
        for task in state["tasks"]
    ]
    

builder = StateGraph(InvestigationState)

builder.add_node("planner", planner_node)
builder.add_node("execute_tasks", execute_tasks)

builder.add_edge(START, "planner")
builder.add_edge("planner", "execute_tasks")
builder.add_edge("execute_tasks", END)
builder.add_node("worker", worker_node)

investigation_graph = builder.compile()