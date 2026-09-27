import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import date

from database import (
    init_database,
    add_transaction,
    get_transactions,
    delete_transaction,
    add_budget,
    get_budgets,
    delete_budget
)

from expense_tracker import (
    get_income,
    get_expenses,
    get_balance,
    get_savings_rate,
    category_expenses,
    monthly_expenses
)

from budget import calculate_budget_status
from analytics import prepare_monthly_summary
from predictor import predict_next_month_expense
from advisor import generate_insights
from report import convert_to_csv


# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="Personal Finance AI Advisor",
    page_icon="💰",
    layout="wide"
)


# --------------------------------------------------
# DATABASE
# --------------------------------------------------

init_database()


# --------------------------------------------------
# CUSTOM CSS
# --------------------------------------------------

st.markdown("""
<style>

.main {
    background-color: #f7f9fc;
}

.dashboard-card {
    padding: 20px;
    border-radius: 12px;
    background-color: white;
    border: 1px solid #e6e6e6;
    margin-bottom: 15px;
}

.title {
    font-size: 36px;
    font-weight: 700;
}

.subtitle {
    color: #666;
    font-size: 16px;
}

</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

st.sidebar.title("💰 Finance Advisor")

page = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "Add Transaction",
        "Transactions",
        "Budget Manager",
        "Analytics",
        "Smart Advisor"
    ]
)


# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

df = get_transactions()


# --------------------------------------------------
# DASHBOARD
# --------------------------------------------------

if page == "Dashboard":

    st.markdown(
        '<div class="title">💰 Personal Finance AI Advisor</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">'
        'Track your income, expenses, budgets and financial trends.'
        '</div>',
        unsafe_allow_html=True
    )

    st.divider()

    income = get_income(df)
    expenses = get_expenses(df)
    balance = get_balance(df)
    savings_rate = get_savings_rate(df)

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "💵 Total Income",
        f"₹{income:,.2f}"
    )

    col2.metric(
        "💸 Total Expenses",
        f"₹{expenses:,.2f}"
    )

    col3.metric(
        "💰 Balance",
        f"₹{balance:,.2f}"
    )

    col4.metric(
        "📈 Savings Rate",
        f"{savings_rate:.1f}%"
    )

    st.divider()

    if df.empty:

        st.info(
            "No transactions available. "
            "Go to 'Add Transaction' to add your first transaction."
        )

    else:

        col1, col2 = st.columns(2)

        with col1:

            categories = category_expenses(df)

            if not categories.empty:

                fig = px.pie(
                    categories,
                    names="category",
                    values="amount",
                    title="Expense Distribution"
                )

                st.plotly_chart(
                    fig,
                    use_container_width=True
                )

        with col2:

            monthly = monthly_expenses(df)

            if not monthly.empty:

                fig = px.bar(
                    monthly,
                    x="month",
                    y="amount",
                    title="Monthly Expenses"
                )

                st.plotly_chart(
                    fig,
                    use_container_width=True
                )


# --------------------------------------------------
# ADD TRANSACTION
# --------------------------------------------------

elif page == "Add Transaction":

    st.title("➕ Add Transaction")

    transaction_type = st.selectbox(
        "Transaction Type",
        ["Expense", "Income"]
    )

    if transaction_type == "Expense":

        categories = [
            "Food",
            "Shopping",
            "Transport",
            "Education",
            "Entertainment",
            "Bills",
            "Health",
            "Travel",
            "Other"
        ]

    else:

        categories = [
            "Salary",
            "Freelance",
            "Business",
            "Investment",
            "Gift",
            "Other"
        ]

    category = st.selectbox(
        "Category",
        categories
    )

    amount = st.number_input(
        "Amount (₹)",
        min_value=0.01,
        step=100.0
    )

    payment_method = st.selectbox(
        "Payment Method",
        [
            "Cash",
            "UPI",
            "Debit Card",
            "Credit Card",
            "Bank Transfer",
            "Other"
        ]
    )

    description = st.text_input(
        "Description"
    )

    transaction_date = st.date_input(
        "Date",
        value=date.today()
    )

    if st.button(
        "💾 Save Transaction",
        use_container_width=True
    ):

        add_transaction(
            transaction_type,
            category,
            amount,
            payment_method,
            description,
            str(transaction_date)
        )

        st.success(
            "Transaction added successfully!"
        )

        st.rerun()


# --------------------------------------------------
# TRANSACTIONS
# --------------------------------------------------

elif page == "Transactions":

    st.title("📋 Transactions")

    if df.empty:

        st.info("No transactions found.")

    else:

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )

        st.download_button(
            "⬇️ Download Transactions CSV",
            data=convert_to_csv(df),
            file_name="finance_transactions.csv",
            mime="text/csv"
        )

        st.divider()

        st.subheader("🗑️ Delete Transaction")

        transaction_id = st.number_input(
            "Transaction ID",
            min_value=1,
            step=1
        )

        if st.button("Delete Transaction"):

            delete_transaction(transaction_id)

            st.success(
                "Transaction deleted."
            )

            st.rerun()


# --------------------------------------------------
# BUDGET MANAGER
# --------------------------------------------------

elif page == "Budget Manager":

    st.title("🎯 Budget Manager")

    st.subheader("Create / Update Budget")

    budget_categories = [
        "Food",
        "Shopping",
        "Transport",
        "Education",
        "Entertainment",
        "Bills",
        "Health",
        "Travel",
        "Other"
    ]

    category = st.selectbox(
        "Category",
        budget_categories
    )

    amount = st.number_input(
        "Monthly Budget (₹)",
        min_value=1.0,
        step=500.0
    )

    month = st.text_input(
        "Month",
        value=date.today().strftime("%Y-%m")
    )

    if st.button("💾 Save Budget"):

        add_budget(
            category,
            amount,
            month
        )

        st.success(
            "Budget saved successfully."
        )

        st.rerun()

    st.divider()

    budgets = get_budgets()

    if not budgets.empty:

        st.subheader("📊 Budget Status")

        status = calculate_budget_status(
            df,
            budgets
        )

        st.dataframe(
            status,
            use_container_width=True,
            hide_index=True
        )

        st.divider()

        st.subheader("🗑️ Delete Budget")

        budget_id = st.number_input(
            "Budget ID",
            min_value=1,
            step=1
        )

        if st.button("Delete Budget"):

            delete_budget(budget_id)

            st.success(
                "Budget deleted."
            )

            st.rerun()


# --------------------------------------------------
# ANALYTICS
# --------------------------------------------------

elif page == "Analytics":

    st.title("📊 Financial Analytics")

    if df.empty:

        st.info(
            "Add transactions to see analytics."
        )

    else:

        summary = prepare_monthly_summary(df)

        if not summary.empty:

            fig = px.line(
                summary,
                x="month",
                y=["income", "expenses", "savings"],
                markers=True,
                title="Income vs Expenses vs Savings"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        categories = category_expenses(df)

        if not categories.empty:

            fig = px.bar(
                categories,
                x="category",
                y="amount",
                title="Category-wise Expenses"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        st.subheader("📈 Monthly Summary")

        st.dataframe(
            summary,
            use_container_width=True,
            hide_index=True
        )


# --------------------------------------------------
# SMART ADVISOR
# --------------------------------------------------

elif page == "Smart Advisor":

    st.title("🤖 Smart Financial Advisor")

    if df.empty:

        st.info(
            "Add some transactions first."
        )

    else:

        st.subheader("💡 Financial Insights")

        insights = generate_insights(df)

        for insight in insights:

            st.info(
                f"💡 {insight}"
            )

        st.divider()

        st.subheader(
            "🔮 Estimated Next-Month Expenses"
        )

        prediction = predict_next_month_expense(df)

        if prediction is None:

            st.warning(
                "At least two months of expense data "
                "are needed for prediction."
            )

        else:

            st.metric(
                "Estimated Expenses",
                f"₹{prediction:,.2f}"
            )

            st.caption(
                "This is a simple machine-learning estimate "
                "based on your recorded historical expenses."
            )

        st.divider()

        st.subheader("📌 Financial Summary")

        income = get_income(df)
        expenses = get_expenses(df)
        balance = get_balance(df)

        st.write(
            f"**Total Income:** ₹{income:,.2f}"
        )

        st.write(
            f"**Total Expenses:** ₹{expenses:,.2f}"
        )

        st.write(
            f"**Current Balance:** ₹{balance:,.2f}"
        )