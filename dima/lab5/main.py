import numpy as np

def read_matrix_from_file(filename):
    with open(filename, 'r') as file:
        n = int(file.readline().strip())
        A = []
        b = []
        for line in file:
            row = list(map(float, line.split()))
            A.append(row[:-1])
            b.append(row[-1])
    return np.array(A), np.array(b), n

def seidel_method(A, b, epsilon=1e-4, max_iterations=100):
    n = len(A)
    x = np.zeros(n)  # начальное приближение (нулевой вектор)
    
    iterations = 0

    for _ in range(max_iterations):
        x_new = np.copy(x)
        
        for i in range(n):
            sum1 = sum(A[i][j] * x_new[j] for j in range(i))
            sum2 = sum(A[i][j] * x[j] for j in range(i + 1, n))
            x_new[i] = (b[i] - sum1 - sum2) / A[i][i]
        
        # Вычисляем норму разности текущего и предыдущего приближений
        norm = np.linalg.norm(x_new - x, ord=np.inf)
        iterations += 1

        if norm < epsilon:
            print(f"Решение найдено за {iterations} итераций.")
            return x_new, iterations

        x = x_new

    print(f"Метод Зейделя не сошелся за {max_iterations} итераций.")
    return x, iterations

# Пример использования
filename = 'matrix_data.txt'
A, b, n = read_matrix_from_file(filename)

print("Матрица A:")
print(A)
print("Вектор b:")
print(b)

# Проверка на сходимость метода
if not np.all(np.diag(A)):
    print("Матрица имеет нулевые элементы на диагонали. Метод Зейделя может не работать.")
else:
    solution, iterations = seidel_method(A, b)
    print("Решение системы:", solution)
    print("Количество итераций:", iterations)
