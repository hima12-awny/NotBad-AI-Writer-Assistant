from PySide6.QtWidgets import QMainWindow, QMessageBox
from typing import Any
import json

PATH_SETTING = "json_files/settings.json"
PATH_AI_TOOLS = r"K:\python\gui\qt\NotBad3\json_files\ai_tools.json"


def load_words(self):
    with open('words.txt', 'r') as file:
        words = file.read().split()

        for word in words:
            word_len = len(word)

            if word_len not in self.dict_of_all_sug_words:
                self.dict_of_all_sug_words[word_len] = []

            self.dict_of_all_sug_words[word_len].append(word)

            self.dict_of_all_sug_words_dict = {word: 1}

            # self.dict_of_all_sug_words = words


def open_file(self: QMainWindow | Any):
    from PySide6.QtWidgets import QFileDialog

    self.file_path, _ = QFileDialog.getOpenFileName(self, "Open File", "")

    if self.file_path:
        with open(self.file_path, 'r', encoding='utf-8') as file:
            text = file.read()

        self.contentFile = text

        self.txtArea.clear()

        self.txtArea.insertPlainText(self.contentFile)

        self.new_file_tag = 0
        self.setWindowTitle('NotBad - ' + self.file_path)

        # self.update_words_len()
        # self.update_line_column_num()


def new_file(self: QMessageBox | Any):
    if self.new_file_tag and self.txtArea.toPlainText() or \
            (not self.new_file_tag and self.txtArea.toPlainText() != self.contentFile):

        response = QMessageBox.question(self, 'Note', 'you haven\'t saved this file, you want to save it?',
                                        QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

        if response == QMessageBox.StandardButton.Yes:
            save_file(self)

    self.txtArea.clear()
    self.setWindowTitle('NotBad - New File')
    self.new_file_tag = 1


def save_file_with_dif_types(self: QMainWindow | Any, text):
    self.file_path = self.file_path + '.txt' \
        if not self.file_path.endswith('.txt') \
        else self.file_path

    with open(self.file_path, 'w', encoding='utf-8') as file:
        file.write(text)

    self.setWindowTitle('NotBad -' + self.file_path)
    self.new_file_tag = 0


def save_file(self):
    text = self.txtArea.toPlainText()

    if self.new_file_tag:
        from PySide6.QtWidgets import QFileDialog

        self.file_path, _ = QFileDialog.getSaveFileName(self, "Save File")

        if self.file_path and len(self.file_path) > 4:
            save_file_with_dif_types(self, text)

        else:
            self.setWindowTitle('NotBad - New file')
            self.new_file_tag = 1

    else:
        save_file_with_dif_types(self, text)

    self.contentFile = text


def read_attr_from_settings(attr_name):
    with open(PATH_SETTING, 'r') as file:
        data = file.read()

    data_dict: dict = json.loads(data)
    return data_dict.get(attr_name, None)


def write_attr_to_settings(attr_name, attr_value):
    with open(PATH_SETTING, 'r') as file:
        in_data = file.read()

    data_dict = json.loads(in_data)

    if attr_value == data_dict.get(attr_name, None):
        return

    data_dict[attr_name] = attr_value
    with open(PATH_SETTING, 'w') as file:
        file.write(json.dumps(data_dict))


def read_ai_tools_dict() -> dict:
    with open(PATH_AI_TOOLS, 'r') as file:
        data = file.read()

    ai_tools: dict = json.loads(data)
    return ai_tools


def write_ai_tools_dict(ai_tools: dict) -> None:
    with open(PATH_AI_TOOLS, 'w') as file:
        file.write(json.dumps(ai_tools))
