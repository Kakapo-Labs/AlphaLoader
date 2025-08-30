import os
import sys
from PyQt5.QtWidgets import (QMainWindow, QFrame, QVBoxLayout, QProgressBar,
                             QLabel, QWidget, QHBoxLayout, QPushButton)
from PyQt5.QtCore import Qt, QTimer, QSize, QUrl
from PyQt5.QtGui import QFontDatabase, QFont, QIcon, QPainter, QPixmap
from PyQt5.QtSvg import QSvgRenderer
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage, QWebEngineSettings
from PyQt5.QtWebChannel import QWebChannel

from backend import Backend
from html_content import HTML_CONTENT


class WebEnginePage(QWebEnginePage):
    """
    Custom WebEnginePage to handle certificate errors, if any.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def certificateError(self, error):
        return True


class CustomTitleBar(QWidget):
    """
    A custom title bar for the main window to provide a modern look and feel.
    """

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(15, 0, 0, 0)
        self.layout.setSpacing(0)

        self.title_font = QFont("Segoe UI", 10, QFont.Bold)

        self.title = QLabel("AlphaLoader Alpha 0.51")
        self.title.setFont(self.title_font)
        self.title.setStyleSheet("color: #ccc;")

        self.layout.addWidget(self.title)
        self.layout.addStretch()

        minimize_icon = self.create_svg_icon(
            '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#FFFFFF" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="5" y1="12" x2="19" y2="12"></line></svg>')
        close_icon = self.create_svg_icon(
            '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#FFFFFF" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>')

        btn_style = """
            QPushButton {
                background-color: transparent;
                border: none;
                padding: 8px 15px;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.1);
            }
            QPushButton#close_btn:hover {
                background-color: #E81123;
            }
        """

        self.btn_minimize = QPushButton(minimize_icon, "")
        self.btn_minimize.setStyleSheet(btn_style)
        self.btn_minimize.setIconSize(QSize(16, 16))
        self.btn_minimize.clicked.connect(self.parent.showMinimized)

        self.btn_close = QPushButton(close_icon, "")
        self.btn_close.setObjectName("close_btn")
        self.btn_close.setStyleSheet(btn_style)
        self.btn_close.setIconSize(QSize(16, 16))
        self.btn_close.clicked.connect(self.parent.close)

        self.layout.addWidget(self.btn_minimize)
        self.layout.addWidget(self.btn_close)

        self.setLayout(self.layout)
        self.setFixedHeight(40)
        self.pressing = False

    def create_svg_icon(self, svg_content):
        renderer = QSvgRenderer(svg_content.encode('utf-8'))
        pixmap = QPixmap(renderer.defaultSize())
        pixmap.fill(Qt.transparent)
        painter = QPainter(pixmap)
        renderer.render(painter)
        painter.end()
        return QIcon(pixmap)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.pressing = True
            self.start_pos = event.globalPos()
            self.start_win_pos = self.parent.pos()

    def mouseMoveEvent(self, event):
        if self.pressing:
            delta = event.globalPos() - self.start_pos
            self.parent.move(self.start_win_pos + delta)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.pressing = False


class BrowserWindow(QMainWindow):
    """
    The main window of the application.
    """

    def __init__(self):
        super().__init__()
        self.backend = Backend()
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        # --- Simplified Startup Sequence ---
        self.init_ui_structure()
        self.init_main_content()

    def init_ui_structure(self):
        self.setWindowTitle("Rocket League Mod Installer")
        self.setGeometry(100, 100, 1400, 900)

        self.container = QFrame(self)
        self.container.setStyleSheet("background-color: #121212; border-radius: 15px;")
        self.main_layout = QVBoxLayout(self.container)
        self.main_layout.setContentsMargins(1, 1, 1, 1)
        self.main_layout.setSpacing(0)

        self.setCentralWidget(self.container)

        self.title_bar = CustomTitleBar(self)
        self.main_layout.addWidget(self.title_bar)

    def init_main_content(self):
        self.content_frame = QFrame()
        self.content_frame.setStyleSheet("background: transparent;")

        self.web_view = QWebEngineView()
        self.web_view.setContextMenuPolicy(Qt.NoContextMenu)
        self.web_view.setStyleSheet("border-bottom-left-radius: 15px; border-bottom-right-radius: 15px;")
        self.web_view.setAttribute(Qt.WA_TranslucentBackground, True)

        settings = self.web_view.settings()
        settings.setAttribute(QWebEngineSettings.WebGLEnabled, True)
        settings.setAttribute(QWebEngineSettings.Accelerated2dCanvasEnabled, True)

        self.web_page = WebEnginePage(self.web_view)
        self.web_page.setBackgroundColor(Qt.transparent)
        self.web_view.setPage(self.web_page)

        content_layout = QVBoxLayout(self.content_frame)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.addWidget(self.web_view)

        self.channel = QWebChannel()
        self.channel.registerObject("backend", self.backend)
        self.web_page.setWebChannel(self.channel)

        # --- MODIFICATION: Connect signals that are handled by the frontend directly in JS ---
        # The following signals are now connected within the HTML's JavaScript:
        # - update_progress
        # - install_complete
        # - uninstall_complete
        # - download_error

        # --- Signals that still need Python-side logic ---
        self.backend.installed_mods_checked.connect(
            lambda mods: self.web_page.runJavaScript(f"setInstalledMods({mods});"))
        self.backend.mod_list_fetched.connect(
            lambda mods_json: self.web_page.runJavaScript(f"initializeWithData(`{mods_json}`);")
        )

        self.main_layout.addWidget(self.content_frame)
        self.web_view.setHtml(HTML_CONTENT)

# --- MODIFICATION: Removed the entire resizeEvent, update_progress, on_install_complete, ---
# --- on_uninstall_complete, and on_download_error methods as they are no longer needed. ---
# --- END OF MODIFICATION ---