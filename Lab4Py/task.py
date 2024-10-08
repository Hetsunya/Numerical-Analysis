import numpy as np


def read_data(filename):
    with open(filename, 'r') as file:
        n = int(file.readline().strip())
        A = []
        b = []
        for line in file:
            values = list(map(float, line.strip().split()))
            A.append(values[:-1])  # все элементы, кроме последнего
            b.append(values[-1])  # последний элемент
    return np.array(A), np.array(b)


def gauss_elimination(A, b):
    n = len(b)
    # Создаем расширенную матрицу
    Ab = np.hstack((A, b.reshape(-1, 1)))

    for i in range(n):
        # Постолбцовый выбор ведущего элемента
        max_row = np.argmax(np.abs(Ab[i:, i])) + i
        Ab[[i, max_row]] = Ab[[max_row, i]]  # меняем местами строки

        # Прямой ход Гаусса
        for j in range(i + 1, n):
            factor = Ab[j, i] / Ab[i, i]
            Ab[j, i:] -= factor * Ab[i, i:]

    # Обратный ход
    x = np.zeros(n)
    for i in range(n - 1, -1, -1):
        x[i] = (Ab[i, -1] - np.dot(Ab[i, i + 1:n], x[i + 1:n])) / Ab[i, i]

    return x


def main(filename):
    A, b = read_data(filename)
    print("Исходные данные:")
    print("Матрица A:\n", A)
    print("Вектор b:\n", b)

    solution = gauss_elimination(A, b)
    print("Решение системы A~x = ~b:")
    print("x =", solution)


if __name__ == "__main__":
    filename = 'data.txt'  # Укажите имя вашего файла
    main(filename)
