import numpy as np
import matplotlib.pyplot as plt


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
def newton_method_finite_diff(x_initial, epsilon=1e-6, max_iter=100):
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


# Функция для визуализации
def plot_solution_and_functions(x1_sol, x2_sol):
    # Определяем диапазон для x1 и x2, зависящий от решения
    x1_range = np.linspace(-abs(x1_sol) - 5, abs(x1_sol) + 5, 400)
    x2_range = np.linspace(-abs(x2_sol) - 5, abs(x2_sol) + 5, 400)

    X1, X2 = np.meshgrid(x1_range, x2_range)

    F1 = np.cos(5 * np.sin(0.1 * X1) - 3 * np.sin(0.3 * X2)) - 0.1
    F2 = np.sin(3 * np.cos(0.3 * X1) - 5 * np.cos(0.1 * X2)) - 0.3

    plt.ion()  # Включаем интерактивный режим
    fig, ax = plt.subplots(figsize=(8, 8))

    # Построение линий уровня для f1 и f2
    contour_f1 = ax.contour(X1, X2, F1, levels=[0], colors='red', linewidths=2)
    contour_f2 = ax.contour(X1, X2, F2, levels=[0], colors='blue', linewidths=2)

    # Добавляем точку решения
    ax.scatter([x1_sol], [x2_sol], color='green', zorder=5)

    # Добавление легенды вручную
    ax.plot([], [], color='red', label='f1 = 0')
    ax.plot([], [], color='blue', label='f2 = 0')
    ax.scatter([], [], color='green', label='Solution')

    ax.set_xlabel('x1')
    ax.set_ylabel('x2')
    ax.set_title('Графическое решение системы уравнений')
    ax.legend()
    ax.grid(True)

    # Активируем интерактивное управление масштабом
    plt.tight_layout()
    plt.show()


# Пример использования
x1_initial = 1
x2_initial = -0.9
solution = newton_method_finite_diff([x1_initial, x2_initial])

if solution is not None:
    plot_solution_and_functions(solution[0], solution[1])

input("Press Enter to exit...")