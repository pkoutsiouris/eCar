import sys
import mysql.connector
from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QFrame, QMessageBox
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap, QIcon, QAction
from back_end import authentication as auth
from main_user import MainDashboard



class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Car Rental Login")
        self.setWindowIcon(QIcon('assets/icon.png'))
        

        self.bg_label = QLabel(self)
        self.bg_label.lower() 
        self.original_pixmap = QPixmap('assets/bg.jpg') 

        # MAIN LAYOUT
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        self.setLayout(main_layout)

        
        container = QWidget()
        container.setStyleSheet("background: transparent;") 
        main_layout.addWidget(container)

        outer_layout = QVBoxLayout()
        outer_layout.setAlignment(Qt.AlignCenter)
        outer_layout.setSpacing(18)
        container.setLayout(outer_layout)

        # LOGO TEXT
        logo_label = QLabel("eCar Rental")
        logo_label.setAlignment(Qt.AlignCenter)
        logo_label.setStyleSheet("""
            color: white;
            font-size: 34px;
            font-weight: bold;
            letter-spacing: 2px;
            background: transparent;
        """)

        # LOGIN CARD
        card = QFrame()
        card.setObjectName("MainCard")
        card.setFixedWidth(390)
        card.setStyleSheet("""
            #MainCard {
                background-color: rgba(255, 255, 255, 200);
                border-radius: 24px;
            }
        """)

        card_layout = QVBoxLayout()
        card_layout.setContentsMargins(35, 30, 35, 30)
        card_layout.setSpacing(16)
        card.setLayout(card_layout)

        title = QLabel("MEMBER LOGIN")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("""
            color: #334155;
            font-size: 18px;
            font-weight: 600;
            letter-spacing: 1px;
            background: transparent;
        """)

        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Enter email")
        self.email_input.setMinimumHeight(46)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter password")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setMinimumHeight(46)

        self.toggle_pw_action = QAction(self)
        self.toggle_pw_action.setIcon(QIcon('assets/eye_hide.png')) 
        self.password_input.addAction(self.toggle_pw_action, QLineEdit.TrailingPosition)
        self.toggle_pw_action.triggered.connect(lambda: self.toggle_password_visibility(self.password_input, self.toggle_pw_action))

        self.email_input.setStyleSheet("""
            QLineEdit {
                background-color: rgba(120, 120, 120, 80);
                color: #1f2937;
                border: none;
                border-bottom: 2px solid #64748b;
                padding: 12px;
                font-size: 15px;
            }
            QLineEdit::placeholder {
                color: #475569;
            }
            QLineEdit:focus {
                background-color: rgba(120, 120, 120, 110);
                border-bottom: 2px solid #22c55e;
            }
        """)

        self.password_input.setStyleSheet("""
            QLineEdit {
                background-color: rgba(120, 120, 120, 80);
                color: #1f2937;
                border: none;
                border-bottom: 2px solid #64748b;
                padding: 12px;
                font-size: 15px;
            }
            QLineEdit::placeholder {
                color: #475569;
            }
            QLineEdit:focus {
                background-color: rgba(120, 120, 120, 110);
                border-bottom: 2px solid #22c55e;
            }
        """)

        login_button = QPushButton("LOGIN")
        login_button.setMinimumHeight(48)
        login_button.setCursor(Qt.PointingHandCursor)
        login_button.setStyleSheet("""
            QPushButton {
                background-color: #22c55e;
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #16a34a;
            }
        """)

        register_button = QPushButton("REGISTER")
        register_button.setFixedWidth(290)
        register_button.setMinimumHeight(48)
        register_button.setCursor(Qt.PointingHandCursor)
        register_button.setStyleSheet("""
            QPushButton {
                background-color: rgba(255, 255, 255, 90);
                color: white;
                border: 2px solid white;
                border-radius: 14px;
                font-size: 16px;
                font-weight: 500;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 130);
            }
        """)

        card_layout.addWidget(title)
        card_layout.addSpacing(8)
        card_layout.addWidget(self.email_input)
        card_layout.addWidget(self.password_input)
        card_layout.addSpacing(8)
        card_layout.addWidget(login_button)

        outer_layout.addWidget(logo_label)
        outer_layout.addWidget(card, alignment=Qt.AlignCenter)
        outer_layout.addWidget(register_button, alignment=Qt.AlignCenter)

   
        outer_layout.addWidget(register_button, alignment=Qt.AlignCenter)
        login_button.clicked.connect(self.handle_login)
        register_button.clicked.connect(self.handle_register)

        self.showMaximized()

    def resizeEvent(self, event):
        
        if not self.original_pixmap.isNull():
            scaled_pixmap = self.original_pixmap.scaled(
                self.size(), 
                Qt.KeepAspectRatioByExpanding, 
                Qt.SmoothTransformation        
            )
            self.bg_label.setPixmap(scaled_pixmap)
            self.bg_label.resize(self.size()) 
        super().resizeEvent(event)

    def handle_login(self):
        email = self.email_input.text().strip()
        password = self.password_input.text().strip()
        response,message,role = auth.authenticate_user(email, password)
        print(response)
        if response:
            self.user_window = MainDashboard()
            self.user_window.show()
            self.close()
        else:
            QMessageBox.warning(self, "Login Failed!", message)
            
    def handle_register(self):
        from register import RegisterWindow
        self.user_window = RegisterWindow()
        self.user_window.show()
        self.close()
    
    def toggle_password_visibility(self, line_edit, action):
        if line_edit.echoMode() == QLineEdit.Password:
            line_edit.setEchoMode(QLineEdit.Normal)
            action.setIcon(QIcon('assets/eye_show.png'))
        else:
            line_edit.setEchoMode(QLineEdit.Password)
            action.setIcon(QIcon('assets/eye_hide.png'))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec())