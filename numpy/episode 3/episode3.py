import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np


def simulate_process_to_gif(
    file_path: str, steps: int = 255, gif_name: str = "simulation.gif"
):
  initial_u = np.loadtxt(file_path)
  n = len(initial_u)

  A = np.eye(n) - np.eye(n, k=-1)
  A[0, -1] = -1

  history = [initial_u.copy()]
  u = initial_u.copy()

  for step in range(steps):
    u = u - 0.5 * np.dot(A, u)
    history.append(u.copy())

  fig, ax = plt.subplots(figsize=(10, 6))

  all_vals = np.array(history)
  ymin, ymax = all_vals.min(), all_vals.max()
  ax.set_ylim(ymin - 0.5, ymax + 0.5)
  ax.set_xlim(0, n - 1)

  (line,) = ax.plot([], [], lw=2, color="blue", label="Текущее состояние u(x)")
  ax.plot(
      initial_u,
      color="gray",
      linestyle="--",
      alpha=0.6,
      label="Начальное состояние (n=0)",
  )

  ax.grid(True)
  ax.set_xlabel("x")
  ax.set_ylabel("u(x)")
  ax.legend(loc="upper right")

  title_text = ax.set_title("")

  def init():
    line.set_data([], [])
    title_text.set_text("")
    return line, title_text

  def animate(i):
    line.set_data(range(n), history[i])
    title_text.set_text(
        f"Динамика процесса: шагов {i} из {steps} (файл: {file_path})"
    )
    return line, title_text

  print("Генерация анимации")
  anim = animation.FuncAnimation(
      fig,
      animate,
      init_func=init,
      frames=len(history),
      interval=40,
      blit=True,
  )

  writer = animation.PillowWriter(fps=30)
  anim.save(gif_name, writer=writer)
  plt.close(fig)

  print(f"Анимация успешно сохранена в файл '{gif_name}'.")
  return history[-1]


if __name__ == "__main__":
  simulate_process_to_gif("start.dat", steps=255, gif_name="simulation_result.gif")
  pass