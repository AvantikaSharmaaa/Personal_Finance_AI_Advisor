from expense_tracker import (
    get_income,
    get_expenses,
    get_balance,
    get_savings_rate,
    category_expenses
)


def generate_insights(df):
    insights = []

    if df.empty:
        return [
            "Add some transactions to receive financial insights."
        ]

    income = get_income(df)
    expenses = get_expenses(df)
    balance = get_balance(df)
    savings_rate = get_savings_rate(df)

    if income == 0:
        insights.append(
            "Add an income transaction to calculate your savings rate."
        )

    if expenses > income and income > 0:
        insights.append(
            "Your recorded expenses are higher than your income."
        )

    elif income > 0 and savings_rate >= 20:
        insights.append(
            f"Your current recorded savings rate is "
            f"{savings_rate:.1f}%."
        )

    elif income > 0:
        insights.append(
            f"Your current recorded savings rate is "
            f"{savings_rate:.1f}%."
        )

    categories = category_expenses(df)

    if not categories.empty:
        top = categories.iloc[0]

        insights.append(
            f"Your largest expense category is "
            f"{top['category']} at ₹{top['amount']:,.2f}."
        )

    if balance < 0:
        insights.append(
            "Your current recorded balance is negative. "
            "Review your largest expense categories."
        )

    return insights