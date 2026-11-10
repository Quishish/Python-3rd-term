import pandas as pd


def get_umbrella_total(filepath: str = "transactions.csv") -> float:
  df = pd.read_csv(filepath)

  umbrella_ok = df[
      (df["STATUS"] == "OK")
      & (df["CONTRACTOR"].str.contains("Umbrella", case=False, na=False))
  ]

  total_sum = umbrella_ok["SUM"].sum()
  return total_sum


if __name__ == "__main__":
  total = get_umbrella_total("transactions.csv")
  print(f"Полная сумма проверенных платежей в адрес Umbrella, Inc.: {total}")