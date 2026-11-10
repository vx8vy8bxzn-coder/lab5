"""Окно Tkinter с кнопкой «Привет»."""

import tkinter as tk
from tkinter import ttk


def hello_message() -> str:
    """Возвращает сообщение для вывода после нажатия кнопки."""
    return "Привет!"


class HelloButtonApp:
    """Управляет окном с приветственной кнопкой."""

    def __init__(self, root: tk.Tk) -> None:
        """Создаёт надпись и кнопку."""
        self.root = root
        root.title("Кнопка «Привет»")
        root.geometry("360x220")
        root.resizable(False, False)

        self.message_label = ttk.Label(
            root,
            text="Нажмите кнопку",
            font=("Arial", 18),
        )
        self.message_label.pack(pady=(55, 25))

        ttk.Button(root, text="Привет", command=self.show_hello).pack()

    def show_hello(self) -> None:
        """Показывает приветствие в окне."""
        self.message_label.configure(text=hello_message())


def main() -> None:
    """Запускает окно с кнопкой «Привет»."""
    root = tk.Tk()
    HelloButtonApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
