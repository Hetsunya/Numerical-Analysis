using ChartLibrary;
using LiveChartsCore;
using LiveChartsCore.SkiaSharpView;
using System.Windows;
using LiveChartsCore.Defaults;

namespace Lab2WPF
{
    public partial class ViewModel
    {
        private readonly ChartManager _chartManager;

        public ViewModel()
        {
            _chartManager = new ChartManager();

            // Пример генерации графика на основе функции
            _chartManager.GenerateDataFromFunction("Sin(x)", -10, 10);
            Series = _chartManager.Series;
        }

        public ISeries[] Series { get; set; }

        public void ImportPoints(ObservablePoint[] points)
        {
            _chartManager.UpdatePoints(points);
            Series = _chartManager.Series;
        }
    }
}
