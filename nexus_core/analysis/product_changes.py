from pathlib import Path

import duckdb

from nexus_core.reasoning.state import Evidence


DATASET_PATH = Path("datasets/churn/customers.csv")

CHURN_BY_PRODUCT_CHANGES_QUERY = """
SELECT
    CASE
        WHEN product_changes = 0 THEN 'none'
        WHEN product_changes = 1 THEN 'one'
        ELSE 'multiple'
    END AS product_change_band,
    COUNT(*) AS customers,
    SUM(churned) AS churned_customers,
    AVG(churned) AS churn_rate
FROM read_csv_auto(?)
GROUP BY product_change_band
ORDER BY
    CASE product_change_band
        WHEN 'none' THEN 1
        WHEN 'one' THEN 2
        WHEN 'multiple' THEN 3
    END
""".strip()


def analyze_churn_by_product_changes() -> list[dict]:
    if not DATASET_PATH.exists():
        raise FileNotFoundError(
            f"Dataset not found: {DATASET_PATH}"
        )

    with duckdb.connect() as connection:
        rows = connection.execute(
            CHURN_BY_PRODUCT_CHANGES_QUERY,
            [str(DATASET_PATH)],
        ).fetchall()

    return [
        {
            "product_change_band": row[0],
            "customers": row[1],
            "churned_customers": row[2],
            "churn_rate": row[3],
        }
        for row in rows
    ]


def analyze_churn_by_product_changes_evidence() -> list[Evidence]:
    rows = analyze_churn_by_product_changes()

    return [
        Evidence(
            source=str(DATASET_PATH),
            type="product_change_churn_analysis",
            data=row,
            query=CHURN_BY_PRODUCT_CHANGES_QUERY,
            methodology=(
                "Customers were grouped by the number of product "
                "changes. Customers with zero changes, one change, "
                "and multiple changes were compared using their "
                "observed churn rates."
            ),
        )
        for row in rows
    ]