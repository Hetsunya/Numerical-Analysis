import numpy as np

# Генерация сетки значений
x = np.linspace(-5, 5, 100)
y = np.cos(np.sqrt(np.abs(x))) - x

# Вычисление численной производной
dy_dx = np.gradient(y, x)

# Сравнение на графике
import matplotlib.pyplot as plt

plt.plot(x, y, label="f(x)")
plt.plot(x, dy_dx, label="Численная производная (NumPy)")
plt.legend()
plt.show()
