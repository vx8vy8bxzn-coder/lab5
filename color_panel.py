"""Цветная панель, которая меняет цвет по нажатию кнопки."""

import tkinter as tk
from tkinter import ttk
from typing import Tuple


COLORS: Tuple[Tuple[str, str], ...] = (
    ("Розовый", "#f7a8b8"),
    ("Голубой", "#9ad5f5"),
    ("Зелёный", "#a8df9c"),
    ("Жёлтый", "#f8dc75"),
    ("Сиреневый", "#c5a3e8"),
)


def next_color_index(current_index: int, colors_count: int) -> int:
    """Возвращает индекс следующего цвета по кругу."""
    if isinstance(current_index, bool) or not isinstance(current_index, int):
        raise TypeError("Индекс должен быть целым числом")
    if isinstance(colors_count, bool) or not isinstance(colors_count, int):
        raise TypeError("Количество цветов должно быть целым числом")
    if colors_count <= 0:
        raise ValueError("Список цветов не должен быть пустым")
    if not 0 <= current_index < colors_count:
        raise ValueError("Индекс цвета находится вне списка")
    return (current_index + 1) % colors_count


class ColorPanelApp:
    """Управляет окном с цветной панелью."""

    def __init__(self, root: tk.Tk) -> None:
        """Создаёт элементы окна и задаёт начальный цвет."""
        self.root = root
        self.color_index = 0

        root.title("Цветная панель")
        root.geometry("420x300")
        root.resizable(False, False)

        self.panel = tk.Frame(root, width=360, height=180, bg=COLORS[0][1])
        self.panel.pack(padx=30, pady=(25, 10))
        self.panel.pack_propagate(False)

        self.color_label = tk.Label(
            self.panel,
            text=COLORS[0][0],
            bg=COLORS[0][1],
            font=("Arial", 18, "bold"),
        )
        self.color_label.place(relx=0.5, rely=0.5, anchor="center")

        ttk.Button(root, text="Сменить цвет", command=self.change_color).pack(pady=15)

    def change_color(self) -> None:
        """Переключает панель на следующий цвет."""
        self.color_index = next_color_index(self.color_index, len(COLORS))
        color_name, color_code = COLORS[self.color_index]
        self.panel.configure(bg=color_code)
        self.color_label.configure(text=color_name, bg=color_code)


def main() -> None:
    """Запускает приложение с цветной панелью."""
    root = tk.Tk()
    ColorPanelApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
