using CommunityToolkit.Mvvm.ComponentModel;
using LiveChartsCore;
using LiveChartsCore.Defaults;
using LiveChartsCore.Drawing;
using LiveChartsCore.SkiaSharpView;
using LiveChartsCore.SkiaSharpView.Painting;
using LiveChartsCore.SkiaSharpView.Painting.Effects;
using Microsoft.Win32;
using NCalc;
using SkiaSharp;
using System;
using System.Collections.ObjectModel;
using System.IO;
using System.Windows;

namespace Lab1WPF
{
    public partial class ViewModel : ObservableObject
    {
        private static readonly SKColor s_gray = new(195, 195, 195);
        private static readonly SKColor s_gray1 = new(160, 160, 160);
        private static readonly SKColor s_gray2 = new(90, 90, 90);
        private static readonly SKColor s_dark3 = new(60, 60, 60);

        private double _start;
        private double _end;

        public double Start
        {
            get => _start;
            set => SetProperty(ref _start, value);
        }

        public double End
        {
            get => _end;
            set => SetProperty(ref _end, value);
        }

        private double Step = 0.01;
        public ISeries[] Series { get; set; }
        public ObservableCollection<ObservablePoint> Points { get; set; }
        private string _function;
        private string _previousFunction;

        public string Function
        {
            get => _function;
            set => SetProperty(ref _function, value);
        }

        public DrawMarginFrame Frame { get; set; } = new()
        {
            Fill = new SolidColorPaint(s_dark3),
            Stroke = new SolidColorPaint
            {
                Color = s_gray,
                StrokeThickness = 1
            }
        };

        public Axis[] XAxes { get; set; } = {
            new Axis
            {
                Name = "X",
                NamePaint = new SolidColorPaint(s_gray1),
                TextSize = 18,
                Padding = new Padding(5, 15, 5, 5),
                LabelsPaint = new SolidColorPaint(s_gray),
                SeparatorsPaint = new SolidColorPaint
                {
                    Color = s_gray,
                    StrokeThickness = 1,
                    PathEffect = new DashEffect(new float[] { 3, 3 })
                },
                SubseparatorsPaint = new SolidColorPaint
                {
                    Color = s_gray2,
                    StrokeThickness = 0.5f
                },
                SubseparatorsCount = 9,
                ZeroPaint = new SolidColorPaint
                {
                    Color = s_gray1,
                    StrokeThickness = 2
                },
                TicksPaint = new SolidColorPaint
                {
                    Color = s_gray,
                    StrokeThickness = 1.5f
                },
                SubticksPaint = new SolidColorPaint
                {
                    Color = s_gray,
                    StrokeThickness = 1
                }
            }
        };

        public Axis[] YAxes { get; set; } = {
            new Axis
            {
                Name = "Y",
                NamePaint = new SolidColorPaint(s_gray1),
                TextSize = 18,
                Padding = new Padding(5, 0, 15, 0),
                LabelsPaint = new SolidColorPaint(s_gray),
                SeparatorsPaint = new SolidColorPaint
                {
                    Color = s_gray,
                    StrokeThickness = 1,
                    PathEffect = new DashEffect(new float[] { 3, 3 })
                },
                SubseparatorsPaint = new SolidColorPaint
                {
                    Color = s_gray2,
                    StrokeThickness = 0.5f
                },
                SubseparatorsCount = 9,
                ZeroPaint = new SolidColorPaint
                {
                    Color = s_gray1,
                    StrokeThickness = 2
                },
                TicksPaint = new SolidColorPaint
                {
                    Color = s_gray,
                    StrokeThickness = 1.5f
                },
                SubticksPaint = new SolidColorPaint
                {
                    Color = s_gray,
                    StrokeThickness = 1
                }
            }
        };

        public ViewModel()
        {
            Points = new ObservableCollection<ObservablePoint>();
            Function = "Cos(Sqrt(Abs(x))) - x";
            _previousFunction = Function;
            Start = -10.0;
            End = 10.0;

            var generatedPoints = GenerateData(Function);
            foreach (var point in generatedPoints)
            {
                Points.Add(point);
            }

            Series = new ISeries[]
            {
                new LineSeries<ObservablePoint>
                {
                    Values = Points,
                    Fill = null,
                    GeometrySize = 0,
                    LineSmoothness = 1
                }
            };
        }

        private ObservablePoint[] GenerateData(string function)
        {
            const double Step = 0.001;
            int count = (int)((End - Start) / Step) + 1;
            var points = new ObservablePoint[count];
            var expression = new NCalc.Expression(function);

            for (int i = 0; i < count; i++)
            {
                double x = Start + i * Step;
                expression.Parameters["x"] = x;
                double y;

                try
                {
                    y = Convert.ToDouble(expression.Evaluate());
                }
                catch
                {
                    MessageBox.Show("Ошибка в функции. Пожалуйста, введите корректное выражение.", "Ошибка", MessageBoxButton.OK, MessageBoxImage.Error);
                    Function = _previousFunction;
                    return GenerateData(Function);
                }

                points[i] = new ObservablePoint(x, y);
            }

            return points;
        }

