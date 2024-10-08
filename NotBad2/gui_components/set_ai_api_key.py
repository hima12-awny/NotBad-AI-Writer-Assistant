from PySide6.QtWidgets import QApplication, QDialog, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout
from functionality.file_handlling import write_attr_to_settings


class ApiKeyInputDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.cancel_button = None
        self.ok_button = None
        self.label = None
        self.input_field = None
        self.setWindowTitle("Enter API Key")
        self.setGeometry(100, 100, 500, 200)
        self.setFixedSize(500, 200)
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

        # Create label with hyperlink
        self.label = QLabel("To use AI features, you should enter your AI Groq API Key From "
                            "<a href='https://console.groq.com/keys'>groq.com</a>")
        self.label.setOpenExternalLinks(True)
        layout.addWidget(self.label)

        # Create input field
        self.input_field = QLineEdit()
        self.input_field.setEchoMode(QLineEdit.Password)  # To hide the API key
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
        input_api_key = self.input_field.text()
        write_attr_to_settings('groq_api_key', input_api_key)

        self.accept()  # Close the dialog

    def get_api_key(self):
        return self.input_field.text()


# Usage example
if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)

    dialog = ApiKeyInputDialog()
    if dialog.exec() == QDialog.Accepted:
        api_key = dialog.get_api_key()
        print(f"API Key: {api_key}")  # For testing purposes, don't print sensitive keys in real applications.

    dialog.close()
    app.closeAllWindows()
