import pandas as pd


def get_income(df):
    if df.empty:
        return 0

    return df.loc[
        df["transaction_type"] == "Income",
        "amount"
    ].sum()


def get_expenses(df):
    if df.empty:
        return 0

    return df.loc[
        df["transaction_type"] == "Expense",
        "amount"
    ].sum()


def get_balance(df):
    return get_income(df) - get_expenses(df)


def get_savings_rate(df):
    income = get_income(df)
    expenses = get_expenses(df)

    if income == 0:
        return 0

    return ((income - expenses) / income) * 100


def category_expenses(df):
    if df.empty:
        return pd.DataFrame()

    expenses = df[df["transaction_type"] == "Expense"]

    if expenses.empty:
        return pd.DataFrame()

    return (
        expenses.groupby("category")["amount"]
        .sum()
        .reset_index()
        .sort_values("amount", ascending=False)
    )


def monthly_expenses(df):
    if df.empty:
        return pd.DataFrame()

    expenses = df[df["transaction_type"] == "Expense"].copy()

    if expenses.empty:
        return pd.DataFrame()

    expenses["transaction_date"] = pd.to_datetime(
        expenses["transaction_date"]
    )

    expenses["month"] = (
        expenses["transaction_date"]
        .dt.to_period("M")
        .astype(str)
    )

    return (
        expenses.groupby("month")["amount"]
        .sum()
        .reset_index()
    )