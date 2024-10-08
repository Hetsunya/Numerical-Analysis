import tkinter as tk
from tkinter import filedialog, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
from graph_library import GraphPlotter  # Импортируем нашу библиотеку


class GraphApp:
    def __init__(self, root):
        self.root = root
        self.root.title("График функции")

        self.plotter = GraphPlotter()

        # Поле для ввода функции
        self.function_label = tk.Label(root, text="Функция:")
        self.function_label.pack()
        self.function_entry = tk.Entry(root)
        self.function_entry.pack()
        self.function_entry.insert(0, self.plotter.function)

        # Поле для ввода начала и конца
        self.start_label = tk.Label(root, text="Начало X:")
        self.start_label.pack()
        self.start_entry = tk.Entry(root)
        self.start_entry.pack()
        self.start_entry.insert(0, str(self.plotter.start))

        self.end_label = tk.Label(root, text="Конец X:")
        self.end_label.pack()
        self.end_entry = tk.Entry(root)
        self.end_entry.pack()
        self.end_entry.insert(0, str(self.plotter.end))

        # Кнопка обновления графика
        self.update_button = tk.Button(root, text="Обновить график", command=self.update_plot)
        self.update_button.pack()

        # Кнопки для импорта/экспорта
        self.export_button = tk.Button(root, text="Экспортировать в файл", command=self.export_to_file)
        self.export_button.pack()

        self.import_button = tk.Button(root, text="Импортировать из файла", command=self.import_from_file)
        self.import_button.pack()

        # Поле для графика
        self.fig = Figure(figsize=(6, 4))
        self.ax = self.fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.canvas.get_tk_widget().pack()

        # Добавляем панель инструментов для интерактивности
        self.toolbar = NavigationToolbar2Tk(self.canvas, root)
        self.toolbar.update()
        self.canvas.get_tk_widget().pack()

        self.update_plot()

    def update_plot(self):
        try:
            function = self.function_entry.get()
            start = float(self.start_entry.get())
            end = float(self.end_entry.get())

            self.plotter.function = function
            self.plotter.start = start
            self.plotter.end = end

            # Генерация данных только если есть функция, а не произвольные точки
            if self.plotter.points and len(self.plotter.points) < 3:
                # Если у нас меньше 3 точек, предполагаем, что это произвольные точки
                self.plotter.points = self.plotter.points  # Используем уже загруженные точки
            else:
                self.plotter.generate_data()

            self.ax.clear()
            self.plotter.plot(self.ax)
            self.canvas.draw()

        except ValueError as e:
            messagebox.showerror("Ошибка", f"Некорректный ввод: {e}")

    def export_to_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if file_path:
            self.plotter.export_to_file(file_path)

    def import_from_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if file_path:
            self.plotter.import_from_file(file_path)
            # После импорта обновляем поля ввода
            self.function_entry.delete(0, tk.END)
            self.function_entry.insert(0, self.plotter.function)
            self.start_entry.delete(0, tk.END)
            self.start_entry.insert(0, str(self.plotter.start))
            self.end_entry.delete(0, tk.END)
            self.end_entry.insert(0, str(self.plotter.end))
            self.update_plot()


# Запуск приложения
if __name__ == "__main__":
    root = tk.Tk()
    app = GraphApp(root)
    root.mainloop()
