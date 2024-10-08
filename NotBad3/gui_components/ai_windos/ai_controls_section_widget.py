from PySide6.QtWidgets import QWidget, QMainWindow, QHBoxLayout
from functionality.file_handlling import write_attr_to_settings, read_attr_from_settings
from typing import Any
from gui_components.combobox_with_label_widget import ComboBoxLabel
from gui_components.button_widget import Button
from functionality.file_handlling import read_ai_tools_dict
from gui_components.input_number_widget import NumberInputWidget


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

        layout = QHBoxLayout(self)

        self.ai_tools = read_ai_tools_dict()
        tools_names = list(self.ai_tools.keys())

        self.function_info = ComboBoxLabel(
            label_text='Function',
            combo_box_items=tools_names,
            parent=self
        )
        self.function_info.set_value(self.function_name)

        self.function_info.value_changed(self.update_options_widget)

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

        # Placeholder for options widget
        self.options_widget = None
        self.update_options_widget()

        self.setLayout(layout)

    def update_function_info_list(self):
        self.ai_tools = read_ai_tools_dict()
        tools_names = list(self.ai_tools.keys())

        self.function_info.clear()
        self.function_info.addItems(tools_names)

        self.function_info.set_value(self.function_name)

    def on_change_function_info(self, set_function_name: str):
        self.function_name = set_function_name
        self.update_options_widget()

    def get_function_name(self):
        return self.function_info.get_value()

    def update_options_widget(self):

        self.function_name = self.get_function_name()

        write_attr_to_settings(
            attr_name='last_ai_feature_opened',
            attr_value=self.function_name)

        if self.options_widget:
            self.layout().removeWidget(self.options_widget)
            self.options_widget.deleteLater()
            self.options_widget = None

        self.options_widget = self.create_options_widget()
        if self.options_widget:
            self.options_widget.value_changed(self.update_option_attr)
            self.layout().addWidget(self.options_widget)

    def update_option_attr(self):

        write_attr_to_settings(
            self.function_name + '_attr',
            self.options_widget.get_value()
        )

    def create_options_widget(self):

        if not self.function_name:
            return

        option_widget = None
        task = self.ai_tools[self.function_name]
        has_option = task['has_options']
        if not has_option:
            return option_widget

        option_type = task['option_type']
        option_label = task['option_label']

        option_last_value = read_attr_from_settings(self.function_name + '_attr')
        if option_last_value is None:
            option_last_value = 0 if option_type == "number" else task['options'][0]

            write_attr_to_settings(
                self.function_name + '_attr',
                option_last_value
            )

        if option_type == 'number':
            option_widget = NumberInputWidget(
                label_text=option_label,
                parent=self,
                min_value=0,
                max_value=100,
            )

        elif option_type == "list":

            option_widget = ComboBoxLabel(
                label_text=option_label,
                combo_box_items=task['options'],
                parent=self
            )

        option_widget.set_value(option_last_value)

        return option_widget

    def update_all_inputs(self):

        self.ai_tools = read_ai_tools_dict()

        self.function_info.value_changed_disconnect(self.update_options_widget)

        self.function_info.clear()
        self.function_info.addItems(list(self.ai_tools.keys()))

        self.function_name = read_attr_from_settings('last_ai_feature_opened')
        self.function_info.set_value(self.function_name)

        self.update_options_widget()
        self.function_info.value_changed(self.update_options_widget)
