import sys

from PySide6.QtCore import QUrl
from PySide6.QtGui import QAction, QKeySequence
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import (
    QApplication,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QStatusBar,
    QToolBar,
)


class SimpleBrowser(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Simple Web Browser")
        self.resize(1200, 800)

        self.home_url = QUrl("https://www.example.com")
        self.web_view = QWebEngineView()
        self.setCentralWidget(self.web_view)

        self._create_toolbar()
        self._create_statusbar()
        self._connect_signals()

        self.web_view.setUrl(self.home_url)

    def _create_toolbar(self) -> None:
        toolbar = QToolBar("Navigation", self)
        toolbar.setMovable(False)
        self.addToolBar(toolbar)

        back_action = QAction("Back", self)
        back_action.setShortcut(QKeySequence("Alt+Left"))
        back_action.triggered.connect(self.web_view.back)
        toolbar.addAction(back_action)

        forward_action = QAction("Forward", self)
        forward_action.setShortcut(QKeySequence("Alt+Right"))
        forward_action.triggered.connect(self.web_view.forward)
        toolbar.addAction(forward_action)

        reload_action = QAction("Reload", self)
        reload_action.setShortcut(QKeySequence("Ctrl+R"))
        reload_action.triggered.connect(self.web_view.reload)
        toolbar.addAction(reload_action)

        home_action = QAction("Home", self)
        home_action.setShortcut(QKeySequence("Alt+Home"))
        home_action.triggered.connect(self.navigate_home)
        toolbar.addAction(home_action)

        toolbar.addSeparator()

        self.url_bar = QLineEdit(self)
        self.url_bar.setPlaceholderText("Enter URL (example: openai.com)")
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        toolbar.addWidget(self.url_bar)

    def _create_statusbar(self) -> None:
        status = QStatusBar(self)
        self.setStatusBar(status)
        status.showMessage("Ready")

    def _connect_signals(self) -> None:
        self.web_view.urlChanged.connect(self._update_url_bar)
        self.web_view.titleChanged.connect(self._update_title)
        self.web_view.loadProgress.connect(self._show_progress)
        self.web_view.loadFinished.connect(self._handle_load_finished)

    def navigate_home(self) -> None:
        self.web_view.setUrl(self.home_url)

    def navigate_to_url(self) -> None:
        raw = self.url_bar.text().strip()
        if not raw:
            return

        if "://" not in raw:
            raw = f"https://{raw}"

        url = QUrl.fromUserInput(raw)
        if not url.isValid():
            QMessageBox.warning(self, "Invalid URL", "Please enter a valid URL.")
            return

        self.web_view.setUrl(url)

    def _update_url_bar(self, url: QUrl) -> None:
        self.url_bar.blockSignals(True)
        self.url_bar.setText(url.toString())
        self.url_bar.blockSignals(False)

    def _update_title(self, title: str) -> None:
        self.setWindowTitle(f"{title} - Simple Web Browser")

    def _show_progress(self, progress: int) -> None:
        self.statusBar().showMessage(f"Loading... {progress}%")

    def _handle_load_finished(self, success: bool) -> None:
        if success:
            self.statusBar().showMessage("Done")
        else:
            self.statusBar().showMessage("Failed to load page")


def main() -> int:
    app = QApplication(sys.argv)
    window = SimpleBrowser()
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
