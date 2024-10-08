from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QComboBox


class ComboBoxLabel(QWidget):
    def __init__(self, label_text, combo_box_items, parent=None):
        super().__init__(parent)

        self.function_section_layout = QVBoxLayout(self)

        # Add a label above the combobox
        label = QLabel(label_text, self)
        self.function_section_layout.addWidget(label)

        # Create a dropdown menu (QComboBox)
        self.dropdown = QComboBox(self)

        self.dropdown.addItems(combo_box_items)
        self.function_section_layout.addWidget(self.dropdown)

        self.dropdown.setStyleSheet(
            '''
           QComboBox {
                border-radius: 5px;  /* Rounded corners */
                padding: 5px;
                font-size: 14px;
            }
            '''
        )

        self.setLayout(self.function_section_layout)

    def get_value(self):
        return self.dropdown.currentText()

    def value_changed(self, callback):
        self.dropdown.currentTextChanged.connect(callback)

    def value_changed_disconnect(self, callback):
        self.dropdown.currentTextChanged.disconnect(callback)

    def set_value(self, value):
        self.dropdown.setCurrentText(value)

    def clear(self):
        self.dropdown.clear()

    def addItems(self, items):
        self.dropdown.addItems(items)
