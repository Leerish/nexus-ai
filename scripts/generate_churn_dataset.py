from pathlib import Path

import numpy as np
import pandas as pd


SEED = 42
N_CUSTOMERS = 1000


def generate_dataset() -> pd.DataFrame:
    rng = np.random.default_rng(SEED)

    segments = rng.choice(
        ["Consumer", "SMB", "Enterprise"],
        size=N_CUSTOMERS,
        p=[0.55, 0.30, 0.15],
    )

    tenure = rng.integers(
        1,
        73,
        size=N_CUSTOMERS,
    )

    monthly_charges = np.round(
        rng.normal(85, 25, N_CUSTOMERS).clip(25, 200),
        2,
    )

    support_tickets = rng.poisson(
        2.5,
        N_CUSTOMERS,
    )

    satisfaction = np.round(
        rng.normal(7.2, 1.5, N_CUSTOMERS).clip(1, 10),
        1,
    )

    product_changes = rng.poisson(
        1.2,
        N_CUSTOMERS,
    )

    # Create a controlled churn relationship.
    churn_score = (
        -1.8
        + 0.28 * support_tickets
        - 0.35 * satisfaction
        + 0.12 * product_changes
        - 0.015 * tenure
        + 0.004 * monthly_charges
    )

    churn_probability = 1 / (
        1 + np.exp(-churn_score)
    )

    churned = rng.binomial(
        1,
        churn_probability,
    )

    return pd.DataFrame(
        {
            "customer_id": [
                f"CUST-{i:05d}"
                for i in range(1, N_CUSTOMERS + 1)
            ],
            "segment": segments,
            "tenure_months": tenure,
            "monthly_charges": monthly_charges,
            "support_tickets": support_tickets,
            "satisfaction_score": satisfaction,
            "product_changes": product_changes,
            "churned": churned,
        }
    )


if __name__ == "__main__":
    output_path = Path(
        "datasets/churn/customers.csv"
    )

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    df = generate_dataset()

    df.to_csv(
        output_path,
        index=False,
    )

    print(f"Generated {len(df)} customers")
    print(f"Saved to {output_path}")