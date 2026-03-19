from __future__ import annotations

import sys

from app.db.session import database
from app.services.auth_service import AuthService


def bootstrap() -> None:
    database.init_schema()
    with database.connect() as db:
        row = db.execute('SELECT id FROM users LIMIT 1').fetchone()
        if row is None:
            AuthService().create_user(db, 'admin', 'admin123!', is_admin=True)


def main() -> int:
    bootstrap()
    try:
        from PySide6.QtWidgets import QApplication
        from app.gui.main_window import MainWindow
    except ModuleNotFoundError:
        print('PySide6 is not installed in this environment. Backend bootstrap completed successfully.')
        return 0
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    return app.exec()


if __name__ == '__main__':
    raise SystemExit(main())
