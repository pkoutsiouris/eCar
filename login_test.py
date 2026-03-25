import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QMainWindow, QLabel, QLineEdit,
    QPushButton, QVBoxLayout, QHBoxLayout, QMessageBox,
    QFrame, QSizePolicy
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont


class MainMenuWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Car Rental - Main Menu")
        self.resize(900, 550)

        central = QWidget()
        self.setCentralWidget(central)

        layout = QVBoxLayout()
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(20)
        central.setLayout(layout)

        title = QLabel("Main Menu")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("""
            font-size: 28px;
            font-weight: bold;
            color: #1f2937;
        """)

        subtitle = QLabel("Προσωρινό μενού για να δεις ότι το login σε πάει σε άλλη οθόνη.")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet("""
            font-size: 14px;
            color: #6b7280;
        """)

        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 1px solid #e5e7eb;
                border-radius: 18px;
            }
        """)

        card_layout = QVBoxLayout()
        card_layout.setContentsMargins(30, 30, 30, 30)
        card_layout.setSpacing(15)
        card.setLayout(card_layout)

        btn_users = QPushButton("Users")
        btn_cars = QPushButton("Cars")
        btn_reservations = QPushButton("Reservations")
        btn_logout = QPushButton("Logout")

        buttons = [btn_users, btn_cars, btn_reservations, btn_logout]

        for btn in buttons:
            btn.setMinimumHeight(48)
            btn.setCursor(Qt.PointingHandCursor)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #2563eb;
                    color: white;
                    border: none;
                    border-radius: 12px;
                    font-size: 15px;
                    font-weight: 600;
                    padding: 10px;
                }
                QPushButton:hover {
                    background-color: #1d4ed8;
                }
                QPushButton:pressed {
                    background-color: #1e40af;
                }
            """)

        btn_users.clicked.connect(lambda: QMessageBox.information(self, "Users", "Εδώ αργότερα θα ανοίγει το Users window."))
        btn_cars.clicked.connect(lambda: QMessageBox.information(self, "Cars", "Εδώ αργότερα θα ανοίγει το Cars window."))
        btn_reservations.clicked.connect(lambda: QMessageBox.information(self, "Reservations", "Εδώ αργότερα θα ανοίγει το Reservations window."))
        btn_logout.clicked.connect(self.handle_logout)

        card_layout.addWidget(btn_users)
        card_layout.addWidget(btn_cars)
        card_layout.addWidget(btn_reservations)
        card_layout.addSpacing(10)
        card_layout.addWidget(btn_logout)

        layout.addStretch()
        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addWidget(card)
        layout.addStretch()

        self.setStyleSheet("""
            QMainWindow {
                background-color: #f3f4f6;
            }
        """)

    def handle_logout(self):
        self.login_window = LoginWindow()
        self.login_window.show()
        self.close()


class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Car Rental - Login")
        self.resize(520, 420)

        self.setStyleSheet("""
            QWidget {
                background-color: #f3f4f6;
                font-family: Segoe UI, Arial, sans-serif;
            }
            QLineEdit {
                background-color: white;
                border: 1px solid #d1d5db;
                border-radius: 10px;
                padding: 12px;
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 2px solid #2563eb;
            }
        """)

        outer_layout = QVBoxLayout()
        outer_layout.setContentsMargins(40, 40, 40, 40)
        outer_layout.setAlignment(Qt.AlignCenter)
        self.setLayout(outer_layout)

        card = QFrame()
        card.setMaximumWidth(380)
        card.setMinimumWidth(320)
        card.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        card.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 20px;
                border: 1px solid #e5e7eb;
            }
        """)

        card_layout = QVBoxLayout()
        card_layout.setContentsMargins(28, 28, 28, 28)
        card_layout.setSpacing(14)
        card.setLayout(card_layout)

        title = QLabel("Login")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("""
            font-size: 28px;
            font-weight: bold;
            color: #111827;
        """)

        subtitle = QLabel("Καλώς ήρθες στο Car Rental App")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet("""
            font-size: 13px;
            color: #6b7280;
            margin-bottom: 8px;
        """)

        email_label = QLabel("Email")
        email_label.setStyleSheet("font-size: 13px; color: #374151; font-weight: 600;")

        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("γράψε email")
        self.email_input.setMinimumHeight(44)

        password_label = QLabel("Password")
        password_label.setStyleSheet("font-size: 13px; color: #374151; font-weight: 600;")

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("γράψε password")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setMinimumHeight(44)

        self.login_button = QPushButton("Sign In")
        self.login_button.setMinimumHeight(48)
        self.login_button.setCursor(Qt.PointingHandCursor)
        self.login_button.setStyleSheet("""
            QPushButton {
                background-color: #2563eb;
                color: white;
                border: none;
                border-radius: 12px;
                font-size: 15px;
                font-weight: bold;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #1d4ed8;
            }
            QPushButton:pressed {
                background-color: #1e40af;
            }
        """)

        self.clear_button = QPushButton("Clear")
        self.clear_button.setMinimumHeight(44)
        self.clear_button.setCursor(Qt.PointingHandCursor)
        self.clear_button.setStyleSheet("""
            QPushButton {
                background-color: #e5e7eb;
                color: #111827;
                border: none;
                border-radius: 12px;
                font-size: 14px;
                font-weight: 600;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #d1d5db;
            }
        """)

        button_row = QHBoxLayout()
        button_row.setSpacing(10)
        button_row.addWidget(self.clear_button)
        button_row.addWidget(self.login_button)

        demo_info = QLabel("Demo login: βάλε κάτι και στα 2 πεδία για να περάσεις στο main menu.")
        demo_info.setWordWrap(True)
        demo_info.setAlignment(Qt.AlignCenter)
        demo_info.setStyleSheet("""
            color: #6b7280;
            font-size: 12px;
            margin-top: 6px;
        """)

        card_layout.addWidget(title)
        card_layout.addWidget(subtitle)
        card_layout.addSpacing(6)
        card_layout.addWidget(email_label)
        card_layout.addWidget(self.email_input)
        card_layout.addWidget(password_label)
        card_layout.addWidget(self.password_input)
        card_layout.addSpacing(8)
        card_layout.addLayout(button_row)
        card_layout.addWidget(demo_info)

        outer_layout.addWidget(card)

        self.login_button.clicked.connect(self.handle_login)
        self.clear_button.clicked.connect(self.clear_fields)

    def clear_fields(self):
        self.email_input.clear()
        self.password_input.clear()

    def handle_login(self):
        email = self.email_input.text().strip()
        password = self.password_input.text().strip()

        if not email or not password:
            QMessageBox.warning(self, "Λείπουν πεδία", "Συμπλήρωσε και email και password.")
            return

        self.main_menu = MainMenuWindow()
        self.main_menu.show()
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec())