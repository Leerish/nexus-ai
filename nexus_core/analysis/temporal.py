from pathlib import Path

import duckdb

from nexus_core.reasoning.state import Evidence


DATASET_PATH = Path(
    "datasets/churn/customer_observations.csv"
)


QUARTERLY_CHURN_QUERY = """
SELECT
    date_trunc('quarter', observation_date) AS quarter,
    COUNT(*) AS customers,
    SUM(churned) AS churned_customers,
    AVG(churned) AS churn_rate
FROM read_csv_auto(?)
GROUP BY quarter
ORDER BY quarter
""".strip()


def analyze_churn_by_quarter() -> list[dict]:
    if not DATASET_PATH.exists():
        raise FileNotFoundError(
            f"Dataset not found: {DATASET_PATH}"
        )

    with duckdb.connect() as connection:
        rows = connection.execute(
            QUARTERLY_CHURN_QUERY,
            [str(DATASET_PATH)],
        ).fetchall()

    return [
        {
            "quarter": row[0],
            "customers": row[1],
            "churned_customers": row[2],
            "churn_rate": row[3],
        }
        for row in rows
    ]


def analyze_churn_by_quarter_evidence() -> list[Evidence]:
    quarterly_data = analyze_churn_by_quarter()

    evidence = [
        Evidence(
            source=str(DATASET_PATH),
            type="quarterly_churn_analysis",
            data=row,
            query=QUARTERLY_CHURN_QUERY,
            methodology=(
                "Quarterly churn rate was calculated as the "
                "mean of the binary churned indicator for "
                "customers observed during each quarter."
            ),
        )
        for row in quarterly_data
    ]

    if len(quarterly_data) >= 2:
        previous = quarterly_data[-2]
        current = quarterly_data[-1]

        previous_rate = previous["churn_rate"]
        current_rate = current["churn_rate"]

        if previous_rate == 0:
            relative_change = None
        else:
            relative_change = (
                (current_rate - previous_rate)
                / previous_rate
            )

        evidence.append(
            Evidence(
                source=str(DATASET_PATH),
                type="quarter_over_quarter_change",
                data={
                    "previous_quarter": previous["quarter"],
                    "current_quarter": current["quarter"],
                    "previous_churn_rate": previous_rate,
                    "current_churn_rate": current_rate,
                    "relative_change": relative_change,
                },
                query=QUARTERLY_CHURN_QUERY,
                methodology=(
                    "The quarter-over-quarter churn change was "
                    "calculated as the relative difference between "
                    "the current quarter churn rate and the previous "
                    "quarter churn rate."
                ),
            )
        )

    return evidence