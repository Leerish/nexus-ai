from pathlib import Path

import duckdb

from nexus_core.reasoning.state import Evidence


DATASET_PATH = Path("datasets/churn/customers.csv")

CHURN_BY_SATISFACTION_QUERY = """
SELECT
    CASE
        WHEN satisfaction_score <= 3 THEN 'low'
        WHEN satisfaction_score <= 6 THEN 'medium'
        WHEN satisfaction_score <= 8 THEN 'high'
        ELSE 'very_high'
    END AS satisfaction_band,
    COUNT(*) AS customers,
    SUM(churned) AS churned_customers,
    AVG(churned) AS churn_rate
FROM read_csv_auto(?)
GROUP BY satisfaction_band
ORDER BY
    CASE satisfaction_band
        WHEN 'low' THEN 1
        WHEN 'medium' THEN 2
        WHEN 'high' THEN 3
        WHEN 'very_high' THEN 4
    END
""".strip()


def analyze_churn_by_satisfaction() -> list[dict]:
    if not DATASET_PATH.exists():
        raise FileNotFoundError(
            f"Dataset not found: {DATASET_PATH}"
        )

    with duckdb.connect() as connection:
        rows = connection.execute(
            CHURN_BY_SATISFACTION_QUERY,
            [str(DATASET_PATH)],
        ).fetchall()

    return [
        {
            "satisfaction_band": row[0],
            "customers": row[1],
            "churned_customers": row[2],
            "churn_rate": row[3],
        }
        for row in rows
    ]


def analyze_churn_by_satisfaction_evidence() -> list[Evidence]:
    rows = analyze_churn_by_satisfaction()

    return [
        Evidence(
            source=str(DATASET_PATH),
            type="satisfaction_churn_analysis",
            data=row,
            query=CHURN_BY_SATISFACTION_QUERY,
            methodology=(
                "Customers were grouped into satisfaction bands "
                "based on satisfaction_score. Churn rate was "
                "calculated as the mean of the binary churned "
                "indicator within each band."
            ),
        )
        for row in rows
    ]