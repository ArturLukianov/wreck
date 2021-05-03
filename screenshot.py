import sys

from PyQt5.QtCore import Qt, QUrl, QTimer, QSize
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineSettings
import time


class Screenshot(QWebEngineView):

    def capture(self, url_file_pairs):
        self.url_file_pairs = url_file_pairs
        self.resize(QSize(1280, 1024))
        self.loadFinished.connect(self.on_loaded)
        self.setAttribute(Qt.WA_DontShowOnScreen)
        self.page().settings().setAttribute(
            QWebEngineSettings.ShowScrollBars, False)
        self.show()
        self.capture_one()

    def capture_one(self):
        url, self.output_file  = self.url_file_pairs.pop(0)
        self.load(QUrl(url))

    def on_loaded(self):
        QTimer.singleShot(3000, self.take_screenshot)

    def take_screenshot(self):
        self.grab().save(self.output_file, b'PNG')
        if len(self.url_file_pairs) == 0:
            self.app.quit()
        else:
            self.capture_one()

