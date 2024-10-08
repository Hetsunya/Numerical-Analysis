import numpy as np
import matplotlib.pyplot as plt

def f(x, y):
    return np.cos(5 * np.sin(0.1 * x) - 3 * np.sin(0.3 * y)) - 0.1

def g(x, y):
    return np.sin(3 * np.cos(0.3 * x) - 5 * np.cos(0.1 * y)) - 0.3

def Phi(x, y):
    return f(x, y)**2 + g(x, y)**2

def gradient(x, y):
    df_dx = 2 * f(x, y) * (-5 * 0.1 * np.cos(5 * np.sin(0.1 * x) - 3 * np.sin(0.3 * y)) * np.cos(0.1 * x) + 3 * 0.3 * np.cos(3 * np.cos(0.3 * x) - 5 * np.cos(0.1 * y)) * np.sin(0.3 * y))
    df_dy = 2 * g(x, y) * (3 * 0.3 * np.sin(3 * np.cos(0.3 * x) - 5 * np.cos(0.1 * y)) * np.cos(0.1 * y) + 5 * 0.1 * np.sin(5 * np.sin(0.1 * x) - 3 * np.sin(0.3 * y)) * np.cos(0.3 * y))
    return np.array([df_dx, df_dy])


def steepest_descent(starting_point, epsilon=1e-4):
    x = np.array(starting_point)
    iterations = 0

    while True:
        grad = gradient(x[0], x[1])
        norm_grad = np.linalg.norm(grad)

        if norm_grad < epsilon:
            break

        # Определение шага (можно использовать фиксированный шаг или адаптивный)
        step_size = 0.01

        x = x - step_size * grad
        iterations += 1

    return x, iterations, Phi(x[0], x[1]), grad


def plot_function():
    x_range = np.linspace(-10, 10, 400)
    y_range = np.linspace(-10, 10, 400)
    X, Y = np.meshgrid(x_range, y_range)
    Z = Phi(X, Y)

    plt.figure(figsize=(10, 7))
    plt.contour(X, Y, Z, levels=50, cmap='viridis')
    plt.colorbar(label='Функция Phi')
    plt.title('Контурный график функции Phi(x, y)')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.grid(True)
    plt.show()

# Пример использования
starting_point = [0, 0]  # Начальная точка
solution, k, f_val, grad_val = steepest_descent(starting_point)

print(f"Решение: x = {solution[0]}, y = {solution[1]}")
print(f"Количество итераций: {k}")
print(f"Функция Phi(x, y) = {f_val}")
print(f"Градиент ∇Phi(x, y) = {grad_val}")

plot_function()
