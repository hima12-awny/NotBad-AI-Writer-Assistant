from PySide6.QtWidgets import QWidget


class NumberInputWidget(QWidget):
    def __init__(
            self,
            label_text: str,
            min_value: int = 0,
            max_value: int = 100,
            parent=None
    ):
        """
        Initialize a widget that includes a label and a spin box for number input.

        :param label_text: The text to display on the label.
        :param min_value: Minimum value for the spin box.
        :param max_value: Maximum value for the spin box.
        :param parent: Parent widget (if any).
        """
        super().__init__(parent)

        from PySide6.QtWidgets import QLabel, QSpinBox, QVBoxLayout

        # Create the layout
        layout = QVBoxLayout(self)

        # Create and add the label
        self.label = QLabel(label_text, self)
        layout.addWidget(self.label)

        # Create and add the spin box for number input
        self.number_input = QSpinBox(self)
        self.number_input.setRange(min_value, max_value)  # Set the range for the spin box

        self.number_input.setStyleSheet(
            '''
           QComboBox {
                border-radius: 5px;  /* Rounded corners */
                padding: 5px;
                font-size: 14px;
            }
            '''
        )
        layout.addWidget(self.number_input)

        # Set the layout for the widget
        self.setLayout(layout)

    def get_value(self):
        """
        Get the current value from the spin box.

        :return: The current value of the spin box.
        """
        return self.number_input.value()

    def set_value(self, value: int):
        """
        Set the value of the spin box.

        :param value: The value to set in the spin box.
        """

        self.number_input.setValue(int(value))

    def value_changed(self, callback):
        self.number_input.valueChanged.connect(callback)
