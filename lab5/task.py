import numpy as np


def read_data_from_file(filename):
    """Читает матрицу A из текстового файла, игнорируя вектор b."""
    with open(filename, 'r') as file:
        lines = file.readlines()
    n = int(lines[0].strip())
    A = []
    for line in lines[1:]:
        data = list(map(float, line.split()))
        A.append(data[:-1])  # Все элементы, кроме последнего (свободного члена)
    return np.array(A), n


def relaxation_method(A, n, epsilon=1e-7, omega=0.5, max_iter=3000):
    """Решает СЛАУ методом релаксаций, игнорируя свободные члены."""
    x = np.zeros(n)  # Начальное приближение
    iteration_count = 0

    while iteration_count < max_iter:
        x_new = np.copy(x)
        for i in range(n):
            sigma = np.dot(A[i], x) - A[i][i] * x[i]
            x_new[i] = (1 - omega) * x[i] + omega * (-sigma) / A[i][i]

        # Вычисляем норму разности
        norm = np.linalg.norm(x_new - x, ord=np.inf)

        # Логируем шаги
        print(f"Шаг {iteration_count + 1}: x = {x_new}")

        # Проверка условия сходимости
        if norm < epsilon:
            print(f"Критерий сходимости достигнут на итерации {iteration_count + 1}.")
            return x_new, iteration_count + 1

        x = x_new
        iteration_count += 1

    print(f"Максимальное количество итераций ({max_iter}) было достигнуто.")
    return x, iteration_count


def main():
    filename = input("Введите имя файла с данными: ")
    try:
        A, n = read_data_from_file(filename)
        print("Исходная матрица A:")
        print(A)

        # Вызываем метод релаксаций
        solution, iteration_count = relaxation_method(A, n)

        print("-" * 50)
        print(f"Решение: {solution}")
        print(f"Количество итераций: {iteration_count}")

    except Exception as e:
        print("Ошибка:", e)


if __name__ == "__main__":
    main()
