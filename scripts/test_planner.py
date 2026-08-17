from nexus_core.reasoning.graph import investigation_graph


if __name__ == "__main__":
    result = investigation_graph.invoke(
        {
            "investigation_id": "test",
            "question": "Why did customer churn increase by 18% this quarter?",
            "tasks": [],
            "results": [],
        }
    )

    print("\nFINAL STATE")
    print(result)