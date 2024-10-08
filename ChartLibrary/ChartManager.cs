using LiveChartsCore;
using LiveChartsCore.Defaults;
using LiveChartsCore.SkiaSharpView;
using System.Collections.ObjectModel;

namespace ChartLibrary
{
    public class ChartManager
    {
        public ObservableCollection<ObservablePoint> Points { get; set; }
        public ISeries[] Series { get; set; }

        public ChartManager()
        {
            Points = new ObservableCollection<ObservablePoint>();
        }

        public void GenerateDataFromFunction(string function, double start, double end, double step = 0.01)
        {
            Points.Clear();
            var generatedPoints = FunctionDataGenerator.GenerateData(function, start, end, step);
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

        public void UpdatePoints(ObservablePoint[] points)
        {
            Points.Clear();
            foreach (var point in points)
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
    }
}
