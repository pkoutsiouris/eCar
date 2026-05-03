import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QScrollArea, QFrame, QTableWidget, 
    QTableWidgetItem, QHeaderView, QStackedWidget, QButtonGroup, QMessageBox
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap, QIcon
from PySide6.QtWidgets import QComboBox

from back_end import functions

class AdminWindow(QMainWindow):
    def __init__(self, session_email: str):
        super().__init__()
        self.session_email = session_email
        self.setWindowTitle("eCar Rental - Admin Panel")
        self.setWindowIcon(QIcon('assets/icon.png'))
        self.resize(1280, 820)

        # Main Central Widget με gradient background όπως το MainDashboard
        outer = QWidget()
        self.setCentralWidget(outer)
        outer_layout = QVBoxLayout(outer)
        outer_layout.setContentsMargins(18, 18, 18, 18)
        outer_layout.setSpacing(0)
        outer.setStyleSheet("""
            QWidget {
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:1,
                    stop:0 #1e293b,
                    stop:1 #334155
                );
            }
        """)

        app_shell = QFrame()
        app_shell.setObjectName("AppShell")
        app_shell.setStyleSheet("QFrame#AppShell { background-color: #f0f4f3; border-radius: 20px; }")
        shell_layout = QHBoxLayout(app_shell)
        shell_layout.setContentsMargins(0, 0, 0, 0)
        shell_layout.setSpacing(0)
        outer_layout.addWidget(app_shell)

        # =========================
        # SIDEBAR (Layout από main_user.py)
        # =========================
        sidebar = QFrame()
        sidebar.setFixedWidth(220)
        sidebar.setStyleSheet("""
            QFrame { background-color: #0f172a; border-top-left-radius: 20px; border-bottom-left-radius: 20px; }
            QPushButton {
                text-align: left; padding: 14px 22px; border: none;
                font-size: 14px; font-weight: 600; color: #94a3b8;
                background: transparent; border-left: 4px solid transparent;
            }
            QPushButton:hover { background-color: #1e293b; color: white; }
            QPushButton:checked { background-color: #1e293b; color: white; border-left: 4px solid #38bdf8; }
        """)
        
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(0, 22, 0, 18)
        
        logo = QLabel("Admin Panel")
        logo.setStyleSheet("color: white; font-size: 22px; font-weight: 800; padding: 0 20px 20px 20px;")
        sidebar_layout.addWidget(logo)

        self.nav_group = QButtonGroup(self)
        self.nav_group.setExclusive(True)

        # Buttons
        self.btn_dash = self.make_nav_btn("Dashboard", True)
        self.btn_users = self.make_nav_btn("Manage Users")
        self.btn_logs = self.make_nav_btn("System Logs")
        
        self.btn_dash.clicked.connect(lambda: self.pages.setCurrentIndex(0))
        self.btn_users.clicked.connect(lambda: self.pages.setCurrentIndex(1))
        self.btn_logs.clicked.connect(lambda: self.pages.setCurrentIndex(2))

        sidebar_layout.addWidget(self.btn_dash)
        sidebar_layout.addWidget(self.btn_users)
        sidebar_layout.addWidget(self.btn_logs)
        sidebar_layout.addStretch()

        btn_logout = QPushButton("Logout")
        btn_logout.setStyleSheet("color: #f87171; font-weight: bold;")
        btn_logout.clicked.connect(self.logout)
        sidebar_layout.addWidget(btn_logout)

        shell_layout.addWidget(sidebar)

        # =========================
        # MAIN CONTENT (Stacked Widget)
        # =========================
        self.pages = QStackedWidget()
        shell_layout.addWidget(self.pages)

        # PAGE 0: DASHBOARD (Σύνδεση με MainDashboard)
        self.pages.addWidget(self.create_welcome_page())

        # PAGE 1: MANAGE USERS
        self.pages.addWidget(self.create_users_page())

        # PAGE 2: LOGS
        self.pages.addWidget(self.create_logs_page())

    def make_nav_btn(self, text, checked=False):
        btn = QPushButton(text)
        btn.setCheckable(True)
        btn.setChecked(checked)
        btn.setCursor(Qt.PointingHandCursor)
        self.nav_group.addButton(btn)
        return btn

    def create_banner(self, title_text, subtitle_text):
        banner = QFrame()
        banner.setFixedHeight(160)
        banner.setStyleSheet("background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #1e293b, stop:1 #334155); border-top-right-radius: 20px;")
        layout = QVBoxLayout(banner)
        layout.setContentsMargins(32, 0, 32, 0)
        
        t = QLabel(title_text)
        t.setStyleSheet("color: white; font-size: 30px; font-weight: 800;")
        st = QLabel(subtitle_text)
        st.setStyleSheet("color: #94a3b8; font-size: 14px;")
        
        layout.addStretch()
        layout.addWidget(t)
        layout.addWidget(st)
        layout.addSpacing(20)
        return banner

    def create_welcome_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(0,0,0,0)
        layout.addWidget(self.create_banner("Admin Dashboard", f"Welcome back, {self.session_email}"))
        
        content = QVBoxLayout()
        content.setContentsMargins(30,30,30,30)
        
        info_card = QFrame()
        info_card.setStyleSheet("background: white; border-radius: 15px; border: 1px solid #e2e8f0;")
        card_layout = QVBoxLayout(info_card)
        
        msg = QLabel("Select a category from the sidebar to manage the system.")
        msg.setStyleSheet("color: #475569; font-size: 16px;")
        msg.setAlignment(Qt.AlignCenter)
        
        btn_back = QPushButton("Go to User Dashboard")
        btn_back.setFixedWidth(200)
        btn_back.setStyleSheet("background: #38bdf8; color: white; padding: 10px; border-radius: 8px; font-weight: bold;")
        btn_back.clicked.connect(self.forward_to_dashboard)
        
        card_layout.addSpacing(40)
        card_layout.addWidget(msg)
        card_layout.addSpacing(20)
        card_layout.addWidget(btn_back, alignment=Qt.AlignCenter)
        card_layout.addSpacing(40)
        
        content.addWidget(info_card)
        content.addStretch()
        layout.addLayout(content)
        return page
    
    def create_users_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(0,0,0,0)
        layout.addWidget(self.create_banner("Manage Users", "View and moderate registered accounts."))

        self.user_table = QTableWidget(0, 5)
        self.user_table.setHorizontalHeaderLabels(["ID", "Full Name", "Email", "Role Selection", "Actions"])
        self.user_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.user_table.setStyleSheet("QTableWidget { background: white; border: none; color: black; }")
        
        users_data = functions.GetUsers() 
        
        if users_data:
            for row_idx, user in enumerate(users_data):
                self.user_table.insertRow(row_idx)
                self.user_table.setItem(row_idx, 0, QTableWidgetItem(str(user['user_id'])))
                self.user_table.setItem(row_idx, 1, QTableWidgetItem(f"{user['first_name']} {user['surname']}"))
                self.user_table.setItem(row_idx, 2, QTableWidgetItem(user['email']))
                
                # --- ΔΗΜΙΟΥΡΓΙΑ COMBOBOX (SCROLLER) ΓΙΑ ΤΟ ΡΟΛΟ ---
                role_combo = QComboBox()
                roles = ["Customer", "Dealer", "Admin"]
                role_combo.addItems(roles)
                # Θέτουμε την τρέχουσα τιμή βάσει της βάσης δεδομένων
                role_combo.setCurrentText(user['user_role'])
                role_combo.setStyleSheet("color: white; padding: 5px;")
                self.user_table.setCellWidget(row_idx, 3, role_combo)
                
                # --- ACTIONS LAYOUT ---
                actions_widget = QWidget()
                actions_layout = QHBoxLayout(actions_widget)
                actions_layout.setContentsMargins(2, 2, 2, 2)

                # ΚΟΥΜΠΙ APPLY
                btn_apply = QPushButton("Apply")
                btn_apply.setStyleSheet("background: #3b82f6; color: white; border-radius: 5px; padding: 5px;")
                # Σύνδεση με τη νέα μέθοδο apply_role_change
                btn_apply.clicked.connect(lambda ch, e=user['email'], c=role_combo: self.apply_role_change(e, c))

                # Κουμπί Delete
                btn_del = QPushButton("Delete")
                btn_del.setStyleSheet("background: #ef4444; color: white; border-radius: 5px; padding: 5px;")
                btn_del.clicked.connect(lambda ch, r=row_idx: self.delete_user(r))

                actions_layout.addWidget(btn_apply)
                actions_layout.addWidget(btn_del)
                self.user_table.setCellWidget(row_idx, 4, actions_widget)

        layout.addWidget(self.user_table)
        return page
    def apply_role_change(self, email, combo_box):
        new_role = combo_box.currentText()
        success = functions.UpdateUserRole(email, new_role) # Καλεί τη νέα συνάρτηση
        
        if success:
            print(f"Successfully updated {email} to {new_role}")
        else:
            print(f"Failed to update role for {email}")
    def create_logs_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(0,0,0,0)
        layout.addWidget(self.create_banner("System Logs", "Real-time activity monitoring."))

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        log_text = QLabel(
            " [INFO] 2024-05-20 10:22:01 - User admin logged in\n"
            " [WARN] 2024-05-20 10:25:44 - Failed login attempt from 192.168.1.1\n"
            " [INFO] 2024-05-20 10:30:12 - New car 'Tesla Model 3' added to database"
        )
        log_text.setStyleSheet("font-family: 'Courier New'; color: #10b981; background: #0f172a; padding: 20px;")
        log_text.setAlignment(Qt.AlignTop)
        
        scroll.setWidget(log_text)
        layout.addWidget(scroll)
        return page

    def delete_user(self, row):
        # 1. Παίρνουμε το email από τη στήλη 2 της συγκεκριμένης σειράς
        email_item = self.user_table.item(row, 2)
        if not email_item:
            return
            
        email = email_item.text()
        
        confirm = QMessageBox.question(
            self,
            "Confirm Deletion",
            f"Are you sure you want to delete user {email}?\nThis action cannot be undone.",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if confirm == QMessageBox.Yes:
            success = functions.DeleteUserByEmail(email)
            
            if success:
                self.user_table.removeRow(row)
                print(f"Successfully removed {email} from UI.")
                QMessageBox.information(self, "Deleted", f"User {email} has been deleted.")
            else:
                QMessageBox.critical(self, "Error", f"Failed to delete user {email} from database.")

    def logout(self):
        from login import LoginWindow
        self.login_win = LoginWindow()
        self.login_win.show()
        self.close()

    def forward_to_dashboard(self):
        from main_user import MainDashboard
        self.main_dash = MainDashboard(self.session_email)
        self.main_dash.show()
        self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AdminWindow("admin@ecarrental.com")
    window.show()
    sys.exit(app.exec())