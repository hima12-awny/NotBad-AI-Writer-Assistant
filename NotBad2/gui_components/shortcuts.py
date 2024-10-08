from PySide6.QtGui import QShortcut
from PySide6.QtWidgets import QMainWindow
from typing import Any

from functionality.file_handlling import (
    save_file,
    open_file,
    new_file
)
from functionality.genral_actions import read_load, close_windows
from functionality.ai_features_window_actions import open_and_run_ai_task, open_ai_window


def add_shortcuts_main_window(self: QMainWindow | Any):
    shortcuts = [
        [QShortcut('ctrl+s', self), lambda: save_file(self)],
        [QShortcut('ctrl+o', self), lambda: open_file(self)],
        [QShortcut('ctrl+n', self), lambda: new_file(self)],

        [QShortcut("alt+e", self), lambda: self.sug_words_options.add_suggested_word(self, True)],

        [QShortcut('alt+up', self), lambda: self.sug_words_options.switch_focus(self)],
        [QShortcut('alt+down', self), lambda: self.sug_words_options.switch_focus(self)],

        [QShortcut('ctrl+r', self), lambda: read_load(self)],
        [QShortcut('ctrl+t', self), lambda: open_and_run_ai_task(self, "Translate")],

        [QShortcut('ctrl+shift+a', self), lambda: open_ai_window(
            self,
            selected_text=self.txtArea.textCursor().selectedText(),
            just_open_window=True
        )],
        [QShortcut('ctrl+shift+q', self), lambda: close_windows(self)],

    ]
    for sc in shortcuts:
        sc[0].activated.connect(sc[1])
