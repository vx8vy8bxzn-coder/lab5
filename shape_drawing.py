"""Рисование прямоугольников и овалов мышью на Canvas."""

import tkinter as tk
from tkinter import ttk
from typing import Optional, Tuple, Union


Number = Union[int, float]
Coordinates = Tuple[float, float, float, float]
COLORS = {
    "Синий": "#2457c5",
    "Красный": "#d63c3c",
    "Зелёный": "#2c8b57",
    "Фиолетовый": "#7c45ad",
    "Чёрный": "#222222",
}


def normalize_coordinates(
    start_x: Number,
    start_y: Number,
    end_x: Number,
    end_y: Number,
) -> Coordinates:
    """Возвращает координаты от левого верхнего до правого нижнего угла."""
    values = (start_x, start_y, end_x, end_y)
    if any(isinstance(value, bool) for value in values) or not all(
        isinstance(value, (int, float)) for value in values
    ):
        raise TypeError("Координаты должны быть числами")
    left, right = sorted((float(start_x), float(end_x)))
    top, bottom = sorted((float(start_y), float(end_y)))
    return left, top, right, bottom


def has_visible_size(coordinates: Coordinates, minimum_size: Number = 3) -> bool:
    """Проверяет, достаточно ли велика нарисованная фигура."""
    if isinstance(minimum_size, bool) or not isinstance(minimum_size, (int, float)):
        raise TypeError("Минимальный размер должен быть числом")
    if minimum_size < 0:
        raise ValueError("Минимальный размер не может быть отрицательным")
    left, top, right, bottom = coordinates
    return right - left >= minimum_size and bottom - top >= minimum_size


class ShapeDrawingApp:
    """Управляет редактором геометрических фигур."""

    def __init__(self, root: tk.Tk) -> None:
        """Создаёт панель инструментов и холст для рисования."""
        self.root = root
        self.start_point: Optional[Tuple[float, float]] = None
        self.preview_id: Optional[int] = None

        root.title("Рисование фигур")
        root.geometry("760x560")
        root.minsize(620, 460)

        tools = ttk.Frame(root, padding=10)
        tools.pack(fill="x")

        self.shape_type = tk.StringVar(value="rectangle")
        ttk.Label(tools, text="Фигура:").pack(side="left", padx=(0, 8))
        ttk.Radiobutton(
            tools,
            text="Прямоугольник",
            variable=self.shape_type,
            value="rectangle",
        ).pack(side="left")
        ttk.Radiobutton(
            tools,
            text="Овал",
            variable=self.shape_type,
            value="oval",
        ).pack(side="left", padx=(5, 20))

        ttk.Label(tools, text="Цвет:").pack(side="left", padx=(0, 8))
        self.color_name = tk.StringVar(value="Синий")
        ttk.Combobox(
            tools,
            textvariable=self.color_name,
            values=tuple(COLORS),
            state="readonly",
            width=12,
        ).pack(side="left")

        ttk.Button(tools, text="Очистить", command=self.clear_canvas).pack(side="right")

        self.canvas = tk.Canvas(root, bg="white", cursor="crosshair")
        self.canvas.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        self.canvas.bind("<ButtonPress-1>", self.start_drawing)
        self.canvas.bind("<B1-Motion>", self.preview_shape)
        self.canvas.bind("<ButtonRelease-1>", self.finish_drawing)

    def start_drawing(self, event: tk.Event) -> None:
        """Запоминает начальную точку фигуры."""
        self.start_point = (event.x, event.y)

    def preview_shape(self, event: tk.Event) -> None:
        """Показывает контур фигуры во время движения мыши."""
        if self.start_point is None:
            return
        if self.preview_id is not None:
            self.canvas.delete(self.preview_id)

        coordinates = normalize_coordinates(*self.start_point, event.x, event.y)
        self.preview_id = self.draw_on_canvas(coordinates, dash=(5, 3))

    def finish_drawing(self, event: tk.Event) -> None:
        """Добавляет законченную фигуру на холст."""
        if self.start_point is None:
            return
        if self.preview_id is not None:
            self.canvas.delete(self.preview_id)
            self.preview_id = None

        coordinates = normalize_coordinates(*self.start_point, event.x, event.y)
        if has_visible_size(coordinates):
            self.draw_on_canvas(coordinates)
        self.start_point = None

    def draw_on_canvas(
        self,
        coordinates: Coordinates,
        dash: Optional[Tuple[int, int]] = None,
    ) -> int:
        """Рисует выбранную фигуру и возвращает её идентификатор."""
        options = {
            "outline": COLORS[self.color_name.get()],
            "width": 3,
            "dash": dash,
        }
        if self.shape_type.get() == "oval":
            return self.canvas.create_oval(*coordinates, **options)
        return self.canvas.create_rectangle(*coordinates, **options)

    def clear_canvas(self) -> None:
        """Удаляет с холста все фигуры."""
        self.canvas.delete("all")
        self.start_point = None
        self.preview_id = None


def main() -> None:
    """Запускает редактор фигур."""
    root = tk.Tk()
    ShapeDrawingApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