        public void UpdateChart()
        {
            Points.Clear();
            var newPoints = GenerateData(Function);
            foreach (var point in newPoints)
            {
                Points.Add(point);
            }
            _previousFunction = Function;
        }

        public void SetAxes()
        {
            Points.Clear();
            var newPoints = GenerateData(Function);
            foreach (var point in newPoints)
            {
                Points.Add(point);
            }
            UpdateChart();
        }

        public void ExportToFile()
        {
            SaveFileDialog saveFileDialog = new SaveFileDialog
            {
                Filter = "CSV files (*.csv)|*.csv|All files (*.*)|*.*"
            };

            if (saveFileDialog.ShowDialog() == true)
            {
                using (StreamWriter writer = new StreamWriter(saveFileDialog.FileName))
                {
                    writer.WriteLine($"{Function};{Start};{End}");

                    if (Points != null && Points.Count > 0)
                    {
                        foreach (var point in Points)
                        {
                            writer.WriteLine($"{point.X};{point.Y}");
                        }
                    }
                    else
                    {
                        MessageBox.Show("Ошибка: отсутствуют данные для экспорта.", "Ошибка", MessageBoxButton.OK, MessageBoxImage.Error);
                    }
                }
            }
        }

        // Импорт данных из CSV
        public void ImportFromFile()
        {
            OpenFileDialog openFileDialog = new OpenFileDialog
            {
                Filter = "CSV files (*.csv)|*.csv|All files (*.*)|*.*"
            };

            if (openFileDialog.ShowDialog() == true)
            {
                Points.Clear(); // Очищаем предыдущие точки

                using (StreamReader reader = new StreamReader(openFileDialog.FileName))
                {
                    string line = reader.ReadLine(); // Читаем первую строку

                    if (line == null)
                    {
                        MessageBox.Show("Файл пустой.", "Ошибка", MessageBoxButton.OK, MessageBoxImage.Error);
                        return;
                    }

                    var parts = line.Split(';');

                    if (parts.Length == 3 && double.TryParse(parts[1], out double start) && double.TryParse(parts[2], out double end))
                    {
                        // Обрабатываем файл как файл с метаданными
                        ImportFileWithMetadata(reader, parts[0], start, end);
                    }
                    else if (parts.Length == 2 && double.TryParse(parts[0], out double x) && double.TryParse(parts[1], out double y))
                    {
                        // Обрабатываем файл как файл с набором точек
                        ImportFileWithPoints(reader, x, y);
                    }
                    else
                    {
                        MessageBox.Show("Ошибка в формате данных. Проверьте файл.", "Ошибка", MessageBoxButton.OK, MessageBoxImage.Error);
                    }
                }

                // Обновляем график после импорта
                UpdateChart();
            }
        }

        // Функция для обработки файла с метаданными (функция, начало и конец)
        private void ImportFileWithMetadata(StreamReader reader, string function, double start, double end)
        {
            Function = function;
            Start = start;
            End = end;

            // Очищаем точки перед генерацией новых данных
            Points.Clear();

            // Генерация данных на основе функции, начала и конца
            var generatedPoints = GenerateData(Function);
            foreach (var point in generatedPoints)
            {
                Points.Add(point);
            }

            // Обновляем данные для Series
            Series = new ISeries[]
            {
        new LineSeries<ObservablePoint>
        {
            Values = Points.ToArray(),
            Fill = null,
            GeometrySize = 0,
            LineSmoothness = 0
        }
            };

            // Обновляем график
            OnPropertyChanged(nameof(Series));
        }

        // Функция для обработки файла с набором точек
        private void ImportFileWithPoints(StreamReader reader, double firstX, double firstY)
        {
            // Добавляем первую точку
            Points.Add(new ObservablePoint(firstX, firstY));

            string line;
            while ((line = reader.ReadLine()) != null)
            {
                var parts = line.Split(';');
                if (parts.Length == 2 && double.TryParse(parts[0], out double x) && double.TryParse(parts[1], out double y))
                {
                    Points.Add(new ObservablePoint(x, y));
                }
                else
                {
                    MessageBox.Show("Ошибка в формате данных в строке: " + line, "Ошибка", MessageBoxButton.OK, MessageBoxImage.Error);
                    return; // Останавливаем импорт при ошибке
                }
            }

            // Обновляем данные для Series
            Series = new ISeries[]
            {
        new LineSeries<ObservablePoint>
        {
            Values = Points.ToArray(),
            Fill = null,
            GeometrySize = 0,
            LineSmoothness = 0
        }
            };
            OnPropertyChanged(nameof(Series));
        }



    }
}
