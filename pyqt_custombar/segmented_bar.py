import math
from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import Qt, QRect
from PyQt6.QtGui import QPainter, QPaintEvent
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
                 border_width: int = 2,
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
                         border_width=border_width,
                         is_vertical=is_vertical)

        self._num_of_segs = None
        self._seg_width = None
        self._extra_room = None
        self._target_seg_width = segment_width
        self._seg_spacing = segment_spacing
        self._set_number_of_segs()

        self._seg_roundness = segment_roundness

    def paintEvent(self, _: QPaintEvent) -> None:
        """Paint the SegmentedBar."""
        self._update_position()

        self._paint_border()

        painter = QPainter(self)
        painter.fillRect(self.rect(), Qt.GlobalColor.transparent)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)

        painter.setPen(Qt.PenStyle.NoPen)
        num_of_filled_segs = int(self._percent_complete * self._num_of_segs)
        for i in range(num_of_filled_segs):
            painter.save()
            seg_pos = (self._seg_width + self._seg_spacing) * i

            if i < self._extra_room:
                seg_pos += i
                current_seg_width = self._seg_width + 1
            else:
                seg_pos += self._extra_room
                current_seg_width = self._seg_width

            painter.setBrush(self._color)
            if self._is_vertical:
                painter.translate(math.ceil(self._border_width / 2), self._bar_length - seg_pos + math.ceil(self._border_width / 2))
                painter.drawRoundedRect(
                    QRect(
                        0,
                        0,
                        self._bar_height,
                        -current_seg_width
                    ),
                    self._seg_roundness,
                    self._seg_roundness,
                    Qt.SizeMode.RelativeSize,
                )
            else:
                painter.translate(seg_pos + math.ceil(self._border_width / 2), math.ceil(self._border_width / 2))
                painter.drawRoundedRect(
                    QRect(
                        0,
                        0,
                        current_seg_width,
                        self._bar_height,
                    ),
                    self._seg_roundness,
                    self._seg_roundness,
                    Qt.SizeMode.RelativeSize,
                )

            painter.restore()

    def _set_number_of_segs(self):
        self._num_of_segs = round((self._bar_length + self._seg_spacing) / (self._target_seg_width + self._seg_spacing))
        self._seg_width = math.floor((self._bar_length - (self._num_of_segs * self._seg_spacing - self._seg_spacing)) / self._num_of_segs)
        self._extra_room = self._bar_length - (self._num_of_segs * self._seg_spacing - self._seg_spacing) - (self._num_of_segs * self._seg_width)
