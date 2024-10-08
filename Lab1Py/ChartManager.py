import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import fsolve
import re


class FunctionPlotter:
    def __init__(self, function="np.cos(np.sqrt(np.abs(x))) - x", start=-10.0, end=10.0, step=0.01):
        self.function = function
        self.start = start
        self.end = end
        self.step = step
        self.points = []
        self.previous_function = function

    def generate_data(self):
        x_values = np.arange(self.start, self.end, self.step)
        y_values = []

        for x in x_values:
            try:
                y = eval(self.function, {"np": np, "x": x})
                y_values.append(y)
            except Exception as e:
                print(f"Ошибка в функции: {e}. Пожалуйста, введите корректное выражение.")
                self.function = self.previous_function
                return self.generate_data()

        self.points = list(zip(x_values, y_values))
        return self.points

    def update_chart(self):
        self.points = self.generate_data()
        self.plot()

    def plot(self):
        if not self.points:
            print("Ошибка: отсутствуют данные для графика.")
            return

        x, y = zip(*self.points)
        plt.plot(x, y, label=self.function)
        plt.xlabel("X")
        plt.ylabel("Y")
        plt.title("График функции")
        plt.axhline(0, color='gray', lw=0.5, ls='--')
        plt.axvline(0, color='gray', lw=0.5, ls='--')
        plt.legend()
        plt.grid()
        plt.show()

    def export_to_file(self, filename):
        df = pd.DataFrame(self.points, columns=['X', 'Y'])
        df.to_csv(filename, index=False)
        print(f"Данные экспортированы в {filename}")

    def import_from_file(self, filename):
        df = pd.read_csv(filename, delimiter=';')
        if 'X' in df.columns and 'Y' in df.columns:
            self.points = df[['X', 'Y']].values.tolist()
            self.start = df['X'].min()
            self.end = df['X'].max()
            self.function = df.iloc[0, 0]  # Считаем, что первая строка содержит функцию
            self.update_chart()
        else:
            print("Ошибка: неверный формат файла.")


# Пример использования:
if __name__ == "__main__":
    plotter = FunctionPlotter()
    plotter.update_chart()  # Обновить график с использованием исходной функции
    plotter.export_to_file("output.csv")  # Экспорт данных в CSV
    plotter.import_from_file("output.csv")  # Импорт данных из CSV
