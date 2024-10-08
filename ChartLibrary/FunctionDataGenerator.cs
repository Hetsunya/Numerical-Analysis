using LiveChartsCore.Defaults;
using NCalc;
using System;

namespace ChartLibrary
{
    public static class FunctionDataGenerator
    {
        public static ObservablePoint[] GenerateData(string function, double start, double end, double step)
        {
            int count = (int)((end - start) / step) + 1;
            var points = new ObservablePoint[count];
            var expression = new NCalc.Expression(function);

            for (int i = 0; i < count; i++)
            {
                double x = start + i * step;
                expression.Parameters["x"] = x;
                double y = Convert.ToDouble(expression.Evaluate());
                points[i] = new ObservablePoint(x, y);
            }

            return points;
        }
    }
}
