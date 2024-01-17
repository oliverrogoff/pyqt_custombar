import sys
import math
from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QPainter, QPen, QPainterPath


class ParentBar(QWidget):

    def __init__(self,
                 parent: QWidget,
                 minimum: int = None,
                 maximum: int = None,
                 center_on_parent: bool = True,
                 disable_parent_when_running: bool = False,
                 bar_length: int = None,
                 bar_height: int = None,
                 color: tuple[int, int, int] = (0, 0, 0),
                 background_color: tuple[int, int, int] = (-1, -1, -1),
                 border_width: int = 1,
                 border_roundness: float = 0.5,
                 is_vertical: bool = False
                 ) -> None:
        super().__init__(parent)

        self._center_on_parent: bool = center_on_parent
        self._disable_parent_when_running: bool = disable_parent_when_running
        self._is_vertical = is_vertical

        if minimum is not None and maximum is not None:
            self._is_determinate = True
        else:
            self._is_determinate = False

        self._minimum = minimum
        self._maximum = maximum

        self._color: QColor = QColor(color[0], color[1], color[2])
        self._bar_length: int = bar_length
        self._bar_height: int = bar_height
        self._border_width: int = border_width

        self._background_color = None
        self.set_background_color(background_color)

        self._border_roundness_input = None
        self._border_roundness = None
        self.set_border_roundness(border_roundness)

        self._current_value = 0
        self._percent_complete = 0.0

        self._border_path = None

        self._update_size()
        self.hide()

    def _update_size(self) -> None:
        """Update the size of the ProgressBar."""
        if self._is_vertical:
            if self._bar_length is not None:
                self.setFixedHeight(self._bar_length + (2 * self._border_width))
            else:
                self._bar_length = self.size().height()

            if self._bar_height is not None:
                self.setFixedWidth(self._bar_height + (2 * self._border_width))
            else:
                self._bar_height = self.size().width()
        else:
            if self._bar_length is not None:
                self.setFixedWidth(self._bar_length + (2 * self._border_width))
            else:
                self._bar_length = self.size().width()

            if self._bar_height is not None:
                self.setFixedHeight(self._bar_height + (2 * self._border_width))
            else:
                self._bar_height = self.size().height()

    def _update_position(self) -> None:
        """Center ProgressBar on parent widget."""
        if self.parentWidget() and self._center_on_parent:
            self.move(
                (self.parentWidget().width() - self.width()) // 2,
                (self.parentWidget().height() - self.height()) // 2,
            )

    def _recalculate_percent_complete(self):
        """update the percent complete value"""
        if self._is_determinate:
            self._percent_complete = float(self._current_value / (self._maximum - self._minimum))

    @staticmethod
    def _line_count_distance_from_primary(
        current: int, primary: int, total_nr_of_lines: int
    ) -> int:
        """Return the amount of lines from _current_counter."""
        distance = primary - current
        if distance < 0:
            distance += total_nr_of_lines
        return distance

    @staticmethod
    def _current_line_color(
        count_distance: int,
        total_nr_of_lines: int,
        trail_fade_perc: float,
        min_opacity: float,
        color_input: QColor,
    ) -> QColor:
        """Returns the current color for the ProgressBar."""
        color = QColor(color_input)
        if count_distance == 0:
            return color
        min_alpha_f = min_opacity / 100.0
        distance_threshold = int(
            math.ceil((total_nr_of_lines - 1) * trail_fade_perc / 100.0)
        )
        if count_distance > distance_threshold:
            color.setAlphaF(min_alpha_f)
        else:
            alpha_diff = color.alphaF() - min_alpha_f
            gradient = alpha_diff / float(distance_threshold + 1)
            result_alpha = color.alphaF() - gradient * count_distance
            # If alpha is out of bounds, clip it.
            result_alpha = min(1.0, max(0.0, result_alpha))
            color.setAlphaF(result_alpha)
        return color

    def _paint_border(self):
        if self._update_border() is None:
            self._update_border()

        if self._border_width > 0:
            outline_painter = QPainter(self)
            pen = QPen()
            pen.setWidth(self._border_width)
            outline_painter.setPen(pen)
            outline_painter.drawPath(self._border_path)

    def _paint_background(self):
        if self._update_border() is None:
            self._update_border()

        if self._background_color is not None:
            painter = QPainter(self)
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(self._background_color)
            painter.drawPath(self._border_path)

    def _update_border(self):
        path = QPainterPath()

        x = self._border_width / 2
        y = self._border_width / 2

        if self._is_vertical:
            width = self._bar_height + self._border_width
            height = self._bar_length + self._border_width

        else:
            width = self._bar_length + self._border_width
            height = self._bar_height + self._border_width

        path.moveTo(x + self._border_roundness, y)
        path.arcTo(x, y, 2 * self._border_roundness, 2 * self._border_roundness, 90.0, 90.0)
        path.lineTo(x, y + (height - self._border_roundness))
        path.arcTo(x, y + (height - 2 * self._border_roundness),
                   2 * self._border_roundness, 2 * self._border_roundness, 180.0, 90.0)
        path.lineTo(x + (width - self._border_roundness), y + height)
        path.arcTo(x + (width - 2 * self._border_roundness), y + (height - 2 * self._border_roundness),
                   2 * self._border_roundness, 2 * self._border_roundness, 270.0, 90.0)
        path.lineTo(x + width, y + self._border_roundness)
        path.arcTo(x + (width - 2 * self._border_roundness), y,
                   2 * self._border_roundness, 2 * self._border_roundness, 0.0, 90.0)
        path.lineTo(x + self._border_roundness, y)

        self._border_path = path

    def get_minimum(self):
        return self._minimum

    def get_maximum(self):
        return self._maximum

    def get_color(self):
        return self._color.getRgb()

    def get_bar_length(self):
        return self._bar_length

    def get_bar_height(self):
        return self._bar_height

    def get_background_color(self):
        return self._background_color.getRgb()

    def get_border_width(self):
        return self._border_width

    def get_border_roundness(self):
        return self._border_roundness_input

    def get_is_vertical(self):
        return self._is_vertical

    def set_minimum(self, min: int):
        self._minimum = min
        if self._maximum is not None:
            self._is_determinate = True

    def set_maximum(self, max: int):
        self._maximum = max
        if self._minimum is not None:
            self._is_determinate = True

    def set_bar_length(self, length: int):
        self._bar_length = length
        self.repaint()

    def set_bar_height(self, height: int):
        self._bar_height = height
        self.set_border_roundness(self._border_roundness_input)
        self.repaint()

    def set_border_roundness(self, border_roundness: float):
        self._border_roundness_input = border_roundness
        if 0 <= self._border_roundness_input <= 1:
            self._border_roundness = self._border_roundness_input * self._bar_height * 0.5
        else:
            print("Error: border roundness must be a float between 0 and 1")
            self._border_roundness = 0

    def set_vertical(self, is_vertical: bool):
        self._is_vertical = is_vertical
        self.repaint()

    def set_color(self, color: tuple[int, int, int]):
        self._color = QColor(color[0], color[1], color[2])
        self.repaint()

    def set_background_color(self, background_color: tuple[int, int, int]):
        if background_color is not None:
            if background_color[0] == -1:
                new_color = lighten_color(self._color.getRgb(), 60)
                self._background_color: QColor = QColor(new_color[0], new_color[1], new_color[2])
            else:
                self._background_color: QColor = QColor(background_color[0], background_color[1], background_color[2])

    def set_border_width(self, width: int):
        self._border_width = width
        self.repaint()

    def get_percent_complete(self):
        return self._percent_complete

    def set_value_by_percent(self, percent_complete: float):
        if percent_complete > 1.0 or percent_complete < 0.0:
            print("ERROR: PERCENT COMPLETE MUST BE FLOAT BETWEEN 0.0 AND 1.0")
            if percent_complete > 1.0:
                percent_complete = 1.0
            else:
                percent_complete = 0.0
        self._percent_complete = percent_complete
        self.repaint()

    def set_value(self, value: int):
        if self._is_determinate:
            self._current_value = value
            self._recalculate_percent_complete()
            self.repaint()
        else:
            print("ERROR: Can't set value without minimum and maximum values set")

    def start_bar(self):
        self._update_position()
        self.show()


def lighten_color(color: tuple[int, int, int], amount_lightened: int):
    red = color[0]
    new_red = round(color[0] + min(255 - red, amount_lightened))
    red_diff = 255 - color[0]
    red_increase = new_red - color[0]
    increase_fraction = red_increase / red_diff
    new_green = round(color[1] + (255 - color[1]) * increase_fraction)
    new_blue = round(color[2] + (255 - color[2]) * increase_fraction)
    return new_red, new_green, new_blue


