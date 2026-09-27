import pandas as pd
from sklearn.linear_model import LinearRegression


def predict_next_month_expense(df):
    if df.empty:
        return None

    expenses = df[
        df["transaction_type"] == "Expense"
    ].copy()

    if expenses.empty:
        return None

    expenses["transaction_date"] = pd.to_datetime(
        expenses["transaction_date"]
    )

    expenses["month"] = (
        expenses["transaction_date"]
        .dt.to_period("M")
        .astype(str)
    )

    monthly = (
        expenses.groupby("month")["amount"]
        .sum()
        .reset_index()
    )

    if len(monthly) < 2:
        return None

    monthly["month_number"] = range(1, len(monthly) + 1)

    X = monthly[["month_number"]]
    y = monthly["amount"]

    model = LinearRegression()

    model.fit(X, y)

    next_month = [[len(monthly) + 1]]

    prediction = model.predict(next_month)[0]

    return max(0, float(prediction))