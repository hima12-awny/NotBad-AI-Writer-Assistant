from functionality.threads_handler import make_thread_for_read_mode, stop_reading
from gui_components.read_lang_selector import LanguageSelectorDialog


def read_load(self):
    if not self.is_read_load_on:
        courser = self.txtArea.textCursor()
        text = courser.selectedText()

        if text:
            make_thread_for_read_mode(self, text)
        return

    stop_reading(self)


def select_read_language(self):
    lang_selector = LanguageSelectorDialog(parent=self)
    lang_selector.show()


def close_windows(self):
    if self.ai_features_window is not None:
        self.ai_features_window.close()
    else:
        self.close()
