from pathlib import Path
import pandas as pd

pd.set_option("display.max_columns", None)
ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = ROOT / "data" / "telco_churn.csv"

def load_raw() -> pd.DataFrame:
    return pd.read_csv(DATA_PATH)

def load_and_clean() -> pd.DataFrame:
    df = load_raw()
    df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")
    # tenure = 0 customers haven't been billed yet, so their true total is $0
    df["TotalCharges"] = df["TotalCharges"].fillna(0)
    df["Churn"] = df["Churn"].map({"Yes": 1, "No": 0})
    return df

if __name__ == "__main__":
    raw = load_raw()
    print(raw.shape)
    print(raw.dtypes)
    print(raw["Churn"].value_counts())

    bad_rows = pd.to_numeric(raw["TotalCharges"], errors="coerce").isna()
    cols = ["customerID", "tenure", "MonthlyCharges", "TotalCharges", "Churn"]
    print(raw.loc[bad_rows, cols])

    df = load_and_clean()
    print("Missing TotalCharges:", df["TotalCharges"].isna().sum())
    print("Duplicate IDs:", df["customerID"].duplicated().sum())
    print(f"Churn rate: {df['Churn'].mean():.1%}")

