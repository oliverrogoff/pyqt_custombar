import math
import sys

from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import Qt, QTimer, QRect
from PyQt6.QtGui import QColor, QPainter, QPaintEvent


class ProgressBar(QWidget):

    def __init__(self,
                 parent: QWidget,
                 determinate: bool = False,
                 minimum: int  = None,
                 maximum: int = None,
                 center_on_parent: bool = True,
                 disable_parent_when_running: bool = False,
                 bar_length: int = None,
                 bar_height: int = None,
                 min_opacity: float = math.pi,
                 fade: float = 80.0,
                 lines: int = 40,
                 # line_length: int = 10,
                 line_width: int = 2,
                 roundness: float = 0,
                 color: tuple[int, int, int] = (0, 0, 0),
                 ) -> None:
        super().__init__(parent)

        self._is_determinate: bool = determinate
        self._center_on_parent: bool = center_on_parent
        self._disable_parent_when_running: bool = disable_parent_when_running

        if self._is_determinate:
            if minimum is None or maximum is None:
                print("Error: If is determinate must declare minimum and maximum values")
                sys.exit()
            self._minimum = minimum
            self._maximum = maximum

        self._color: QColor = QColor(color[0], color[1], color[2])
        self._minimum_trail_opacity: float = min_opacity
        self._trail_fade_percentage: float = fade
        self._number_of_lines: int = lines
        # self._line_length: int = line_length
        self._line_width: int = line_width
        self._roundness: float = roundness
        self._current_counter: int = 0

        self._bar_length = bar_length
        self._bar_height = bar_height

        self._current_value = 0
        self._percent_complete = 0.0

        # self._timer: QTimer = QTimer(self)
        # self._timer.timeout.connect(self._rotate)
        self._update_size()
        # self._update_timer()
        self.hide()

        self._update_position()
        # self._is_spinning = True
        self.show()

        # self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

    def paintEvent(self, _: QPaintEvent) -> None:
        """Paint the WaitingSpinner."""
        self._update_position()
        painter = QPainter(self)
        painter.fillRect(self.rect(), Qt.GlobalColor.transparent)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)
        if self._current_counter >= self._number_of_lines:
            self._current_counter = 0
        painter.setPen(Qt.PenStyle.NoPen)
        relative_number_of_lines = int(self._percent_complete * self._number_of_lines)
        for i in range(relative_number_of_lines):
            painter.save()

            # painter.translate(
            #     self._inner_radius + self._line_length,
            #     self._inner_radius + self._line_length,
            # )
            # rotate_angle = 360 * i / self._number_of_lines
            # painter.rotate(rotate_angle)
            # painter.translate(self._inner_radius, 0)
            pos = int((self.size().width() * self._percent_complete) * i / relative_number_of_lines)
            painter.translate(pos, 0)
            painter.rotate(90)

            distance = self._line_count_distance_from_primary(
                i, self._current_counter, self._number_of_lines
            )
            color = self._current_line_color(
                distance,
                self._number_of_lines,
                self._trail_fade_percentage,
                self._minimum_trail_opacity,
                self._color,
            )
            painter.setBrush(color)
            painter.drawRoundedRect(
                QRect(
                    0,
                    -self._line_width // 2,
                    self._bar_height,
                    self._line_width,
                ),
                self._roundness,
                self._roundness,
                Qt.SizeMode.RelativeSize,
            )
            painter.restore()

    def _update_size(self) -> None:
        """Update the size of the ProgressBar."""
        # size = (self._inner_radius + self._line_length) * 2
        # self.setFixedSize(size, size)
        if self._bar_length is not None:
            self.setFixedWidth(self._bar_length)

        if self._bar_height is not None:
            self.setFixedHeight(self._bar_height)

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

    def get_percent_complete(self):
        return self._percent_complete

    def set_value_by_percent(self, percent_complete: float):
        self._percent_complete = percent_complete
        self.repaint()

    def set_value(self, value: int):
        self._current_value = value
        self._recalculate_percent_complete()
        self.repaint()
