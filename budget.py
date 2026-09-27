import pandas as pd


def calculate_budget_status(transactions, budgets):
    if budgets.empty:
        return pd.DataFrame()

    expenses = transactions[
        transactions["transaction_type"] == "Expense"
    ].copy()

    if expenses.empty:
        budgets = budgets.copy()
        budgets["spent"] = 0
    else:
        expenses["transaction_date"] = pd.to_datetime(
            expenses["transaction_date"]
        )

        expenses["month"] = (
            expenses["transaction_date"]
            .dt.to_period("M")
            .astype(str)
        )

        spending = (
            expenses.groupby(["category", "month"])["amount"]
            .sum()
            .reset_index()
        )

        budgets = budgets.merge(
            spending,
            on=["category", "month"],
            how="left"
        )

        budgets.rename(
            columns={"amount_x": "budget", "amount_y": "spent"},
            inplace=True
        )

        budgets["spent"] = budgets["spent"].fillna(0)

        if "budget" not in budgets.columns:
            budgets["budget"] = budgets["amount"]

    budgets["remaining"] = (
        budgets["budget"] - budgets["spent"]
    )

    budgets["usage_percent"] = (
        budgets["spent"] / budgets["budget"] * 100
    ).round(2)

    return budgets