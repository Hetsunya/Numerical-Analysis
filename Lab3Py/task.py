import numpy as np


# Определяем функции системы
def f1(x1, x2):
    return np.cos(5 * np.sin(0.1 * x1) - 3 * np.sin(0.3 * x2)) - 0.1


def f2(x1, x2):
    return np.sin(3 * np.cos(0.3 * x1) - 5 * np.cos(0.1 * x2)) - 0.3


# Функция для вычисления вектора F(x)
def F(x):
    x1, x2 = x
    return np.array([f1(x1, x2), f2(x1, x2)])


# Вычисление численной производной по разностной схеме
def finite_difference_jacobian(x, h=1e-6):
    n = len(x)
    J = np.zeros((n, n))
    f_x = F(x)

    # Вычисляем Якобиан через конечные разности
    for i in range(n):
        x_plus_h = np.copy(x)
        x_plus_h[i] += h
        f_x_plus_h = F(x_plus_h)
        J[:, i] = (f_x_plus_h - f_x) / h

    return J


# Разностный аналог неявного метода Ньютона
def newton_method_finite_diff(x_initial, epsilon=1e-8, max_iter=100):
    x = np.array(x_initial)

    for i in range(max_iter):
        F_val = F(x)

        # Проверяем условие выхода по норме вектора F
        if np.linalg.norm(F_val) < epsilon:
            print(f"Решение: x1 = {x[0]}, x2 = {x[1]}")
            print(f"Количество итераций: {i + 1}")
            return x

        # Вычисляем Якобиан через разностную схему
        J = finite_difference_jacobian(x)

        # Решаем систему линейных уравнений для нахождения поправок Δx
        delta_x = np.linalg.solve(J, -F_val)

        # Обновляем значения x
        x = x + delta_x

    print("Метод не сошелся за максимальное количество итераций.")
    return None


# Пример использования
x1_initial = 0.5
x2_initial = 0.5
newton_method_finite_diff([x1_initial, x2_initial])
