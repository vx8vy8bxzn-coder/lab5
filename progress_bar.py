"""Окно Tkinter с управляемым прогрессбаром."""

import tkinter as tk
from tkinter import ttk
from typing import Union


Number = Union[int, float]


def next_progress(current: Number, step: Number = 10, maximum: Number = 100) -> float:
    """Увеличивает прогресс, а после максимума начинает его заново."""
    values = (current, step, maximum)
    if any(isinstance(value, bool) for value in values) or not all(
        isinstance(value, (int, float)) for value in values
    ):
        raise TypeError("Значения прогресса должны быть числами")
    if maximum <= 0:
        raise ValueError("Максимум должен быть больше нуля")
    if step <= 0:
        raise ValueError("Шаг должен быть больше нуля")
    if not 0 <= current <= maximum:
        raise ValueError("Текущий прогресс находится вне допустимого диапазона")
    if current == maximum:
        return 0.0
    return float(min(current + step, maximum))


class ProgressBarApp:
    """Управляет окном с прогрессбаром."""

    def __init__(self, root: tk.Tk) -> None:
        """Создаёт прогрессбар, надпись и кнопку."""
        self.root = root
        self.progress_value = 0.0

        root.title("Прогрессбар")
        root.geometry("420x230")
        root.resizable(False, False)

        self.value_label = ttk.Label(root, text="0%", font=("Arial", 18, "bold"))
        self.value_label.pack(pady=(45, 15))

        self.progress_bar = ttk.Progressbar(
            root,
            orient="horizontal",
            length=330,
            mode="determinate",
            maximum=100,
        )
        self.progress_bar.pack(pady=10)

        ttk.Button(root, text="Продолжить", command=self.advance).pack(pady=15)

    def advance(self) -> None:
        """Передвигает прогрессбар на один шаг."""
        self.progress_value = next_progress(self.progress_value)
        self.progress_bar.configure(value=self.progress_value)
        self.value_label.configure(text=f"{self.progress_value:g}%")


def main() -> None:
    """Запускает окно с прогрессбаром."""
    root = tk.Tk()
    ProgressBarApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
