import numpy as np
import matplotlib.pyplot as plt

def f(x):
    return x + 2 * np.sin(x) + np.cos(3 * x)

def f_prime(x):
    return 1 + 2 * np.cos(x) - 3 * np.sin(3 * x)

def f_double_prime(x):
    return -2 * np.sin(x) - 9 * np.cos(3 * x)

def taylor_parabola(x0):
    """Строит параболу на основе ряда Тейлора второго порядка."""
    def parabola(x):
        return f(x0) + f_prime(x0) * (x - x0) + 0.5 * f_double_prime(x0) * (x - x0)**2
    return parabola

def plot_function_with_taylor_parabola(a, b, x0, parabola_fn, iteration):
    x_vals = np.linspace(a, b, 5000)
    y_vals = f(x_vals)

    plt.plot(x_vals, y_vals, label='f(x) = x + 2sin(x) + cos(3x)', color='blue')

    y_parabola = parabola_fn(x_vals)
    plt.plot(x_vals, y_parabola, '--', label=f'Парабола Тейлора на итерации {iteration}', color='orange')

    plt.scatter(x0, f(x0), color='red', label=f'Итерация {iteration}, x0 = {x0:.4f}')

    plt.axhline(0, color='black', linewidth=0.5)
    plt.axvline(0, color='black', linewidth=0.5)

    plt.title('График функции и параболы ряда Тейлора')
    plt.xlabel('x')
    plt.ylabel('f(x)')
    plt.grid(True)
    plt.legend()
    plt.show()

def taylor_method(a, b, eps=1e-4):
    max_iter = 1000

    for k in range(max_iter):
        x0 = (a + b) / 2
        fx0 = f(x0)

        parabola_fn = taylor_parabola(x0)

        print(f"Итерация {k+1}: x0 = {x0:.6f}, f(x0) = {fx0:.6f}, точность = {eps}")
        plot_function_with_taylor_parabola(a, b, x0, parabola_fn, k+1)

        if abs(fx0) < eps:
            print(f"Решение найдено: x = {x0:.6f}, f(x) = {fx0:.6f}, количество итераций = {k+1}, точность = {eps}")
            return x0, k+1

        if np.sign(f(a)) * np.sign(fx0) < 0:
            b = x0
        else:
            a = x0

    print(f"Решение не найдено за {max_iter} итераций, точность = {eps}")
    return None, max_iter

a, b = -5, 5

taylor_method(a, b)
