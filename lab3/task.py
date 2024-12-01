import numpy as np
import matplotlib.pyplot as plt

# Функция f(x)
def f(x):
    return np.cos(np.sqrt(np.abs(x))) - x

# Численная первая производная (разностный аналог)
def f_prime_numeric(x, h=1e-5):
    return (f(x + h) - f(x - h)) / (2 * h)

# Численная вторая производная (разностный аналог)
def f_double_prime_numeric(x, h=1e-5):
    return (f(x + h) - 2 * f(x) + f(x - h)) / (h**2)

# Метод Ньютона с численными производными
def newton_method_numeric(x0, epsilon=1e-4, max_iter=100):
    x = x0
    for k in range(max_iter):
        fx_prime = f_prime_numeric(x)
        fx_double_prime = f_double_prime_numeric(x)

        # Проверка на малое значение производной
        if abs(fx_prime) < epsilon:
            break

        # Проверка на деление на ноль
        if fx_double_prime == 0:
            print("Вторая производная равна нулю, метод не применим.")
            return None, k

        # Итерационное обновление
        x_new = x - fx_prime / fx_double_prime
        print(f"Итерация {k+1}: x = {x_new:.6f}, f(x) = {f(x_new):.6f}")

        # Проверка критерия сходимости
        if abs(x_new - x) < epsilon:
            return x_new, k + 1, f(x_new), fx_prime

        x = x_new

    return x, max_iter, f(x), fx_prime

# График функции
x_vals = np.linspace(-10, 10, 1000)
y_vals = f(x_vals)

plt.figure(figsize=(10, 6))
plt.plot(x_vals, y_vals, label="f(x) = cos(sqrt(|x|)) - x")
plt.axhline(0, color='black', linestyle='--', linewidth=0.5)
plt.axvline(0, color='black', linestyle='--', linewidth=0.5)
plt.xlabel("x")
plt.ylabel("f(x)")
plt.title("График функции f(x)")
plt.grid(True)
plt.legend()
plt.show()

# Запуск метода Ньютона
x0 = 0.5  # Начальная точка
epsilon = 1e-4
result = newton_method_numeric(x0, epsilon)

# Вывод результата
if result[0] is not None:
    x_extremum, iterations, f_val, f_prime_val = result
    print(f"Найденное значение x(k): {x_extremum}")
    print(f"Количество итераций k: {iterations}")
    print(f"Значение функции f(x(k)): {f_val}")
    print(f"Значение производной f'(x(k)): {f_prime_val}")
    print(f"Точность ε: {epsilon}")
else:
    print("Метод не сошелся.")
