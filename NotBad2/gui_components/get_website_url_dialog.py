from PySide6.QtWidgets import (
    QApplication,
    QDialog,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout
)

from functionality.file_handlling import write_attr_to_settings


class GetUrlDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.cancel_button = None
        self.input_field = None
        self.label = None
        self.ok_button = None

        self.setWindowTitle("Enter Website URL")
        self.setFixedSize(400, 150)
        self.setStyleSheet(
            '''
            QDialog {
                background-color: #f2f2f2;
                border: 2px solid #c8c8c8;
            }
            QLabel {
                font-size: 14px;
                color: #333;
            }
            QLineEdit {
                font-size: 14px;
                padding: 5px;
                border: 1px solid #c8c8c8;
                border-radius: 5px;
            }
            QPushButton {
                font-size: 14px;
                padding: 5px 10px;
                border: 1px solid #c8c8c8;
                border-radius: 5px;
                background-color: #4CAF50; /* Green */
                color: white;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #3e8e41;
            }
            QPushButton#cancelButton {
                background-color: #f44336; /* Red */
            }
            QPushButton#cancelButton:hover {
                background-color: #da190b;
            }
            QPushButton#cancelButton:pressed {
                background-color: #c1170a;
            }
            '''
        )
        self.init_ui()

    def init_ui(self):
        # Create layout
        layout = QVBoxLayout(self)

        # Create label
        self.label = QLabel("Enter Valid Website URL:")
        layout.addWidget(self.label)

        # Create input field
        self.input_field = QLineEdit()

        self.input_field.setPlaceholderText('https://example.com')
        layout.addWidget(self.input_field)

        # Create buttons
        button_layout = QHBoxLayout()
        self.ok_button = QPushButton("OK")
        self.ok_button.clicked.connect(self.handle_ok)
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.setObjectName("cancelButton")
        self.cancel_button.clicked.connect(self.reject)

        button_layout.addWidget(self.ok_button)
        button_layout.addWidget(self.cancel_button)

        layout.addLayout(button_layout)

    def handle_ok(self):
        # Handle the OK button click
        self.accept()  # Close the dialog

    def get_url(self):
        return self.input_field.text()


# # Usage example
# if __name__ == "__main__":
#     import sys
#
#     app = QApplication(sys.argv)
#
#     dialog = GetUrlDialog()
#     if dialog.exec() == QDialog.Accepted:
#         url = dialog.get_url()
#         print(f"url: {url}")
#
#     dialog.close()
#     app.closeAllWindows()
