# pyqt_custombar

## Widgets
The pyqt_custombar package has 2 progress bar widgets, FilledBar and SegmentedBar.
They both inherent from the base class ParentBar which inherits the PyQt6 QWidget class.

### Shared Parameters
The parameters that both progress bar widgets have in common are as follows:
- parent
  - type: `QWidget`
  - the parent widget to the progress bar
  - no default value
- minimum
  - type: `int`
  - optional, if it is not `None` it is required that you also pass in a value for maximum
  - if it is not `None`, the progress bars progress is updated with the method `set_value(value: int)`
  - default value: `None`
- maximum
  - type: `int`
  - optional, if it is not `None` it is required that you also pass in a value for minimum
  - if it is not `None`, the progress bars progress is updated with the method `set_value(value: int)`
  - default value: `None`
- center_on_parent
  - type: `bool`
  - if `True`, the progress bar will center itself on the parent widget
  - default value: `True`
- disable_parent_while_running
  - type: `bool`
  - if `True`, the bar will attempt to disable user interaction with the parent widget while the progress bar is running
  - default value: `False`
- bar_length
  - type: `int`
  - the length of the progress bar
- bar_height
  - type: `int`
  - the height (or thickness) of the progress bar
-color
  - type: `tuple[int, int, int]`
  - the color of the progress bar (filled portion) in RBG format
  - default: `(0, 0, 0)`
- background_color
  - type `tuple[int, int, int]`
  - the background color of the progress bar (unfilled portion) in RBG format
  - if you pass in `None`, the unfilled portion of the bar will be empty (transparent)
  - if you pass in `(-1, -1, -1)`, the color will be automatically assigned as a lighter hue of the bars color
  - default: `(-1, -1, -1)`
- border_width
  - type: `int`
  - the width of the outline of the progress bar
  - if you pass in `0`, there will be no outline of the bar
  - default: `0`
- border_roundness
  - type: `float`
  - must enter value between `0.0` and `1.0`
  - the higher the value, the more rounded the edges of the progress bar will be
  - default: `0.5`
- is_vertical
  - type: `bool`
  - if `True`, the progress bar will be oriented vertically, if `False` it will be oriented horizontally (normal)
  - default: `False`

### FilledBar
The FilledBar class can be imported with the statement `from pyqt_custombar import FilledBar`.

```python
from PyQt6.QtWidgets import QWidget
from pyqt_custombar import FilledBar

widget = QWidget()
bar = FilledBar(
    widget,
    minimum=0,
    maximum=1000,
    center_on_parent=True,
    disable_parent_when_running=False,
    bar_length=250,
    bar_height=20,
    color=(137, 49, 19),
    background_color=(-1, -1, -1),
    border_width=0,
    border_roundness=1.0,
    is_vertical=False
)
```

### SegmentedBar
The FilledBar class can be imported with the statement `from pyqt_custombar import SegmentedBar`.
SegmentedBar has extra parameters:
- segment_width
  - type: `int`
  - the desired width of each segment in the bar (will not be exact, the program adjusts 
it to evenly fill the bar's length)
  - default: `10`
- segment_spacing
  - type: `int`
  - the desired width of the space between each segment in the bar 
(will not be exact, the program adjusts it to evenly fill the bar's length)
  - default: `2`
- segment_roundness
  - type: float
  - must enter value between `0.0` and `1.0`
  - the higher the value, the more rounded each segment will be
  - default: `0.0`

```python
from PyQt6.QtWidgets import QWidget
from pyqt_custombar import SegmentedBar

widget = QWidget()
bar = SegmentedBar(
    widget,
    minimum=0,
    maximum=1000,
    center_on_parent=True,
    disable_parent_when_running=False,
    bar_length=250,
    bar_height=20,
    color=(137, 49, 19),
    background_color=(-1, -1, -1),
    border_width=0,
    border_roundness=1.0,
    is_vertical=False,
    segment_width=20,
    segment_spacing=2,
    segment_roundness=0.0
)
```
