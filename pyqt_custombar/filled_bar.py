import sys
import math
from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import Qt, QTimer, QRect
from PyQt6.QtGui import QColor, QPainter, QPaintEvent, QPen, QBrush
from .parent_bar import ParentBar


class FilledBar(ParentBar):
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
        super().__init__(parent=parent,
                         minimum=minimum,
                         maximum=maximum,
                         center_on_parent=center_on_parent,
                         disable_parent_when_running=disable_parent_when_running,
                         bar_length=bar_length,
                         bar_height=bar_height,
                         color=color,
                         is_vertical=is_vertical)

        self._num_of_segs = None
        self._seg_width = None

    def paintEvent(self, _: QPaintEvent) -> None:
        """Paint the SegmentedBar."""
        self._update_position()

        self._paint_border()

        painter = QPainter(self)
        painter.fillRect(self.rect(), Qt.GlobalColor.transparent)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)

        painter.save()
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(self._color)

        if self._is_vertical:
            painter.drawRect(0, 0, self._bar_height, math.floor(self._bar_length * self.get_percent_complete()))
        else:
            painter.drawRect(0, 0, math.floor(self._bar_length * self.get_percent_complete()), self._bar_height)

        painter.restore()

        # distance = self._line_count_distance_from_primary(
        #     i, self._current_counter, self._number_of_lines
        # )
        # color = self._current_line_color(
        #     distance,
        #     self._number_of_lines,
        #     self._trail_fade_percentage,
        #     self._minimum_trail_opacity,
        #     self._color,
        # )
        # painter.restore()
