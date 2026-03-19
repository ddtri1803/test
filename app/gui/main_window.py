from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import QMimeData, QPoint, Qt, Signal
from PySide6.QtGui import QAction, QDragEnterEvent, QDropEvent, QIcon, QStandardItem, QStandardItemModel
from PySide6.QtWidgets import (
    QApplication,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListView,
    QMainWindow,
    QMenu,
    QMessageBox,
    QPushButton,
    QSplitter,
    QStatusBar,
    QToolBar,
    QTreeView,
    QVBoxLayout,
    QWidget,
)


class DropListView(QListView):
    files_dropped = Signal(list)

    def __init__(self) -> None:
        super().__init__()
        self.setAcceptDrops(True)
        self.setViewMode(QListView.IconMode)
        self.setSpacing(12)

    def dragEnterEvent(self, event: QDragEnterEvent) -> None:
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event: QDropEvent) -> None:
        paths = [url.toLocalFile() for url in event.mimeData().urls()]
        self.files_dropped.emit(paths)
        event.acceptProposedAction()


class LoginPane(QFrame):
    login_requested = Signal(str, str)

    def __init__(self) -> None:
        super().__init__()
        layout = QVBoxLayout(self)
        title = QLabel("Secure FTP Manager")
        title.setObjectName("heroTitle")
        self.username = QLineEdit()
        self.username.setPlaceholderText("Username")
        self.password = QLineEdit()
        self.password.setEchoMode(QLineEdit.Password)
        self.password.setPlaceholderText("Password")
        button = QPushButton("Sign in")
        button.clicked.connect(self._emit_login)
        layout.addWidget(title)
        layout.addWidget(QLabel("App login"))
        layout.addWidget(self.username)
        layout.addWidget(self.password)
        layout.addWidget(button)
        layout.addStretch()

    def _emit_login(self) -> None:
        self.login_requested.emit(self.username.text().strip(), self.password.text())


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Secure FTP Manager")
        self.resize(1400, 900)
        self._build_ui()
        self._apply_styles()

    def _build_ui(self) -> None:
        container = QWidget()
        root = QVBoxLayout(container)
        self.login_pane = LoginPane()
        root.addWidget(self.login_pane)

        self.chrome = QToolBar("Navigation")
        self.chrome.setMovable(False)
        self.addToolBar(self.chrome)
        self.breadcrumb = QLineEdit("/public_html")
        self.breadcrumb.setReadOnly(True)
        self.chrome.addWidget(self.breadcrumb)
        self.chrome.addAction(QAction("Grid", self))
        self.chrome.addAction(QAction("List", self))

        splitter = QSplitter()
        self.sidebar = QTreeView()
        self.sidebar.setHeaderHidden(True)
        self.sidebar_model = QStandardItemModel()
        self.sidebar_model.appendRow(QStandardItem("Connections"))
        self.sidebar.setModel(self.sidebar_model)
        splitter.addWidget(self.sidebar)

        panel = QWidget()
        panel_layout = QVBoxLayout(panel)
        self.live_indicator = QLabel("● Offline")
        self.live_indicator.setObjectName("statusOffline")
        panel_layout.addWidget(self.live_indicator)
        self.file_list = DropListView()
        self.file_model = QStandardItemModel()
        self.file_list.setModel(self.file_model)
        self.file_list.setContextMenuPolicy(Qt.CustomContextMenu)
        self.file_list.customContextMenuRequested.connect(self._show_context_menu)
        panel_layout.addWidget(self.file_list)
        splitter.addWidget(panel)
        splitter.setStretchFactor(1, 1)
        root.addWidget(splitter)

        self.setCentralWidget(container)
        self.status = QStatusBar()
        self.setStatusBar(self.status)
        self.status.showMessage("Ready")
        self._populate_placeholder_entries()

    def _populate_placeholder_entries(self) -> None:
        for name, icon in [("index.php", "text-x-python"), ("assets", "folder"), ("uploads", "folder")]:
            item = QStandardItem(QIcon.fromTheme(icon), name)
            self.file_model.appendRow(item)

    def _show_context_menu(self, point: QPoint) -> None:
        menu = QMenu(self)
        menu.addAction("Rename")
        menu.addAction("Delete")
        menu.addAction("Download")
        menu.exec(self.file_list.mapToGlobal(point))

    def set_live(self, is_live: bool) -> None:
        self.live_indicator.setText("● Live" if is_live else "● Offline")
        self.live_indicator.setObjectName("statusLive" if is_live else "statusOffline")
        self.live_indicator.style().unpolish(self.live_indicator)
        self.live_indicator.style().polish(self.live_indicator)

    def toast(self, message: str) -> None:
        self.status.showMessage(message, 5000)
        QMessageBox.information(self, "Secure FTP Manager", message)

    def _apply_styles(self) -> None:
        self.setStyleSheet(
            """
            QMainWindow { background: #111827; color: #f9fafb; }
            QToolBar { background: #0f172a; border: 0; padding: 8px; }
            QLineEdit, QListView, QTreeView { background: #1f2937; color: #f9fafb; border: 1px solid #374151; border-radius: 8px; padding: 8px; }
            QFrame { background: #111827; }
            QPushButton { background: #2563eb; color: white; border: 0; border-radius: 8px; padding: 10px 14px; }
            QLabel#heroTitle { font-size: 28px; font-weight: 700; }
            QLabel#statusLive { color: #22c55e; font-weight: 700; }
            QLabel#statusOffline { color: #f59e0b; font-weight: 700; }
            """
        )
