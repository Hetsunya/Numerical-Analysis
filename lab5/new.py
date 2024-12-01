import numpy as np

#ХЗ ЧТО ЗДЕСЬ ВООБЩЕ

# Функция для вычисления ошибки между векторами решений
def error_calc(X, xn):
    # Вычисляем норму разности между предыдущим и текущим векторами
    return np.linalg.norm(np.array(X[-1]) - np.array(xn), ord=np.inf)


# Метод релаксаций
def relax(A, B, start=0, eps=0.1, omega=0.1):
    n = len(A)
    if start == 0 or len(start) != n:
        start = [0] * n  # Начальное приближение по умолчанию

    X = []  # Список решений на каждом шаге
    X.append(start)  # Добавляем начальное приближение
    error = float('inf')
    xn = [0] * n  # Вектор решения
    k = 0  # Счётчик итераций

    while error > eps:
        k += 1
        x = X[-1]  # Предыдущее решение
        xc = x.copy()  # Копия для расчетов

        for j in range(n):
            # Вычисляем новое значение для xn[j] по формуле релаксаций
            xn[j] = (1 / float(A[j][j])) * (B[j] - sum(A[j][i] * xc[i] for i in range(n) if i != j))
            xc[j] = xn[j]  # Обновляем копию

        # Обновляем решения с учетом релаксации
        for j in range(n):
            xn[j] = omega * xn[j] + (1 - omega) * x[j]

        X.append(xn.copy())  # Добавляем новое решение в список
        error = error_calc(X, xn)  # Рассчитываем ошибку
        if error > 10000 or k == 1000:
            raise RuntimeError('Итерации не сходятся!')

    return X, k  # Возвращаем список решений и количество итераций

# Пример использования метода с матрицей A и вектором B
A = np.array([
    [-1.0, 1.5, 2.25],
    [-3.0, 4.0, 2.0],
    [-6.0, 2.0, 7.0]
])

B = np.array([10.5, 10.0, 2.0])

# Решение с методом релаксаций
X, iterations = relax(A, B, eps=1e-6, omega=0.1)

# Выводим решения и количество итераций
print(f"Решение после {iterations} итераций:")
for i, x in enumerate(X):
    print(f"Шаг {i}: x = {x}")
