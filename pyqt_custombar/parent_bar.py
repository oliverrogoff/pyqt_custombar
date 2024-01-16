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

        if minimum is not None or maximum is not None:
            self._is_determinate = True
        else:
            self._is_determinate = False

        if self._is_determinate:
            if minimum is None or maximum is None:
                print("Error: If is determinate must declare minimum and maximum values")
                sys.exit()
            self._minimum = minimum
            self._maximum = maximum

        self._color: QColor = QColor(color[0], color[1], color[2])
        self._bar_length: int = bar_length
        self._bar_height: int = bar_height
        self._border_width: int = border_width

        if background_color is not None:
            if background_color[0] == -1:
                new_color = lighten_color(color, 60)
                self._background_color: QColor = QColor(new_color[0], new_color[1], new_color[2])
            else:
                self._background_color: QColor = QColor(background_color[0], background_color[1], background_color[2])

        if 0 <= border_roundness <= 1:
            self._border_roundness = border_roundness * self._bar_height * 0.6
        else:
            print("Error: border roundness must be a float between 0 and 1")
            sys.exit()

        self._current_value = 0
        self._percent_complete = 0.0

        self._border_path = None

        # self._current_counter: int = 0
        # self._timer: QTimer = QTimer(self)
        # self._timer.timeout.connect(self._rotate)
        # self._update_timer()
        # self._is_spinning = True
        # self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

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

    # def _update_timer(self) -> None:
    #     """Update the spinning speed of the WaitingSpinner."""
    #     self._timer.setInterval(
    #         int(1000 / (self._number_of_lines * self._revolutions_per_second))
    #     )

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
        self._current_value = value
        self._recalculate_percent_complete()
        self.repaint()

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
