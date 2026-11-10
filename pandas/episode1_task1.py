import pandas as pd


def get_top_ok_payments(filepath: str = "transactions.csv") -> pd.DataFrame:
  df = pd.read_csv(filepath)

  ok_payments = df[df["STATUS"] == "OK"]

  top3 = ok_payments.sort_values(by="SUM", ascending=False).head(3)

  return top3


if __name__ == "__main__":
  top3_df = get_top_ok_payments("transactions.csv")
  print("Топ-3 самых крупных реально проведённых платежа:")
  print(top3_df)