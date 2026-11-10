import matplotlib.pyplot as plt
import numpy as np


def filter_signal_data(file_path: str, output_file_path: str):
  data = np.loadtxt(file_path)
  n = len(data)
  filtered_data = np.zeros_like(data)

  window_size = 10

  for i in range(n):
    start_idx = max(0, i - window_size + 1)
    filtered_data[i] = np.mean(data[start_idx : i + 1])

  np.savetxt(output_file_path, filtered_data)
  print(f"Результат успешно сохранен в файл '{output_file_path}'.")

  fig, axes = plt.subplots(1, 2, figsize=(14, 5))

  axes[0].plot(data, color="blue", alpha=0.7)
  axes[0].set_title("Сырой сигнал")
  axes[0].grid(True)

  axes[1].plot(filtered_data, color="crimson")
  axes[1].set_title("После фильтра (скользящее среднее)")
  axes[1].grid(True)

  plt.tight_layout()
  plot_filename = output_file_path.rsplit(".", 1)[0] + "_plot.png"
  plt.savefig(plot_filename)
  print(f"График фильтрации успешно сохранен в '{plot_filename}'.")
  plt.show()

  return filtered_data


if __name__ == "__main__":
  filter_signal_data("signal01.dat", "signal01_filtered.dat")
  filter_signal_data("signal02.dat", "signal02_filtered.dat")
  filter_signal_data("signal03.dat", "signal03_filtered.dat")
  pass