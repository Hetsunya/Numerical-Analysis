package main

import (
	"fmt"
	"image/color"
	"log"
	"math"
	"strconv"

	"fyne.io/fyne/v2/app"
	"fyne.io/fyne/v2/container"
	"fyne.io/fyne/v2/dialog"
	"fyne.io/fyne/v2/widget"
	"gonum.org/v1/plot"
	"gonum.org/v1/plot/plotter"
	"gonum.org/v1/plot/vg"
)

type FunctionPlotter struct {
	start  float64
	end    float64
	step   float64
	function string
}

func NewFunctionPlotter(function string, start, end, step float64) *FunctionPlotter {
	return &FunctionPlotter{
		start:   start,
		end:     end,
		step:    step,
		function: function,
	}
}

func (fp *FunctionPlotter) GenerateData() (plotter.XYs, error) {
	pts := plotter.XYs{}
	step := fp.step
	for x := fp.start; x <= fp.end; x += step {
		y := evalFunction(fp.function, x)
		pts = append(pts, plotter.XY{X: x, Y: y})
	}
	return pts, nil
}

func evalFunction(function string, x float64) float64 {
	// Для простоты, используя math библиотеку для примера
	switch function {
	case "sin(x)":
		return math.Sin(x)
	case "cos(x)":
		return math.Cos(x)
	default:
		return x // просто возвращаем x для любых других функций
	}
}

func plotFunction(function string, start, end, step float64) {
	fp := NewFunctionPlotter(function, start, end, step)
	data, err := fp.GenerateData()
	if err != nil {
		log.Fatalf("Ошибка генерации данных: %v", err)
	}

	p, err := plot.New()
	if err != nil {
		log.Fatalf("Ошибка создания графика: %v", err)
	}

	p.Title.Text = "График функции"
	p.X.Label.Text = "X"
	p.Y.Label.Text = "Y"

	line, err := plotter.NewLine(data)
	if err != nil {
		log.Fatalf("Ошибка создания линии: %v", err)
	}
	line.Color = color.RGBA{R: 255, G: 0, B: 0, A: 255} // Красный цвет

	p.Add(line)
	p.X.Min = start
	p.X.Max = end
	p.Y.Min = -1
	p.Y.Max = 1

	if err := p.Save(4*vg.Inch, 4*vg.Inch, "plot.png"); err != nil {
		log.Fatalf("Ошибка сохранения графика: %v", err)
	}

	dialog.ShowInformation("График", "График сохранен как plot.png", a.Window())
}

var a = app.New()

func main() {
	w := a.NewWindow("Function Plotter")

	functionEntry := widget.NewEntry()
	functionEntry.SetPlaceHolder("Введите функцию (например: sin(x) или cos(x))")

	startEntry := widget.NewEntry()
	startEntry.SetPlaceHolder("Начало")

	endEntry := widget.NewEntry()
	endEntry.SetPlaceHolder("Конец")

	stepEntry := widget.NewEntry()
	stepEntry.SetPlaceHolder("Шаг")

	plotButton := widget.NewButton("Построить график", func() {
		start, _ := strconv.ParseFloat(startEntry.Text, 64)
		end, _ := strconv.ParseFloat(endEntry.Text, 64)
		step, _ := strconv.ParseFloat(stepEntry.Text, 64)
		function := functionEntry.Text

		plotFunction(function, start, end, step)
	})

	w.SetContent(container.NewVBox(
		functionEntry,
		startEntry,
		endEntry,
		stepEntry,
		plotButton,
	))

	w.ShowAndRun()
}
