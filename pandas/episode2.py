import matplotlib.pyplot as plt
import pandas as pd


def analyze_cargo_flights(filepath: str = "flights.csv") -> pd.DataFrame:

  df = pd.read_csv(filepath)

  grouped = (
      df.groupby("CARGO")
      .agg(
          flight_count=("PRICE", "count"),
          total_price=("PRICE", "sum"),
          total_weight=("WEIGHT", "sum"),
      )
      .reset_index()
  )

  print("Сводная статистика по авиакомпаниям:")
  print(grouped)

  fig, axes = plt.subplots(1, 3, figsize=(18, 5))

  grouped.plot(
      x="CARGO",
      y="flight_count",
      kind="bar",
      ax=axes[0],
      color="skyblue",
      legend=False,
  )
  axes[0].set_title("Количество рейсов")
  axes[0].set_ylabel("Рейсы")
  axes[0].tick_params(axis="x", rotation=45)

  grouped.plot(
      x="CARGO",
      y="total_price",
      kind="bar",
      ax=axes[1],
      color="salmon",
      legend=False,
  )
  axes[1].set_title("Полная стоимость грузов")
  axes[1].set_ylabel("Стоимость")
  axes[1].tick_params(axis="x", rotation=45)

  grouped.plot(
      x="CARGO",
      y="total_weight",
      kind="bar",
      ax=axes[2],
      color="lightgreen",
      legend=False,
  )
  axes[2].set_title("Полная масса грузов")
  axes[2].set_ylabel("Масса")
  axes[2].tick_params(axis="x", rotation=45)

  plt.tight_layout()
  plt.savefig("cargo_analysis.png")
  print("\nГрафик успешно сохранен в файл 'cargo_analysis.png'.")
  plt.show()

  return grouped


if __name__ == "__main__":
  analyze_cargo_flights("flights.csv")