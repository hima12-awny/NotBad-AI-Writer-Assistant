from PySide6.QtWidgets import (
    QMainWindow,
    QVBoxLayout,
    QWidget,
    QLabel,
    QLineEdit,
    QComboBox,
    QPushButton,
    QTextEdit,
    QMessageBox,
    QCheckBox,
    QListWidget,
    QHBoxLayout,
    QListWidgetItem,
)

from functionality.file_handlling import read_ai_tools_dict


class AddTaskWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.task_name_str: str | None = None
        self.task_label_str: str | None = None
        self.has_options_bool: bool | None = None
        self.option_type_str: str | None = None
        self.task_prompt_str: str | None = None
        self.options_list: list[str] | None = None

        self.parent = parent
        self.setWindowTitle("Task Creator")
        self.setGeometry(100, 100, 600, 500)

        # Main widget and layout
        self.main_widget = QWidget(self)
        self.setCentralWidget(self.main_widget)
        self.layout = QVBoxLayout(self.main_widget)

        # Task Name input
        self.task_name_input = QLineEdit(self)
        self.task_name_input.setPlaceholderText("Enter Task Name")
        self.layout.addWidget(QLabel("Task Name:"))
        self.layout.addWidget(self.task_name_input)

        self.task_label_input = QLineEdit(self)
        self.task_label_input.setPlaceholderText("Enter Task Label")
        self.layout.addWidget(QLabel("Task Label:"))
        self.layout.addWidget(self.task_label_input)

        # Checkbox to indicate if the task has options
        self.has_options_checkbox = QCheckBox("This task has options", self)
        self.layout.addWidget(self.has_options_checkbox)

        # Option Type and Label Column
        self.option_type_label_layout = QVBoxLayout()

        self.option_type_combo = QComboBox(self)
        self.option_type_combo.addItems(["number", "list"])
        self.option_type_label_layout.addWidget(QLabel("Option Type:"))
        self.option_type_label_layout.addWidget(self.option_type_combo)

        self.option_value_input = QLineEdit(self)
        self.option_value_input.setPlaceholderText("Enter option value")
        self.add_option_button = QPushButton("Add Option", self)
        self.add_option_button.clicked.connect(self.add_option)

        self.option_type_label_layout.addWidget(QLabel("Option Label:"))
        self.option_type_label_layout.addWidget(self.option_value_input)
        self.option_type_label_layout.addWidget(self.add_option_button)

        # Option Values Column
        self.option_values_layout = QVBoxLayout()

        self.option_list_widget = QListWidget(self)
        self.remove_option_button = QPushButton("Remove Selected Option", self)
        self.remove_option_button.clicked.connect(self.remove_option)

        self.option_values_layout.addWidget(QLabel("Option Values:"))
        self.option_values_layout.addWidget(self.option_list_widget)
        self.option_values_layout.addWidget(self.remove_option_button)

        # Horizontal Layout to combine two columns
        self.options_layout = QHBoxLayout()
        self.options_layout.addLayout(self.option_type_label_layout)
        self.options_layout.addLayout(self.option_values_layout)

        self.layout.addLayout(self.options_layout)

        # Input Text area
        self.task_prompt = QTextEdit(self)
        self.task_prompt.setFixedHeight(200)

        self.task_prompt.setPlaceholderText("Enter Task Prompt...")
        self.layout.addWidget(QLabel("Task Prompt:"))
        self.layout.addWidget(self.task_prompt)

        # Info text below Input Text
        self.info_text = QLabel(
            "Constraints:\n"
            "- The text should be relevant and comprehensive.\n"
            "- Use only English and avoid including any other languages.\n"
            "- You must include {input_text} as the user input text that will be processed.\n"
            "- If the Task has Options, you must include {option} in your prompt.\n",
            self
        )
        self.info_text.setWordWrap(True)
        self.layout.addWidget(self.info_text)

        # Button to create task
        self.create_task_button = QPushButton("Create Task", self)
        self.create_task_button.clicked.connect(self.create_task)
        self.layout.addWidget(self.create_task_button)

        self.ai_tools = read_ai_tools_dict()

        # Apply styles
        self.apply_styles()

    def apply_styles(self):
        # Style for input fields
        input_style = """
            QLineEdit, QTextEdit, QComboBox, QCheckBox {
                padding: 8px;
                font-size: 14px;
                border: 2px solid #ccc;
                border-radius: 5px;
                background-color: #f9f9f9;
            }
            QLineEdit:focus, QTextEdit:focus, QComboBox:focus, QCheckBox:focus {
                border-color: #5e9ed6;
            }
            QListWidget {
                padding: 8px;
                border: 2px solid #ccc;
                border-radius: 5px;
            }
        """
        # Style for labels
        label_style = """
            QLabel {
                font-size: 14px;
                font-weight: bold;
                margin-bottom: 5px;
            }
        """
        # Style for button
        button_style = """
            QPushButton {
                padding: 10px 20px;
                font-size: 14px;
                background-color: #5e9ed6;
                color: white;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #3d7bbf;
            }
        """
        # Apply styles
        self.setStyleSheet(input_style + label_style + button_style)

        # # Font for the whole application
        # app_font = QFont("Arial", 10)
        # QApplication.instance().setFont(app_font)

    def add_option(self):
        value = self.option_value_input.text().strip()
        if value:
            self.option_list_widget.addItem(QListWidgetItem(value))
            self.option_value_input.clear()
        else:
            QMessageBox.warning(self, "Input Error", "Please enter an option value to add!")

    def remove_option(self):
        selected_items = self.option_list_widget.selectedItems()
        if selected_items:
            for item in selected_items:
                self.option_list_widget.takeItem(self.option_list_widget.row(item))
        else:
            QMessageBox.warning(self, "Selection Error", "Please select an option to remove!")

    def create_task(self):
        # Retrieve inputs
        self.task_name_str = self.task_name_input.text().strip()
        self.task_label_str = self.task_label_input.text().strip()
        self.has_options_bool = self.has_options_checkbox.isChecked()
        self.option_type_str = self.option_type_combo.currentText()
        self.task_prompt_str = self.task_prompt.toPlainText().strip()

        # Collect option values
        self.options_list = [self.option_list_widget.item(i).text()
                             for i in range(self.option_list_widget.count())] if self.has_options_bool else []

        if not self.validate_inputs_values():
            return

        new_task = {
            "task_name": self.task_name_str,
            "prompt": self.task_prompt_str,
            "has_options": self.has_options_bool,
            "option_type": self.option_type_str,
            "options": self.options_list,
            "option_label": self.task_label_str,
        }

        self.ai_tools[self.task_name_str] = new_task

        from functionality.file_handlling import write_ai_tools_dict

        write_ai_tools_dict(self.ai_tools)

        # Display the created task in a message box
        QMessageBox.information(self, "Task Created", f"Task '{self.task_name_str}' Created Successfully!")

        self.update_parent_control()

    def update_parent_control(self):
        self.parent.controls_section.update_function_info_list()

    def validate_inputs_values(self) -> bool:

        if self.task_name_str and self.task_name_str in self.ai_tools:
            QMessageBox.warning(self, "Input Error", "This Task Already Exists!")
            return False

        # Validate inputs
        if not self.task_name_str or not self.task_prompt or not self.task_label_str:
            QMessageBox.warning(self, "Input Error", "Please fill all fields!")
            return False

        if self.has_options_bool and self.option_type_str == 'list' and not self.options_list:
            QMessageBox.warning(self, "Input Error", "Please add at least one option!")
            return False

        if self.has_options_bool and self.option_type_str not in ["number", "list"]:
            QMessageBox.warning(self, "Input Error", "Please select a valid option type!")
            return False

        if self.has_options_bool and self.option_type_str == "list" and not self.options_list[0].isalpha():
            QMessageBox.warning(self, "Input Error", "Please enter a valid list for the option!")
            return False

        if self.task_prompt_str.count("{input_text}") != 1:
            QMessageBox.warning(self, "Input Error", "Please include \"{input_text}\" in your prompt!")
            return False

        if self.has_options_bool and self.task_prompt_str.count("{option}") != 1:
            QMessageBox.warning(self, "Input Error", "Please include \"{option}\" in your prompt!")
            return False

        return True
