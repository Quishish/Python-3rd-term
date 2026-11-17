import numpy as np
import sympy as sp
import matplotlib.pyplot as plt
from scipy import integrate


x = sp.symbols("x")
y = sp.Function("y")
equation = sp.Eq(sp.diff(y(x), x), -2 * y(x))
solution = sp.dsolve(equation, ics={y(0): sp.sqrt(2)})
print("SymPy solution:", solution)

t = np.linspace(0, 10, 300)
exact = sp.lambdify(x, solution.rhs, "numpy")(t)
numeric = integrate.solve_ivp(
    lambda t, y: -2 * y,
    (0, 10),
    [np.sqrt(2)],
    t_eval=t,
    rtol=1e-9,
    atol=1e-12,
).y[0]

fig, axs = plt.subplots(nrows=2, ncols=1, figsize=(8, 7))
axs[0].plot(t, exact, label="SymPy")
axs[0].plot(t, numeric, "--", label="SciPy")
axs[0].set_title("Solutions")
axs[0].legend()
axs[0].grid(True)

axs[1].plot(t, exact - numeric)
axs[1].set_title("Difference")
axs[1].set_xlabel("x")
axs[1].grid(True)

plt.tight_layout()
plt.show()