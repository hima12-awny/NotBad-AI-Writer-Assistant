import googletrans
from PySide6.QtWidgets import QWidget, QMainWindow, QHBoxLayout
from functionality.file_handlling import write_attr_to_settings, read_attr_from_settings
from typing import Any
from gui_components.combobox_with_label import ComboBoxLabel
from gui_components.button import Button
from functionality.ai_tasks import all_tasks_functions


class ControlsSectionWidget(QWidget):

    def __init__(self,
                 parent: QMainWindow | Any = None,
                 init_function_name=None,
                 selected_text=None):

        super().__init__(parent)

        self.selected_text = selected_text
        self.parent = parent

        self.function_name = init_function_name

        if self.function_name:
            write_attr_to_settings('last_ai_feature_opened', self.function_name)
        else:
            self.function_name = read_attr_from_settings('last_ai_feature_opened')

        self.function_constraints = None

        layout = QHBoxLayout(self)

        self.function_info = ComboBoxLabel(
            label_text='Function',
            combo_box_items=list(all_tasks_functions.keys()),
            parent=self
        )

        self.function_info.setCurrentText(self.function_name)
        self.function_info.currentTextChanged(self.on_change_function_info)

        self.all_optional_infos: dict[str, dict[str, any]] = {
            'Translate':
                {
                    'showInfo': lambda: self.select_info_options(
                        'Translate',
                        'Destination Lang',
                        options=googletrans.LANGCODES
                    ),
                    'info': None
                },

            'Check Grammar/Spelling':
                {
                    'showInfo': lambda: self.select_info_options(
                        'Check Grammar/Spelling',
                        None,
                        None
                    ),
                    'info': None
                },

            'Arrange In Blots':
                {
                    'showInfo': lambda: self.select_info_options(
                        'Arrange In Blots',
                        'Max # of Dots',
                        options=list(map(lambda x: str(x), reversed(range(2, 100))))
                    ),
                    'info': None
                },

            'Arrange In Steps':
                {
                    'showInfo': lambda: self.select_info_options(
                        'Arrange In Steps',
                        'Max # of Steps',
                        options=list(map(lambda x: str(x), reversed(range(1, 100))))
                    ),
                    'info': None
                },

            'Suitable Title':
                {
                    'showInfo': lambda: self.select_info_options(
                        'Suitable Title',
                        'Select Tone',
                        options=[
                            "Formal", "Casual", "Humorous", "Technical", "Poetic", "Persuasive",
                            "Satirical", "Scholarly", "Conversational", "Narrative"]
                    ),
                    'info': None
                },

            'Summarize':
                {
                    'showInfo': lambda: self.select_info_options(
                        'Summarize',
                        'Select Max Words',
                        options=[
                            str(i) for i in
                            reversed(range(1, self.selected_text.count(' ') + 1))
                        ] if self.selected_text else ['0']
                    ),
                    'info': None
                },

            'Expand':
                {
                    'showInfo': lambda: self.select_info_options(
                        'Expand',
                        'Max Approximate Lines',
                        options=[
                            str(i) for i in
                            reversed(range(2, 500))
                        ]
                    ),
                    'info': None
                },

            'Rephrase':
                {
                    'showInfo': lambda: self.select_info_options(
                        'Rephrase',
                        'Select Tone',
                        options=[
                            "Formal", "Casual", "Humorous", "Technical", "Poetic", "Persuasive",
                            "Satirical", "Scholarly", "Conversational", "Narrative"]
                    ),
                    'info': None
                },
        }

        self.generate_button = Button(
            'Generate',
            self,
            self.parent.generate_func)

        self.insert_button = Button(
            'Insert',
            self,
            self.parent.insert_outText_in_main_txtArea)

        layout.addWidget(self.generate_button)
        layout.addWidget(self.insert_button)
        layout.addWidget(self.function_info)

        self.all_optional_infos[self.function_name]['showInfo']()

        self.setLayout(layout)

    def on_change_function_info(self, set_function_name=None):

        self.function_name = ''
        if set_function_name:
            self.function_name = set_function_name
            self.function_info.setCurrentText(self.function_name)
        else:
            self.function_name = self.function_info.get_value()

        write_attr_to_settings('last_ai_feature_opened', self.function_name)

        for func_name, info in self.all_optional_infos.items():
            if func_name == self.function_name:
                info['showInfo']()
            else:
                if info['info'] is not None:
                    info['info'].hide()
                    self.layout().removeWidget(info['info'])
                    info['info'] = None

    def on_change_constants(self):

        write_attr_to_settings(
            f'{self.function_name}_attr',
            self.all_optional_infos[self.function_name]['info'].get_value())

        if self.function_name == "Translate" and self.parent.in_txtArea is not None:
            self.parent.generate_func()

    def select_info_options(self, function_name, label_text, options):

        if (
                function_name not in ['Check Grammar/Spelling'] and
                self.all_optional_infos[function_name]['info'] is None
        ):

            self.all_optional_infos[function_name]['info'] = ComboBoxLabel(
                label_text=label_text,
                combo_box_items=options,
                parent=self
            )

            self.all_optional_infos[function_name]['info'].currentTextChanged(
                self.on_change_constants
            )

            last_attr_value = read_attr_from_settings(f'{function_name}_attr')
            if last_attr_value and function_name != 'Summarize':
                self.all_optional_infos[function_name]['info'].set_init_value(last_attr_value)

            self.layout().addWidget(self.all_optional_infos[function_name]['info'])
