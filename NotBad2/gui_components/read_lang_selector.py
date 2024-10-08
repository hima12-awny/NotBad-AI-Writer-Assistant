from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QComboBox, QDialogButtonBox
from gtts.lang import tts_langs
from functionality.file_handlling import write_attr_to_settings


class LanguageSelectorDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.comboBox = None
        self.label = None
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Select Language')

        # Set up the main layout
        layout = QVBoxLayout(self)

        # Create a label
        self.label = QLabel("Select a language:", self)
        layout.addWidget(self.label)

        # Create a combo box
        self.comboBox = QComboBox(self)

        # Fetch languages from gtts and add them to the combo box
        languages = tts_langs()
        for lang_code, lang_name in languages.items():
            self.comboBox.addItem(f"{lang_name} ({lang_code})", lang_code)

        layout.addWidget(self.comboBox)

        # Button box with OK and Cancel buttons
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

        # Connect the combo box change event to a function
        self.comboBox.currentIndexChanged.connect(self.on_language_changed)

    def on_language_changed(self):
        # Get selected language code
        language_code = self.comboBox.currentData()
        # Update label with the selected language code
        self.label.setText(f"Selected Language Code: {language_code}")

    def get_selected_language(self):
        # Return the selected language code
        return self.comboBox.currentData()

    def accept(self):
        # Write selected language to settings before accepting the dialog
        language_code = self.get_selected_language()
        write_attr_to_settings("read_lang_code", language_code)
        super().accept()

    def reject(self):
        # Handle rejection (optional)
        super().reject()

# Example usage:
# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     dialog = LanguageSelectorDialog()
#     if dialog.exec() == QDialog.Accepted:
#         selected_language = dialog.get_selected_language()
#         print(f"Selected Language Code: {selected_language}")
#     sys.exit(app.exec())
