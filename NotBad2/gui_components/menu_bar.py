from PySide6.QtWidgets import QMenuBar, QMainWindow, QMenu
from PySide6.QtGui import QAction
from gui_components.drop_shadow import DropShadow
from functools import partial
from functionality.file_handlling import open_file, save_file, new_file, Any
from gui_components.word_assistant_menu import WordAssistantMenu
from functionality.genral_actions import select_read_language
from functionality.get_website_content import get_website_content
from functionality.genral_actions import read_load
from functionality.ai_features_window_actions import open_and_run_ai_task


class MenuBar(QMenuBar):
    def __init__(self, parent: QMainWindow | Any):
        super().__init__(parent)

        self.parent = parent

        self.setObjectName("MenuBar")
        self.setStyleSheet(
            '''
            QMenuBar{
                background-color:#fff;
            }
            ''')
        self.setGraphicsEffect(DropShadow(self, 10))
        parent.setMenuBar(self)

        self.menu_file = self.addMenu("File")
        actions_file = [
            [QAction("Open", self), partial(open_file, parent)],
            [QAction("New", self), partial(new_file, parent)],
            [QAction("Save", self), partial(save_file, parent)],
        ]
        for action in actions_file:
            action[0].triggered.connect(action[1])
            self.menu_file.addAction(action[0])

        self.addMenu(self.menu_file)
        ############################

        #  word assistant menu
        self.addMenu(WordAssistantMenu(parent))

        # Read Menu
        self.menu_read = self.addMenu("Read")

        # Read action
        parent.action_read_load = QAction('Start Read', self)
        parent.action_read_load.triggered.connect(lambda: read_load(parent))
        self.menu_read.addAction(parent.action_read_load)

        # Select Read Language action
        self.action_select_lang = QAction('Select Read Language', self)
        self.action_select_lang.triggered.connect(lambda: select_read_language(self.parent))
        self.menu_read.addAction(self.action_select_lang)

        # Web Content Menu
        self.addAction('Web Content', lambda: get_website_content(self.parent))


def setupMouseMenu(self):
    self.mouse_menu = QMenu(self)
    self.mouse_menu.addAction('Read', lambda: read_load(self))

    self.mouse_menu.addAction("Translate", lambda: open_and_run_ai_task(self, 'Translate'))
    self.mouse_menu.addAction("Summarize", lambda: open_and_run_ai_task(self, 'Summarize'))
    self.mouse_menu.addAction("Expand", lambda: open_and_run_ai_task(self, 'Expand'))
    self.mouse_menu.addAction("Rephrase", lambda: open_and_run_ai_task(self, 'Rephrase'))
    self.mouse_menu.addAction("Check Grammar/Spelling", lambda: open_and_run_ai_task(self, 'Check Grammar/Spelling'))
    self.mouse_menu.addAction("Arrange In Blots", lambda: open_and_run_ai_task(self, 'Arrange In Blots'))
    self.mouse_menu.addAction("Arrange In Steps", lambda: open_and_run_ai_task(self, 'Arrange In Steps'))
    self.mouse_menu.addAction("Suitable Title", lambda: open_and_run_ai_task(self, 'Suitable Title'))
