from pathlib import Path

import duckdb

from nexus_core.reasoning.state import Evidence


DATASET_PATH = Path("datasets/churn/customers.csv")

CHURN_BY_SEGMENT_QUERY = """
SELECT
    segment,
    COUNT(*) AS customers,
    AVG(churned) AS churn_rate
FROM read_csv_auto(?)
GROUP BY segment
ORDER BY churn_rate DESC
""".strip()


def analyze_churn_by_segment() -> list[dict]:
    if not DATASET_PATH.exists():
        raise FileNotFoundError(
            f"Dataset not found: {DATASET_PATH}"
        )

    with duckdb.connect() as connection:
        rows = connection.execute(
            CHURN_BY_SEGMENT_QUERY,
            [str(DATASET_PATH)],
        ).fetchall()

    return [
        {
            "segment": row[0],
            "customers": row[1],
            "churn_rate": row[2],
        }
        for row in rows
    ]


def analyze_churn_by_segment_evidence() -> list[Evidence]:
    rows = analyze_churn_by_segment()

    return [
        Evidence(
            source=str(DATASET_PATH),
            type="aggregate",
            data=row,
            query=CHURN_BY_SEGMENT_QUERY,
            methodology=(
                "Churn rate calculated as the mean of the "
                "binary churned indicator grouped by segment."
            ),
        )
        for row in rows
    ]