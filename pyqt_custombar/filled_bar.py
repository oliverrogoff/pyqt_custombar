import math
from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import Qt, QRectF
from PyQt6.QtGui import QPainter, QPaintEvent
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
                 background_color: tuple[int, int, int] = (-1, -1, -1),
                 border_width: int = 2,
                 border_roundness: float = 0.6,
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
                         background_color=background_color,
                         border_width=border_width,
                         border_roundness=border_roundness,
                         is_vertical=is_vertical)

    def paintEvent(self, _: QPaintEvent) -> None:
        """Paint the SegmentedBar."""
        self._update_position()
        self._update_border()
        self._paint_background()

        painter = QPainter(self)
        painter.fillRect(self.rect(), Qt.GlobalColor.transparent)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)

        painter.save()
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(self._color)

        painter.setClipPath(self._border_path, Qt.ClipOperation.ReplaceClip)

        if self._is_vertical:
            painter.drawRect(QRectF(
                    self._border_width,
                    self._bar_length + self._border_width,
                    self._bar_height,
                    -math.floor(self._bar_length * self.get_percent_complete())
                ))
        else:
            painter.drawRect(QRectF(
                    self._border_width,
                    self._border_width,
                    math.floor(self._bar_length * self.get_percent_complete()),
                    self._bar_height,
                ))

        painter.restore()
        self._paint_border()
