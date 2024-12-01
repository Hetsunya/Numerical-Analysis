import numpy as np
import matplotlib.pyplot as plt


def f(x):
    return x + 2 * np.sin(x) + np.cos(3 * x)


def f_prime(x):
    return 1 + 2 * np.cos(x) - 3 * np.sin(3 * x)


def f_double_prime(x):
    return -2 * np.sin(x) - 9 * np.cos(3 * x)


def newton_method(x0, epsilon=1e-4, max_iter=100):
    x = x0
    for k in range(max_iter):
        fx_prime = f_prime(x)
        fx_double_prime = f_double_prime(x)
        if abs(fx_prime) < epsilon:
            break
        if fx_double_prime == 0:
            print("Вторая производная равна нулю, метод не применим.")
            return None, k

        x_new = x - fx_prime / fx_double_prime
        if abs(x_new - x) < epsilon:
            return x_new, k + 1, f(x_new), fx_prime
        x = x_new

    return x, max_iter, f(x), fx_prime


x_vals = np.linspace(-10, 10, 1000)
y_vals = f(x_vals)

plt.figure(figsize=(10, 6))
plt.plot(x_vals, y_vals, label="f(x) = x + 2*sin(x) + cos(3*x)")
plt.xlabel("x")
plt.ylabel("f(x)")
plt.title("График функции f(x)")
plt.grid(True)
plt.legend()
plt.show()

x0 = 0.5
epsilon = 1e-4
x_extremum, iterations, f_val, f_prime_val = newton_method(x0, epsilon)

if x_extremum is not None:
    print(f"Найденное значение x(k): {x_extremum}")
    print(f"Количество итераций k: {iterations}")
    print(f"Значение функции f(x(k)): {f_val}")
    print(f"Значение производной f'(x(k)): {f_prime_val}")
    print(f"Точность ε: {epsilon}")
else:
    print("Метод не сошелся.")