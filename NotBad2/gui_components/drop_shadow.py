from PySide6.QtGui import QColor
from PySide6.QtWidgets import QGraphicsDropShadowEffect


class DropShadow(QGraphicsDropShadowEffect):

    def __init__(self, parent=None, blur_radius=30, x=0, y=0):

        super().__init__(parent)
        self.setBlurRadius(blur_radius)
        self.setColor(QColor(0, 0, 0, int(255 * .3)))
        self.setOffset(x, y)
