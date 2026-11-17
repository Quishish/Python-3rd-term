import os
import numpy as np
import matplotlib.pyplot as plt
from scipy import linalg


fig, axs = plt.subplots(nrows=2, ncols=1, figsize=(11, 7))
for i, name in enumerate(["small", "large"]):
    path = f"data/{name}.txt" if os.path.exists(f"data/{name}.txt") else f"{name}.txt"
    with open(path, "r") as file:
        n = int(file.readline())
        data = np.loadtxt(file)
    A = data[:n]
    b = data[n]
    x = linalg.solve(A, b)
    print(f"{name} result:")
    print(x)
    axs[i].bar(range(n), x)
    axs[i].set_title(f"{name} system")
    axs[i].set_xlabel("Variable number")
    axs[i].set_ylabel("Value")
    axs[i].grid(True, axis="y")
    axs[i].set_axisbelow(True)

plt.tight_layout()
plt.show()