import numpy as np
import matplotlib.pyplot as plt

# Определение функции и её производных
def compute_function(x):
    return np.cos(np.sqrt(np.abs(x))) - x

def exact_first_derivative(x):
    sqrt_abs_value = np.sqrt(np.abs(x))
    return (-np.sin(sqrt_abs_value) / (2 * sqrt_abs_value)) * np.sign(x) - 1


# Численные методы вычисления первой производной
def numerical_derivative_2nd_order(func, x, h):
    return (func(x + h) - func(x - h)) / (2 * h)

def numerical_derivative_4th_order(func, x, h):
    return (-func(x + 2 * h) + 8 * func(x + h) - 8 * func(x - h) + func(x - 2 * h)) / (12 * h)

# Метод Рунге для оценки погрешности
def runge_estimation(result_1, result_2, accuracy_order):
    return abs(result_1 - result_2) / (2 ** accuracy_order - 1)

x = 1
h = [0.1, 0.01, 0.025]
x_range = np.linspace(-3, 3, 100000)

# Визуализация функции и её производной
plt.figure(figsize=(10, 6))
plt.plot(x_range, compute_function(x_range), label="f(x)")
plt.plot(x_range, exact_first_derivative(x_range), label="Точная f'(x)", color='orange')
plt.title("Функция и первая производная")
plt.xlabel("x")
plt.ylabel("Значение")
plt.legend()
plt.grid()
plt.show()

results_log = []

# Логирование результатов
def log_results(x, label):
    for step in h:
        second_order_result = numerical_derivative_2nd_order(compute_function, x, step)
        refined_second_order_result = numerical_derivative_2nd_order(compute_function, x, step / 2)
        error_2nd = runge_estimation(second_order_result, refined_second_order_result, 2)

        fourth_order_result = numerical_derivative_4th_order(compute_function, x, step)
        refined_fourth_order_result = numerical_derivative_4th_order(compute_function, x, step / 2)
        error_4th = runge_estimation(fourth_order_result, refined_fourth_order_result, 4)

        exact_value = exact_first_derivative(x)

        results_log.append(f"Точка: {label}, шаг: {step}")
        results_log.append(f"2-й порядок: f'(x) = {second_order_result}, ошибка Рунге = {error_2nd}")
        results_log.append(f"4-й порядок: f'(x) = {fourth_order_result}, ошибка Рунге = {error_4th}")
        results_log.append(f"Точное значение: f'(x) = {exact_value}")
        results_log.append("-")

log_results(x, "x~")
print("\n".join(results_log))

# Сравнение численных и точных значений
plt.figure(figsize=(10, 6))
plt.plot(x_range, exact_first_derivative(x_range), label="Точная f'(x)", color='orange')

for step in h:
    second_order_value = numerical_derivative_2nd_order(compute_function, x, step)
    fourth_order_value = numerical_derivative_4th_order(compute_function, x, step)
    plt.scatter([x], [second_order_value], label=f"2-й порядок, шаг={step}", marker='o', zorder=5)
    plt.scatter([x], [fourth_order_value], label=f"4-й порядок, шаг={step}", marker='s', zorder=5)

plt.title("Сравнение точной и численных производных")
plt.xlabel("x")
plt.ylabel("Значение")
plt.legend()
plt.grid()
plt.show()