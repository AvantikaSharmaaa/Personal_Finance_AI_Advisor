import pandas as pd


def prepare_monthly_summary(df):
    if df.empty:
        return pd.DataFrame()

    data = df.copy()

    data["transaction_date"] = pd.to_datetime(
        data["transaction_date"]
    )

    data["month"] = (
        data["transaction_date"]
        .dt.to_period("M")
        .astype(str)
    )

    income = (
        data[data["transaction_type"] == "Income"]
        .groupby("month")["amount"]
        .sum()
        .rename("income")
    )

    expenses = (
        data[data["transaction_type"] == "Expense"]
        .groupby("month")["amount"]
        .sum()
        .rename("expenses")
    )

    summary = pd.concat(
        [income, expenses],
        axis=1
    ).fillna(0)

    summary["savings"] = (
        summary["income"] - summary["expenses"]
    )

    return summary.reset_index()


def get_top_categories(df, limit=5):
    if df.empty:
        return pd.DataFrame()

    expenses = df[
        df["transaction_type"] == "Expense"
    ]

    return (
        expenses.groupby("category")["amount"]
        .sum()
        .reset_index()
        .sort_values("amount", ascending=False)
        .head(limit)
    )