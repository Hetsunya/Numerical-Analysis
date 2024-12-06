import numpy as np
import matplotlib.pyplot as plt

def f(x):
    return x + 2 * np.sin(x) + np.cos(3 * x)

def analytical_second_derivative(x):
    return -2 * np.sin(x) - 9 * np.cos(3 * x)

def second_derivative_2nd_order(f, x, h):
    return (f(x + h) - 2 * f(x) + f(x - h)) / h**2

def second_derivative_4th_order(f, x, h):
    return (-f(x + 2 * h) + 16 * f(x + h) - 30 * f(x) + 16 * f(x - h) - f(x - 2 * h)) / (12 * h**2)

def runge_correction(value_h, value_h2, p):
    return abs(value_h - value_h2) / (2**p - 1)

experiments = [
    {"x_tilde": np.pi / 4, "h": 0.1},
    {"x_tilde": np.pi / 2, "h": 0.05},
    {"x_tilde": np.pi, "h": 0.2}
]

x_values = np.linspace(-5 * np.pi, 5 * np.pi, 1000)  # Точки для построения графиков
f_values = f(x_values)
analytical_values = analytical_second_derivative(x_values)

x_tilde_points = []
for exp in experiments:
    x_tilde = exp["x_tilde"]
    h = exp["h"]

    numerical_2nd = second_derivative_2nd_order(f, x_tilde, h)
    numerical_2nd_h2 = second_derivative_2nd_order(f, x_tilde, h / 2)
    error_2nd = runge_correction(numerical_2nd, numerical_2nd_h2, 2)

    numerical_4th = second_derivative_4th_order(f, x_tilde, h)
    numerical_4th_h2 = second_derivative_4th_order(f, x_tilde, h / 2)
    error_4th = runge_correction(numerical_4th, numerical_4th_h2, 4)

    analytical_value = analytical_second_derivative(x_tilde)

    print(f"\nЭксперимент для x_tilde = {x_tilde}, h = {h}:")
    print(f"  Аналитическое значение: {analytical_value}")
    print(f"  Численное значение (2-й порядок): {numerical_2nd}")
    print(f"  Оценка погрешности (2-й порядок): {error_2nd}")
    print(f"  Численное значение (4-й порядок): {numerical_4th}")
    print(f"  Оценка погрешности (4-й порядок): {error_4th}")

    x_tilde_points.append((x_tilde, analytical_value))

plt.figure(figsize=(10, 6))
plt.plot(x_values, f_values, label="f(x)", color="blue")
plt.plot(x_values, analytical_values, label="Аналитическая вторая производная", color="red")

for x_tilde, value in x_tilde_points:
    plt.scatter(x_tilde, value, color="green", zorder=5, label=f"x_tilde={x_tilde:.2f}")
    plt.text(x_tilde, value, f"({x_tilde:.2f}, {value:.2f})", color="green", fontsize=9, ha='right')

plt.title("График функции и её второй производной")
plt.xlabel("x")
plt.ylabel("y")
plt.legend()
plt.grid()
plt.show()