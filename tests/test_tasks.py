"""Проверки всех заданий варианта 9."""

import os
import unittest
from unittest.mock import MagicMock, patch

import pyqt_table
from color_panel import COLORS, ColorPanelApp, next_color_index
from hello_button import HelloButtonApp, hello_message
from progress_bar import ProgressBarApp, next_progress
from pyqt_table import (
    BOOKS,
    PYQT_AVAILABLE,
    TABLE_HEADERS,
    BookTableWindow,
    main as pyqt_main,
    table_rows,
)
from shape_drawing import has_visible_size, normalize_coordinates


class HelloButtonTests(unittest.TestCase):
    """Проверки окна с приветственной кнопкой."""

    def test_returns_hello_message(self) -> None:
        self.assertEqual(hello_message(), "Привет!")

    def test_button_handler_updates_label(self) -> None:
        application = object.__new__(HelloButtonApp)
        application.message_label = MagicMock()

        application.show_hello()

        application.message_label.configure.assert_called_once_with(text="Привет!")


class ColorPanelTests(unittest.TestCase):
    """Проверки переключения цветов панели."""

    def test_returns_next_index(self) -> None:
        self.assertEqual(next_color_index(0, 5), 1)

    def test_wraps_after_last_color(self) -> None:
        self.assertEqual(next_color_index(4, 5), 0)

    def test_rejects_index_outside_list(self) -> None:
        with self.assertRaises(ValueError):
            next_color_index(-1, 5)
        with self.assertRaises(ValueError):
            next_color_index(5, 5)

    def test_rejects_empty_color_list(self) -> None:
        with self.assertRaises(ValueError):
            next_color_index(0, 0)

    def test_rejects_boolean_values(self) -> None:
        with self.assertRaises(TypeError):
            next_color_index(True, 5)

    def test_button_handler_changes_panel_and_label(self) -> None:
        application = object.__new__(ColorPanelApp)
        application.color_index = 0
        application.panel = MagicMock()
        application.color_label = MagicMock()

        application.change_color()

        color_name, color_code = COLORS[1]
        self.assertEqual(application.color_index, 1)
        application.panel.configure.assert_called_once_with(bg=color_code)
        application.color_label.configure.assert_called_once_with(
            text=color_name,
            bg=color_code,
        )


class ProgressBarTests(unittest.TestCase):
    """Проверки вычисления и отображения прогресса."""

    def test_adds_step(self) -> None:
        self.assertEqual(next_progress(20, 10), 30)

    def test_stops_exactly_at_maximum(self) -> None:
        self.assertEqual(next_progress(95, 10, 100), 100)

    def test_starts_again_after_maximum(self) -> None:
        self.assertEqual(next_progress(100), 0)

    def test_rejects_invalid_range(self) -> None:
        with self.assertRaises(ValueError):
            next_progress(-1)
        with self.assertRaises(ValueError):
            next_progress(101)

    def test_rejects_non_positive_step(self) -> None:
        with self.assertRaises(ValueError):
            next_progress(10, 0)

    def test_rejects_boolean_values(self) -> None:
        with self.assertRaises(TypeError):
            next_progress(True)

    def test_button_handler_updates_progressbar_and_label(self) -> None:
        application = object.__new__(ProgressBarApp)
        application.progress_value = 20.0
        application.progress_bar = MagicMock()
        application.value_label = MagicMock()

        application.advance()

        self.assertEqual(application.progress_value, 30)
        application.progress_bar.configure.assert_called_once_with(value=30)
        application.value_label.configure.assert_called_once_with(text="30%")


class ShapeDrawingTests(unittest.TestCase):
    """Проверки геометрии редактора фигур."""

    def test_keeps_ordered_coordinates(self) -> None:
        self.assertEqual(
            normalize_coordinates(10, 20, 80, 90),
            (10.0, 20.0, 80.0, 90.0),
        )

    def test_normalizes_reverse_drawing_direction(self) -> None:
        self.assertEqual(
            normalize_coordinates(80, 90, 10, 20),
            (10.0, 20.0, 80.0, 90.0),
        )

    def test_rejects_non_numeric_coordinates(self) -> None:
        with self.assertRaises(TypeError):
            normalize_coordinates(0, 0, "10", 20)

    def test_accepts_visible_shape(self) -> None:
        self.assertTrue(has_visible_size((0, 0, 10, 15)))

    def test_rejects_tiny_shape(self) -> None:
        self.assertFalse(has_visible_size((0, 0, 2, 10)))

    def test_rejects_negative_minimum_size(self) -> None:
        with self.assertRaises(ValueError):
            has_visible_size((0, 0, 10, 10), -1)


class PyQtTableTests(unittest.TestCase):
    """Проверки данных приложения с таблицей."""

    def test_table_has_four_columns(self) -> None:
        self.assertEqual(
            TABLE_HEADERS,
            ("Название", "Автор", "Год", "Статус"),
        )

    def test_converts_all_rows_to_strings(self) -> None:
        rows = table_rows()

        self.assertEqual(len(rows), len(BOOKS))
        self.assertTrue(all(isinstance(value, str) for row in rows for value in row))

    def test_returns_new_list_for_each_call(self) -> None:
        self.assertIsNot(table_rows(), table_rows())

    @unittest.skipUnless(PYQT_AVAILABLE, "Для проверки нужен PyQt5")
    def test_window_contains_all_table_rows(self) -> None:
        os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
        application = pyqt_table.QApplication.instance()
        if application is None:
            application = pyqt_table.QApplication([])
        window = BookTableWindow()

        self.assertEqual(window.table.rowCount(), len(BOOKS))
        self.assertEqual(window.table.columnCount(), len(TABLE_HEADERS))

        window.close()

    @unittest.skipIf(PYQT_AVAILABLE, "Проверка нужна только без PyQt5")
    def test_window_explains_missing_dependency(self) -> None:
        with self.assertRaisesRegex(RuntimeError, "PyQt5"):
            BookTableWindow()

    @unittest.skipIf(PYQT_AVAILABLE, "Проверка нужна только без PyQt5")
    def test_main_prints_installation_hint(self) -> None:
        with patch("builtins.print") as print_mock:
            exit_code = pyqt_main()

        self.assertEqual(exit_code, 1)
        self.assertIn("requirements.txt", print_mock.call_args.args[0])


if __name__ == "__main__":
    unittest.main()
