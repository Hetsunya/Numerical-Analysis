import numpy as np

def read_matrix_from_file(filename):
    with open(filename, 'r') as file:
        n = int(file.readline().strip())
        A = [list(map(float, line.split()[:-1])) for line in file]
    return np.array(A), n

def to_upper_triangular(A, n):
    swap_count = 0
    
    for i in range(n):
        # Поиск строки с максимальным элементом в текущем столбце для устойчивости
        max_row = i + np.argmax(np.abs(A[i:, i]))
        if i != max_row:
            A[[i, max_row]] = A[[max_row, i]]
            swap_count += 1
            print(f"Перестановка строк {i+1} и {max_row+1}:")
            print(A, "\n")
        
        if A[i, i] == 0:
            print("Элемент на главной диагонали равен 0, матрица вырожденная.")
            return A, swap_count, True

        # Приведение к треугольному виду
        for j in range(i + 1, n):
            factor = A[j, i] / A[i, i]  # Коэффициент для исключения
            A[j, i:] -= factor * A[i, i:]  # Вычитание строки для получения нуля ниже главного элемента
            
            print(f"Обнуление элемента в строке {j+1}, столбце {i+1}")
            print(A, "\n")

    return A, swap_count, False

def gauss_determinant(A, n):
    A, swap_count, singular = to_upper_triangular(A, n)

    if singular:
        return 0

    det = (-1) ** swap_count
    for i in range(n):
        det *= A[i, i]
    
    print("Матрица после приведения к треугольному виду:")
    print(A, "\n")
    return det

filename = '.\Lab4\matrix_data.txt'
A, n = read_matrix_from_file(filename)

print("Исходная матрица A:")
print(A)

det = gauss_determinant(A.copy(), n) 

print("\nОпределитель матрицы A:", det)
