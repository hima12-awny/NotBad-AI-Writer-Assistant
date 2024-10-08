from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QMainWindow, QMessageBox

from functionality.file_handlling import load_words, Any
from functionality.word_tracker import WordTracker
from functionality.switching_handler import SwitchingHandler
from functionality.file_handlling import read_attr_from_settings, save_file

from gui_components.text_area import TextArea
from gui_components.menu_bar import MenuBar, setupMouseMenu
from gui_components.shortcuts import add_shortcuts_main_window
from gui_components.suggestions_words_container import SuggestionsWordsContainer


class NoteBad(QMainWindow):

    def __init__(self):
        super().__init__(None)

        # Data And File stuff #############
        self.new_file_tag = 1
        self.file_path = 'New file'
        self.contentFile = ''
        self.dict_of_all_sug_words = dict()
        self.dict_of_all_sug_words_dict = dict()
        self.wrong_words = dict()

        load_words(self)
        self.sug_word_list = []

        ##################################

        ## Next Word Assistant ###########

        self.loading_next_word_data_thread = None

        self.switch_handler = SwitchingHandler(self)

        self.word_tracker = WordTracker(self)
        self.ai_next_word_prid = None
        self.counter_next_word_prid = None

        self.acs_next_word_ai = None
        self.acs_next_word_counter = None

        self.thread = None
        self.worker = None
        self.progressbar = None

        self.ai_next_word_is_on = 0
        self.counter_is_on = 0
        self.ai_tools_is_loaded = 0
        self.counter_tools_is_loaded = 0

        self.n_prev_word = read_attr_from_settings("n_prev_words")

        self.action_word_completion = None
        self.word_completion_is_on = 1
        ##################################

        self.action_read_load = None
        self.is_read_load_on = 0

        ##################################

        ## GUI Stuff ######################

        self.ai_features_window: QMainWindow | Any = None

        self.loading_window = None

        self.setMinimumSize(800, 720)
        self.setGeometry(300, 100, 1000, 720)

        self.setWindowTitle(f'NoteBad - {self.file_path}')
        self.setWindowIcon(QIcon('mainWindowIcon.png'))

        self.cen_widget = QWidget(self)
        self.setCentralWidget(self.cen_widget)
        self.layout_ = QVBoxLayout()

        # Text Area
        self.txtArea = TextArea(self)

        self.txtArea.cursorPositionChanged(self.word_tracker.track_sug_words)
        self.txtArea.setContextMenuPolicy(Qt.CustomContextMenu)
        self.txtArea.customContextMenuRequested(self.menuMouse)

        #  Suggestions Words Container
        self.sug_words_options = SuggestionsWordsContainer(self)

        #  Menu Bar and Shortcuts
        MenuBar(self)
        add_shortcuts_main_window(self)

        self.mouse_menu = None
        setupMouseMenu(self)

        self.layout_.addWidget(self.txtArea)
        self.cen_widget.setLayout(self.layout_)

    def menuMouse(self, pos):
        self.mouse_menu.exec(self.mapToGlobal(pos))

    def closeEvent(self, event):

        final_text = self.txtArea.toPlainText()

        if (self.new_file_tag and final_text) or \
                (not self.new_file_tag and final_text != self.contentFile):

            response = QMessageBox.question(self, 'Note', 'you haven\'t saved this file, you want to save it?',
                                            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

            if response == QMessageBox.StandardButton.Yes:
                save_file(self)


app = QApplication()
root = NoteBad()
root.show()
app.exec()
