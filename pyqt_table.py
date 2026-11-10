"""Приложение PyQt5 с таблицей книг."""

import sys
from typing import List, Tuple


try:
    from PyQt5.QtCore import Qt
    from PyQt5.QtWidgets import (
        QAbstractItemView,
        QApplication,
        QHeaderView,
        QLabel,
        QMainWindow,
        QTableWidget,
        QTableWidgetItem,
        QVBoxLayout,
        QWidget,
    )
except ImportError:
    PYQT_AVAILABLE = False
    QMainWindow = object
else:
    PYQT_AVAILABLE = True


BookRow = Tuple[str, str, int, str]
TABLE_HEADERS = ("Название", "Автор", "Год", "Статус")
BOOKS: Tuple[BookRow, ...] = (
    ("Мастер и Маргарита", "Михаил Булгаков", 1967, "Прочитана"),
    ("Евгений Онегин", "Александр Пушкин", 1833, "Прочитана"),
    ("Война и мир", "Лев Толстой", 1869, "Читаю"),
    ("Преступление и наказание", "Фёдор Достоевский", 1866, "В планах"),
)


def table_rows() -> List[Tuple[str, ...]]:
    """Возвращает данные таблицы в виде строк."""
    return [tuple(str(value) for value in book) for book in BOOKS]


class BookTableWindow(QMainWindow):
    """Главное окно PyQt5 с таблицей книг."""

    def __init__(self) -> None:
        """Создаёт и заполняет таблицу."""
        if not PYQT_AVAILABLE:
            raise RuntimeError("Для запуска нужно установить PyQt5")
        super().__init__()

        self.setWindowTitle("Моя книжная таблица")
        self.resize(780, 390)

        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)

        title = QLabel("Список книг")
        title.setAlignment(Qt.AlignCenter)
        title.setMinimumHeight(44)
        title.setStyleSheet("font-size: 20px; font-weight: bold; margin: 8px;")
        layout.addWidget(title)

        rows = table_rows()
        self.table = QTableWidget(len(rows), len(TABLE_HEADERS))
        self.table.setHorizontalHeaderLabels(TABLE_HEADERS)
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setSortingEnabled(False)

        for row_index, row in enumerate(rows):
            for column_index, value in enumerate(row):
                item = QTableWidgetItem(value)
                if column_index == 2:
                    item.setTextAlignment(Qt.AlignCenter)
                self.table.setItem(row_index, column_index, item)

        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        self.table.setSortingEnabled(True)
        layout.addWidget(self.table)

        row_count = QLabel(f"Всего книг: {len(rows)}")
        row_count.setAlignment(Qt.AlignRight)
        layout.addWidget(row_count)

        self.setCentralWidget(central_widget)


def main() -> int:
    """Запускает приложение с таблицей книг."""
    if not PYQT_AVAILABLE:
        print("Ошибка: PyQt5 не установлен. Выполните: pip install -r requirements.txt")
        return 1

    application = QApplication(sys.argv)
    window = BookTableWindow()
    window.show()
    return application.exec_()


if __name__ == "__main__":
    raise SystemExit(main())
