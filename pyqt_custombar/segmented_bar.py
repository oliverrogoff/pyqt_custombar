import sys
import math
from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import Qt, QTimer, QRect
from PyQt6.QtGui import QColor, QPainter, QPaintEvent
from .parent_bar import ParentBar


class SegmentedBar(ParentBar):
    def __init__(self,
                 parent: QWidget,
                 minimum: int = None,
                 maximum: int = None,
                 center_on_parent: bool = True,
                 disable_parent_when_running: bool = False,
                 bar_length: int = None,
                 bar_height: int = None,
                 color: tuple[int, int, int] = (0, 0, 0),
                 is_vertical: bool = False,
                 segment_width: int = 10,
                 segment_spacing: int = 2,
                 segment_roundness: float = 0.0
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
        self._target_seg_width = segment_width
        self._seg_spacing = segment_spacing
        self._set_number_of_segs()

        self._seg_roundness = segment_roundness

    def paintEvent(self, _: QPaintEvent) -> None:
        """Paint the SegmentedBar."""
        self._update_position()
        painter = QPainter(self)
        painter.fillRect(self.rect(), Qt.GlobalColor.transparent)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)

        # if self._current_counter >= self._number_of_lines:
        #     self._current_counter = 0

        painter.setPen(Qt.PenStyle.NoPen)
        num_of_filled_segs = int(self._percent_complete * self._num_of_segs)
        for i in range(num_of_filled_segs):
            painter.save()
            seg_pos = (self._seg_width + self._seg_spacing) * i
            painter.setBrush(self._color)
            if self._is_vertical:
                painter.translate(0, self._bar_length - seg_pos)
                painter.drawRoundedRect(
                    QRect(
                        0,
                        0,
                        self._bar_height,
                        -self._seg_width
                    ),
                    self._seg_roundness,
                    self._seg_roundness,
                    Qt.SizeMode.RelativeSize,
                )
            else:
                painter.translate(seg_pos, 0)
                painter.drawRoundedRect(
                    QRect(
                        0,
                        0,
                        self._seg_width,
                        self._bar_height,
                    ),
                    self._seg_roundness,
                    self._seg_roundness,
                    Qt.SizeMode.RelativeSize,
                )

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
            painter.restore()

    def _set_number_of_segs(self):
        self._num_of_segs = round(self._bar_length / (self._target_seg_width + self._seg_spacing))
        self._seg_width = int((self._bar_length - (self._num_of_segs * self._seg_spacing)) / self._num_of_segs)
