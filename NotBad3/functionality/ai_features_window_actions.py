def open_ai_window(
        self,
        init_function_name=None,
        selected_text=None,
        just_open_window=None
):
    from gui_components.ai_windos.ai_features_window import AIFeaturesWindow

    if not selected_text:
        selected_text = "Select Text From Main Text Area"

    if self.ai_features_window is None:
        self.ai_features_window = AIFeaturesWindow(
            parent=self,
            init_function_name=init_function_name,
            selected_text=selected_text,
            just_open_window=just_open_window
        )

        self.ai_features_window.show()


def open_and_run_ai_task(self, init_function_name):
    textCourser = self.txtArea.textCursor()
    if self.ai_features_window is None and textCourser:
        open_ai_window(
            self,
            init_function_name=init_function_name,
            selected_text=textCourser.selectedText()
        )
    else:
        self.ai_features_window.update_func_and_in_text(init_function_name, textCourser.selectedText())
