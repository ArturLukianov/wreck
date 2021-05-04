#!/usr/bin/env python3
import sys
import os
import argparse

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt, QUrl, QTimer, QSize
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineSettings
import time
from wreckhelpers import alphize


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


def make_screenshots(urls, output_dir):
    os.mkdir(output_dir)
    
    url_file_pairs = []
    for url in urls:
        url_file_pairs.append((url, os.path.join(output_dir, alphize(url) + '.png')))

    app = QApplication([])
    s = Screenshot()
    s.app = app
    s.capture(url_file_pairs)
    app.exec_()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Make screenshots of web-pages')
    parser.add_argument('--urls', dest='urls', required=True, help='File with urls to screenshot')
    parser.add_argument('--output', dest='output', default='screenshots', help='Output directory')

    args = parser.parse_args()
    
    with open(args.urls) as urls_file:
        urls = [i.strip() for i in urls_file.readlines()]
        make_screenshots(urls, args.output)
