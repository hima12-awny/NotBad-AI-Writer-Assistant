from PySide6.QtWidgets import QDialog
from bs4 import BeautifulSoup
import requests
import re
from gui_components.get_website_url_dialog import GetUrlDialog


def get_soup(url):
    html = requests.get(url).text
    soup = BeautifulSoup(html, 'html.parser')
    return soup


def clean_and_get_all_text_from(text):
    text = text.strip()
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text


def get_website_content(self):

    dialog = GetUrlDialog()
    if dialog.exec() == QDialog.Accepted:
        url = dialog.get_url()

        soup = get_soup(url)
        text = soup.get_text()
        text = clean_and_get_all_text_from(text)
        self.txtArea.setText(text)

    else:
        print("rejected")

    dialog.close()

