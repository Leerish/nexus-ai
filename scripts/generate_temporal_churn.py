from pathlib import Path

import numpy as np
import pandas as pd


SEED = 42
rng = np.random.default_rng(SEED)

BASE_DIR = Path("datasets/churn")
SOURCE_PATH = BASE_DIR / "customers.csv"
OUTPUT_PATH = BASE_DIR / "customer_observations.csv"

BASE_DIR.mkdir(parents=True, exist_ok=True)

customers = pd.read_csv(SOURCE_PATH)

# Four quarterly observation periods.
quarters = pd.to_datetime(
    [
        "2025-01-15",
        "2025-04-15",
        "2025-07-15",
        "2025-10-15",
    ]
)

records = []

for _, customer in customers.iterrows():
    customer_id = customer["customer_id"]

    # Customers are observed until they churn.
    active = True

    satisfaction = float(customer["satisfaction_score"])
    product_changes = int(customer["product_changes"])
    tenure = int(customer["tenure_months"])
    monthly_charges = float(customer["monthly_charges"])

    for quarter_index, observation_date in enumerate(quarters):

        if not active:
            break

        # Customer tenure increases every quarter.
        if quarter_index > 0:
            tenure += 3

        # Satisfaction changes gradually over time.
        satisfaction_change = rng.normal(0, 0.35)

        # Introduce a modest Q4 deterioration.
        if quarter_index == 3:
            satisfaction_change -= 0.25

        satisfaction = np.clip(
            satisfaction + satisfaction_change,
            2.7,
            10.0,
        )

        # Support activity increases slightly when satisfaction drops.
        base_support = max(
            0,
            int(round(customer["support_tickets"] + rng.normal(0, 1)))
        )

        if satisfaction < 6:
            base_support += 1

        support_tickets = max(0, base_support)

        # Product changes can accumulate.
        if rng.random() < 0.25:
            product_changes += 1

        product_changes = min(product_changes, 6)

        # Base churn probability.
        churn_probability = 0.025

        # Segment effect.
        if customer["segment"] == "SMB":
            churn_probability += 0.007
        elif customer["segment"] == "Enterprise":
            churn_probability -= 0.003

        # Satisfaction effect.
        if satisfaction <= 6:
            churn_probability += 0.025
        elif satisfaction <= 8:
            churn_probability += 0.005
        else:
            churn_probability -= 0.008

        # Product-change effect.
        if product_changes >= 2:
            churn_probability += 0.008
        # Q4 target: approximately 18% higher churn than Q3.
        # We use a calibrated uplift at the individual hazard level.
        if quarter_index == 3:
            churn_probability *= 1.07

        churn_probability = float(
            np.clip(churn_probability, 0.001, 0.50)
        )

        churned = int(rng.random() < churn_probability)

        records.append(
            {
                "customer_id": customer_id,
                "observation_date": observation_date,
                "segment": customer["segment"],
                "tenure_months": tenure,
                "monthly_charges": monthly_charges,
                "support_tickets": support_tickets,
                "satisfaction_score": round(satisfaction, 2),
                "product_changes": product_changes,
                "churned": churned,
            }
        )

        if churned:
            active = False


observations = pd.DataFrame(records)

observations.to_csv(
    OUTPUT_PATH,
    index=False,
)

print(f"Created: {OUTPUT_PATH}")
print(f"Rows: {len(observations)}")
print(f"Customers: {observations['customer_id'].nunique()}")

print("\nChurn by quarter:")

quarter_summary = (
    observations.assign(
        quarter=observations["observation_date"].dt.to_period("Q")
    )
    .groupby("quarter")
    .agg(
        customers=("customer_id", "count"),
        churned=("churned", "sum"),
        churn_rate=("churned", "mean"),
    )
)

print(quarter_summary)

print("\nQuarter-over-quarter change:")

quarter_summary["qoq_change"] = (
    quarter_summary["churn_rate"].pct_change() * 100
)

print(quarter_summary)