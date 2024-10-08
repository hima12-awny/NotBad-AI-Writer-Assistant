
from functionality.file_handlling import read_attr_from_settings
from gui_components.ai_windos.show_tasks_dashboard import *

from PySide6.QtGui import QFont, QShortcut
from PySide6.QtCore import Qt

from typing import Any

from gui_components.text_area import TextArea
from gui_components.ai_windos.ai_controls_section_widget import ControlsSectionWidget


class AIFeaturesWindow(QMainWindow):
    def __init__(self,
                 parent: QMainWindow | Any = None,
                 init_function_name=None,
                 selected_text=None,
                 just_open_window=False
                 ):
        """
        :param parent:
        :param init_function_name:
        :param selected_text:
        :param just_open_window:
        """

        super().__init__(parent=parent)

        self.function_name = init_function_name

        if init_function_name is None or just_open_window:
            self.function_name = read_attr_from_settings('last_ai_feature_opened')

        self.selected_text = selected_text
        self.output_result_text = None

        self.parent = parent
        self.parent.txtArea.selectionChangedConnect(self.update_in_text_window)

        self.init_opened = True
        self.ai_task_is_running = False

        self.ai_task_thread = None
        self.ai_task_worker = None

        self.in_txtArea = None

        self.setWindowTitle("AI Features")
        self.setMinimumSize(600, 600)

        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)

        # Create a central widget and set it
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # Create main layout
        self.main_layout = QVBoxLayout(central_widget)

        # Create controls section widget
        self.controls_section = ControlsSectionWidget(self, self.function_name, selected_text)

        # input and output text areas
        self.in_txtArea = TextArea(self, border_radius=10, blur_radius=10)

        self.in_txtArea.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.in_txtArea.setText(selected_text)

        self.in_label = QLabel(self)
        self.in_label.setText('Input')

        self.out_label = QLabel(self)
        self.out_label.setText('Output')

        self.out_txtArea = TextArea(self, border_radius=10, blur_radius=10)
        self.out_txtArea.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.out_txtArea.setText("waiting for generating")

        self.main_layout.addWidget(self.controls_section)
        self.main_layout.addWidget(self.in_label)
        self.main_layout.addWidget(self.in_txtArea)
        self.main_layout.addWidget(self.out_label)
        self.main_layout.addWidget(self.out_txtArea)

        # Set up font size management
        self.current_font_size = 12
        self.update_font_size()

        # Set up shortcuts
        self.setup_shortcuts()

        self.setup_menu_bar()

        if not just_open_window:
            self.generate_func()

        self.make_thread_for_ai_task = None

    def setup_shortcuts(self):
        from functionality.genral_actions import close_windows

        shortcuts = [
            [QShortcut('ctrl++', self), self.increase_font_size],
            [QShortcut('ctrl+-', self), self.decrease_font_size],

            [QShortcut('ctrl+g', self), self.generate_func],
            [QShortcut('ctrl+g', self.parent), self.generate_func],

            [QShortcut('ctrl+i', self), self.insert_outText_in_main_txtArea],
            [QShortcut('ctrl+i', self.parent), self.insert_outText_in_main_txtArea],

            [QShortcut('ctrl+shift+q', self), lambda: close_windows(self.parent)],

        ]
        for sc in shortcuts:
            sc[0].activated.connect(sc[1])

    def setup_menu_bar(self):
        from PySide6.QtWidgets import QMenuBar

        menu_bar = QMenuBar()

        api_key_menu = menu_bar.addMenu('API Key')
        api_key_menu.addAction("Set/Update API Key", self.set_api_key)

        tasks_menu = menu_bar.addMenu('Tasks')

        tasks_menu.addAction("Add Task", self.show_add_new_task)
        tasks_menu.addAction("Task Dashboard", self.show_task_dashboard)

        self.setMenuBar(menu_bar)

    def show_add_new_task(self):
        new_task_window = AddTaskWindow(self)
        new_task_window.show()

    def show_task_dashboard(self):
        task_dash_window = TaskDashboardWindow(self)
        task_dash_window.show()

    def set_api_key(self):
        from gui_components.set_ai_api_key import ApiKeyInputDialog

        api_key_response = ApiKeyInputDialog(self)
        api_key_response.exec()

        if api_key_response.finished:

            groq_api_key = read_attr_from_settings('groq_api_key')

            if not groq_api_key:
                self.out_txtArea.setText("You Should to put valid Api")
                return False
        else:
            self.out_txtArea.setText("You Should to put valid Api")
            return False

        return True

    def generate_func(self):

        in_text = self.in_txtArea.toPlainText()

        if in_text.strip() == "":
            return

        if self.ai_task_is_running:
            return

        api_key = read_attr_from_settings('groq_api_key')
        self.function_name = read_attr_from_settings('last_ai_feature_opened')

        if not api_key and self.function_name != 'Translate':
            is_valid_api = self.set_api_key()
            if not is_valid_api:
                return

        self.ai_task_is_running = True

        from functionality.threads_handler import make_thread_for_ai_task

        if self.function_name == 'Translate':
            from functionality.ai_tasks import translate_task

            dest_lang = read_attr_from_settings("Translate_attr")
            make_thread_for_ai_task(
                self,
                func=lambda: translate_task(in_text, dest_lang),
            )
            return

        ai_tools = read_ai_tools_dict()
        task = ai_tools[self.function_name]
        prompt: str = task["prompt"]

        if task['has_options']:
            option_value = read_attr_from_settings(self.function_name + '_attr')
            prompt = prompt.format(input_text=in_text, option=option_value)

        else:
            prompt = prompt.format(input_text=in_text)

        from functionality.ai_tasks import get_ai_results

        make_thread_for_ai_task(
            self,
            func=lambda: get_ai_results(prompt),
        )

    def insert_outText_in_main_txtArea(self):
        cursorWord = self.parent.txtArea.textCursor()
        cursorWord.insertText(self.out_txtArea.toPlainText() + " ")
        self.parent.txtArea.setFocus()

    def update_font_size(self):
        font = QFont()
        font.setPointSize(self.current_font_size)

        self.in_label.setFont(font)
        self.out_label.setFont(font)

    def increase_font_size(self):
        if self.current_font_size < 30:
            self.current_font_size += 2
            self.update_font_size()

    def decrease_font_size(self):
        if self.current_font_size > 14:  # Minimum font size to avoid becoming too small
            self.current_font_size -= 2
            self.update_font_size()

    def update_func_and_in_text(self, func_name, selected_text):

        self.function_name = read_attr_from_settings('last_ai_feature_opened')

        if self.function_name != func_name:
            self.controls_section.on_change_function_info(set_function_name=func_name)

        self.function_name = func_name

        self.selected_text = selected_text
        self.controls_section.selected_text = selected_text

        self.in_txtArea.setText(selected_text)

        self.generate_func()

    def track_selected_text(self, selected_text):
        self.in_txtArea.setText(selected_text)
        self.controls_section.selected_text = selected_text

    def update_in_text_window(self):

        selected_text = self.parent.txtArea.textCursor().selectedText()
        if selected_text:
            self.track_selected_text(selected_text)

    def closeEvent(self, event):

        self.parent.txtArea.selectionChangedDisconnect(self.update_in_text_window)
        self.parent.ai_features_window = None
