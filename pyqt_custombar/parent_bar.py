import sys
import math
from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QColor


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

        if self._is_determinate:
            if minimum is None or maximum is None:
                print("Error: If is determinate must declare minimum and maximum values")
                sys.exit()
            self._minimum = minimum
            self._maximum = maximum

        self._color: QColor = QColor(color[0], color[1], color[2])
        self._bar_length = bar_length
        self._bar_height = bar_height

        self._current_value = 0
        self._percent_complete = 0.0

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
                self.setFixedHeight(self._bar_length)
            else:
                self._bar_length = self.size().height()

            if self._bar_height is not None:
                self.setFixedWidth(self._bar_height)
            else:
                self._bar_height = self.size().width()
        else:
            if self._bar_length is not None:
                self.setFixedWidth(self._bar_length)
            else:
                self._bar_length = self.size().width()

            if self._bar_height is not None:
                self.setFixedHeight(self._bar_height)
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
