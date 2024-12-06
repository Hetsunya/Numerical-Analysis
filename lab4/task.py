import numpy as np


def read_data_from_file(filename):
    """Читает матрицу A из текстового файла."""
    with open(filename, 'r') as file:
        lines = file.readlines()
    n = int(lines[0].strip())
    matrix = []
    for line in lines[1:]:
        matrix.append(list(map(float, line.split()[:-1])))  # Игнорируем столбец b
    A = np.array(matrix)
    return A, n


def gaussian_determinant(A, n):
    """Вычисляет определитель методом Гаусса с выбором ведущего элемента."""
    det = 1
    swap_count = 0  # Счётчик перестановок строк
    logs = []  # Логи шагов вычисления

    for k in range(n):
        # Выбор ведущего элемента
        max_row = max(range(k, n), key=lambda i: abs(A[i][k]))
        logs.append(
            f"Выбор ведущего элемента в столбце {k + 1}: max |A[{max_row + 1},{k + 1}]| = {abs(A[max_row][k]):.3f}")

        if A[max_row][k] == 0:
            logs.append("Матрица вырожденная, определитель равен 0.")
            return 0, logs

        # Перестановка строк
        if max_row != k:
            A[[k, max_row]] = A[[max_row, k]]
            swap_count += 1
            det *= -1  # Меняем знак определителя при перестановке строк
            logs.append(f"Перестановка строк {k + 1} и {max_row + 1}, смена знака определителя.")

        # Прямой ход
        for i in range(k + 1, n):
            factor = A[i][k] / A[k][k]
            A[i, k:] -= factor * A[k, k:]
            logs.append(f"Обновление строки {i + 1}: A[{i + 1}] -= ({factor:.3f}) * A[{k + 1}]")

        # Умножаем на диагональный элемент
        det *= A[k][k]
        logs.append(f"Умножение определителя на диагональный элемент A[{k + 1},{k + 1}] = {A[k][k]:.3f}")
        logs.append(f"Текущий определитель: {det:.3f}")

        # Вывод текущего состояния
        logs.append(f"Матрица после шага {k + 1}:\n{A}\n")

    # Учет перестановок
    formula = f"{' * '.join([f'A[{i + 1},{i + 1}]' for i in range(n)])} * (-1)^{swap_count}"
    logs.append(f"Формула определителя: {formula}")
    logs.append(f"Количество перестановок строк: {swap_count}")

    return det, logs


def main():
    filename = "data.txt"
    try:
        A, n = read_data_from_file(filename)
        print("Исходная матрица A:")
        print(A)
        print("-" * 50)

        det, logs = gaussian_determinant(A.copy(), n)

        for log in logs:
            print(log)

        print("-" * 50)
        print(f"Определитель матрицы: {det:.3f}")
    except Exception as e:
        print("Ошибка:", e)


if __name__ == "__main__":
    main()
