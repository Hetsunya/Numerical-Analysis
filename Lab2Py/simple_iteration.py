import math
from graph_library import GraphPlotter  # Импортируем библиотеку для работы с графиками


def g(x):
    return math.cos(math.sqrt(abs(x)))


def simple_iteration_method(g, x0, epsilon=1e-4, max_iter=1000):
    x_k = x0
    for k in range(max_iter):
        x_next = g(x_k)
        # Проверка на достижение точности
        if abs(x_next - x_k) < epsilon:
            print(f"Решение: x = {x_next}")
            print(f"Количество итераций: {k + 1}")
            print(f"Значение f(x): {g(x_next) - x_next}")
            return x_next
        x_k = x_next

    print("Метод не сошелся за максимальное количество итераций.")
    return None


def plot_function_and_solution(ax, func, start, end, solution):
    import numpy as np

    # Создаём массив значений x
    x = np.linspace(start, end, 400)

    # Вычисляем y на основе переданной функции
    y = func(x)

    # Отображаем график функции
    ax.plot(x, y, label=f'f(x)')

    # Линия оси Y
    ax.axhline(0, color='black', linewidth=0.5)

    # Линия найденного решения
    ax.axvline(solution, color='r', linestyle='--', label=f'Найденное решение: x = {solution:.5f}')

    ax.legend()


