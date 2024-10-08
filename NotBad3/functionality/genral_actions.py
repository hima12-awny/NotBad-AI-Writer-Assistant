

def read_load(self):
    if not self.is_read_load_on:
        courser = self.txtArea.textCursor()
        text = courser.selectedText()

        if text:
            from functionality.threads_handler import make_thread_for_read_mode
            make_thread_for_read_mode(self, text)
        return

    from functionality.threads_handler import stop_reading
    stop_reading(self)


def select_read_language(self):
    from gui_components.read_lang_selector import LanguageSelectorDialog

    lang_selector = LanguageSelectorDialog(parent=self)
    lang_selector.show()


def close_windows(self):
    if self.ai_features_window is not None:
        self.ai_features_window.close()
    else:
        self.close()
