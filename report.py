import pandas as pd


def prepare_report(df):
    if df.empty:
        return pd.DataFrame()

    report = df.copy()

    report["transaction_date"] = pd.to_datetime(
        report["transaction_date"]
    ).dt.strftime("%Y-%m-%d")

    return report


def convert_to_csv(df):
    report = prepare_report(df)

    return report.to_csv(index=False).encode("utf-8")