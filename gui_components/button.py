from PySide6.QtWidgets import QPushButton


class Button(QPushButton):
    def __init__(self, text, parent=None, callback=None):

        super().__init__(text, parent)

        self.default_style = """
            QPushButton {
                background-color: #D3D3D3;  /* Light gray */
                color: black;
                padding: 10px 25px;
                display: inline-block;
                font-size: 16px;
                border-radius: 10px;  /* Rounded corners */
                font-family: Arial, sans-serif; /* Optional: Set a specific font */
                border: none; /* Remove border */
            }
            QPushButton:pressed {
                background-color: #B0B0B0;  /* Slightly darker gray for pressed state */
            }
        """

        self.disabled_style = """
            QPushButton {
                background-color: #FFCCCC;  /* Light red for disabled state */
                color: black;
                padding: 10px 25px;
                display: inline-block;
                font-size: 16px;
                border-radius: 10px;  /* Rounded corners */
                font-family: Arial, sans-serif; /* Optional: Set a specific font */
                border: none; /* Remove border */
            }
        """

        self.setStyleSheet(self.default_style)
        self.pressed.connect(callback)

    def disable_button(self):
        self.setEnabled(False)
        self.setStyleSheet(self.disabled_style)

    def enable_button(self):
        self.setEnabled(True)
        self.setStyleSheet(self.default_style)
