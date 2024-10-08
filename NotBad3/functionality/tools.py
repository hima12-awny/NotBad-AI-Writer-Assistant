# from PySide6.QtWidgets import QLabel
# from PySide6.QtCore import Signal, Qt
#
#
# class ClickableLabel(QLabel):
#     clicked = Signal()
#
#     def __init__(self, text, parent=None):
#         super().__init__(text, parent)
#         # Set the cursor to a pointing hand
#         self.setCursor(Qt.CursorShape.PointingHandCursor)
#
#     def mouseReleaseEvent(self, event):
#         # Emit a signal with the label text as the argument
#         self.clicked.emit()
