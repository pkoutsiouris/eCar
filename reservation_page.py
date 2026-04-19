import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QScrollArea, QGridLayout, QFrame, QButtonGroup, QDialog , QFormLayout, QLineEdit, QDateTimeEdit, QDialogButtonBox
)
from PySide6.QtCore import Qt, QDateTime 
from back_end import functions
from PySide6.QtGui import QPixmap, QIcon

class DatePickerDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Select Reservation Dates")
        self.setFixedWidth(350)
        
        layout = QVBoxLayout(self)
        form = QFormLayout()

        # Ορισμός τρέχουσας ημερομηνίας ως default
        now = QDateTime.currentDateTime()

        self.start_date_edit = QDateTimeEdit(now)
        self.start_date_edit.setCalendarPopup(True)
        self.start_date_edit.setDisplayFormat("yyyy-MM-dd HH:mm")

        self.end_date_edit = QDateTimeEdit(now.addDays(1))
        self.end_date_edit.setCalendarPopup(True)
        self.end_date_edit.setDisplayFormat("yyyy-MM-dd HH:mm")

        form.addRow("Start Date:", self.start_date_edit)
        form.addRow("End Date:", self.end_date_edit)
        
        layout.addLayout(form)

        # Buttons (OK / Cancel)
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def get_dates(self):
        # Επιστρέφει τις ημερομηνίες στο string format που ζήτησες
        start_str = self.start_date_edit.dateTime().toString("yyyy-MM-dd HH:mm")
        end_str = self.end_date_edit.dateTime().toString("yyyy-MM-dd HH:mm")
        return start_str, end_str
class ReservationsWindow(QMainWindow):
    def __init__(self,session_email:str):
        super().__init__()
        self.setWindowTitle("Car Rental - Reservations")
        self.setWindowIcon(QIcon('assets/icon.png'))
        self.resize(1280, 820)
        self.session_email=session_email
        # Τραβάμε τα αυτοκίνητα
        db_cars = functions.GetCars()

        if db_cars:
            self.cars = db_cars
        else:
            self.cars = []

        outer = QWidget()
        self.setCentralWidget(outer)
        outer_layout = QVBoxLayout(outer)
        outer_layout.setContentsMargins(18, 18, 18, 18)
        outer_layout.setSpacing(0)

        outer.setStyleSheet("""
            QWidget {
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:1,
                    stop:0 #3a5a54,
                    stop:0.5 #2d3e3a,
                    stop:1 #4a6d64
                );
            }
        """)

        app_shell = QFrame()
        app_shell.setObjectName("AppShell")
        app_shell.setStyleSheet("""
            QFrame#AppShell {
                background-color: #f0f4f3;
                border-radius: 20px;
            }
        """)

        shell_layout = QHBoxLayout(app_shell)
        shell_layout.setContentsMargins(0, 0, 0, 0)
        shell_layout.setSpacing(0)

        outer_layout.addWidget(app_shell)

        # =========================
        # Sidebar
        # =========================
        sidebar = QFrame()
        sidebar.setFixedWidth(220)
        sidebar.setStyleSheet("""
            QFrame {
                background-color: #1a2b27;
                border-top-left-radius: 20px;
                border-bottom-left-radius: 20px;
            }
            QLabel {
                background: transparent;
            }
            QPushButton {
                text-align: left;
                padding: 14px 22px;
                border: none;
                font-size: 14px;
                font-weight: 600;
                color: #a3c9b8;
                background: transparent;
                border-left: 4px solid transparent;
            }
            QPushButton:hover {
                background-color: #243a34;
                color: white;
            }
            QPushButton:checked {
                background-color: #2d3e3a;
                color: white;
                border-left: 4px solid #6a9a83;
            }   
        """)
        
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(0, 22, 0, 18)
        sidebar_layout.setSpacing(6)
        

        logo_wrap = QWidget()
        logo_layout = QVBoxLayout(logo_wrap)
        logo_layout.setContentsMargins(18, 0, 18, 10)
        logo_layout.setSpacing(2)

        logo = QLabel("eCar Rental")
        logo.setStyleSheet("""
            color: white;
            font-size: 24px;
            font-weight: 800;
        """)

       

        logo_layout.addWidget(logo)
        sidebar_layout.addWidget(logo_wrap)

        self.nav_group = QButtonGroup(self)
        self.nav_group.setExclusive(True)

        btn_dashboard = self.make_sidebar_button("Dashboard")
        btn_dashboard.clicked.connect(self.forward_to_dashboard)
        btn_reservations = self.make_sidebar_button("Reservations", checked=True)
        btn_settings = self.make_sidebar_button("Settings")
        btn_logout = self.make_sidebar_button("Logout")

        self.nav_group.addButton(btn_dashboard)
        self.nav_group.addButton(btn_reservations)
        self.nav_group.addButton(btn_settings)

        sidebar_layout.addWidget(btn_dashboard)
        sidebar_layout.addWidget(btn_reservations)
        sidebar_layout.addWidget(btn_settings)
        sidebar_layout.addStretch()

        self.btn_logout = QPushButton("Logout")
        self.btn_logout.setCursor(Qt.PointingHandCursor)
        self.btn_logout.setMinimumHeight(46)
        self.btn_logout.clicked.connect(self.logout)
        self.btn_logout.setStyleSheet("""
            QPushButton {
                text-align: left;
                padding: 14px 22px;
                border: none;
                font-size: 14px;
                font-weight: 600;
                color: #ff9999;
                background: transparent;
            }
            QPushButton:hover {
                background-color: #3d2424;
                color: #ff4444;
            }
        """)
        sidebar_layout.addWidget(self.btn_logout)

        shell_layout.addWidget(sidebar)

        # =========================
        # Main content
        # =========================
        content = QWidget()
        content.setStyleSheet("background-color: transparent;")
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)

        shell_layout.addWidget(content)

        btn_logout.setStyleSheet("""
            QPushButton {
                text-align: left;
                padding: 14px 22px;
                border: none;
                font-size: 14px;
                font-weight: 600;
                color: #ff9999;
                background: transparent;
            }
            QPushButton:hover {
                background-color: #3d2424;
                color: #ff4444;
            }
        """)

        # Banner
        banner = QFrame()
        banner.setFixedHeight(190)
        banner.setStyleSheet("""
         QFrame {
            border-top-right-radius: 20px;
            background: qlineargradient(
                x1:0, y1:0, x2:1, y2:0,
                stop:0 #6a9a83,
                stop:1 #3a5a54
                );
            }
        """)

        banner_layout = QVBoxLayout(banner)
        banner_layout.setContentsMargins(32, 24, 32, 24)
        banner_layout.setSpacing(10)

        banner_top = QHBoxLayout()
        banner_top.setSpacing(10)

        title = QLabel("Reservations")
        title.setStyleSheet("""
            color: white;
            font-size: 34px;
            font-weight: 800;W
            background: transparent;
        """)

        subtitle = QLabel("View and manage reservations and details.")
        subtitle.setStyleSheet("""
            color: rgba(255,255,255,0.88);
            font-size: 14px;
            font-weight: 500;
            background: transparent;
        """)

        banner_layout.addLayout(banner_top)
        banner_layout.addStretch()
        banner_layout.addWidget(title)
        banner_layout.addWidget(subtitle)
        banner_layout.addSpacing(8)

        content_layout.addWidget(banner)
        
        #Logout Button
        btn_logout = QPushButton(" Logout")
        btn_logout.setCursor(Qt.PointingHandCursor)
        btn_logout.setMinimumHeight(46)
        btn_logout.clicked.connect(self.logout)

        #MainDashboard Button
        btn_dashboard = QPushButton(" Dashboard")
        btn_dashboard.setCursor(Qt.PointingHandCursor)
        btn_dashboard.setMinimumHeight(46)
        btn_dashboard.clicked.connect(self.forward_to_dashboard)


        # Toolbar
        toolbar = QWidget()
        toolbar.setFixedHeight(72)
        toolbar.setStyleSheet("background-color: white; border-bottom: 1px solid #e0e8e5;")

        toolbar_layout = QHBoxLayout(toolbar)
        toolbar_layout.setContentsMargins(28, 0, 28, 0)
        toolbar_layout.setSpacing(12)

        self.right_info_label = QLabel(f"Showing <b>{len(self.cars)}</b> vehicles")
        self.right_info_label.setStyleSheet("""
            color: #556070;
            font-size: 14px;
            background: transparent;
        """)


        toolbar_layout.addStretch()
        toolbar_layout.addWidget(self.right_info_label)
        content_layout.addWidget(toolbar)

        # Scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: #f5f7fb;
            }
            QScrollBar:vertical {
                background: #edf2f9;
                width: 12px;
                margin: 6px 2px 6px 2px;
                border-radius: 6px;
            }
            QScrollBar::handle:vertical {
                background: #c7d3e4;
                border-radius: 6px;
                min-height: 30px;
            }
            QScrollBar::handle:vertical:hover {
                background: #aebcd0;
            }
        """)

        scroll_content = QWidget()
        scroll_content.setStyleSheet("background-color: #f5f7fb;")

        # ... (υπάρχων κώδικας toolbar) ...
        toolbar_layout.setContentsMargins(28, 0, 28, 0)
        toolbar_layout.setSpacing(12)

        # ΝΕΟ ΚΟΥΜΠΙ ΕΠΙΛΟΓΗΣ ΗΜΕΡΟΜΗΝΙΑΣ
        self.btn_pick_dates = QPushButton("📅 Set Dates")
        self.btn_pick_dates.setCursor(Qt.PointingHandCursor)
        self.btn_pick_dates.clicked.connect(self.open_date_picker)
        self.btn_pick_dates.setStyleSheet("""
            QPushButton {
                background-color: #3a5a54;
                color: white;
                border-radius: 8px;
                padding: 8px 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #4a6d64;
            }
        """)
        toolbar_layout.addWidget(self.btn_pick_dates) # Προσθήκη στο toolbardef open_date_picker(self):
        dialog = DatePickerDialog(self)
        if dialog.exec() == QDialog.Accepted:
            start_date, end_date = dialog.get_dates()
            
            # Εδώ έχεις τις ημερομηνίες έτοιμες για το st = datetime.strptime(...)
            print(f"Selected Start: {start_date}")
            print(f"Selected End: {end_date}")
            
            # Μπορείς να ενημερώσεις το UI ή να φιλτράρεις τα αυτοκίνητα
            self.btn_pick_dates.setText(f"📅 {start_date} to {end_date}")
        
        toolbar_layout.addStretch()
        # ...

        self.grid = QGridLayout(scroll_content)
        self.grid.setContentsMargins(28, 24, 28, 28)
        self.grid.setHorizontalSpacing(22)
        self.grid.setVerticalSpacing(22)
        self.update_grid(self.cars)

        scroll.setWidget(scroll_content)
        content_layout.addWidget(scroll)
       


        scroll.setWidget(scroll_content)
        content_layout.addWidget(scroll)
    def open_date_picker(self):
        """Αυτή η μέθοδος έλειπε ή ήταν σε λάθος θέση!"""
        dialog = DatePickerDialog(self)
        if dialog.exec() == QDialog.Accepted:
            start_date, end_date = dialog.get_dates()
            # Εδώ οι ημερομηνίες είναι ακριβώς στο format που θες
            print(f"Start: {start_date}, End: {end_date}")
            self.btn_pick_dates.setText(f"📅 {start_date}")
    def update_grid(self, cars_list):
        for i in reversed(range(self.grid.count())):
            widget = self.grid.itemAt(i).widget()
            if widget:
                widget.deleteLater()
                
        if not cars_list:           
                no_cars_label = QLabel("No reservations can be found.")
                no_cars_label.setAlignment(Qt.AlignCenter)
                no_cars_label.setStyleSheet("""
                    color: #8a94a6; 
                    font-size: 20px; 
                    font-weight: bold; 
                    margin-top: 60px;
                """)
                
                self.grid.addWidget(no_cars_label, 0, 0, 1, 3) 
                
                self.right_info_label.setText("Showing <b>0</b> vehicles")
                
                return 
                
                self.right_info_label.setText(f"Showing <b>{len(cars_list)}</b> vehicles")


        row = 0
        col = 0
        for car in cars_list:
            card = self.create_car_card(car)
            self.grid.addWidget(card, row, col)
            col += 1
            if col > 2:
                col = 0
                row += 1
        
          
    def logout(self):
        from login import LoginWindow
        self.login_window = LoginWindow() 
        self.login_window.show()
        self.close()      

    def forward_to_dashboard(self):
        from main_user import MainDashboard
        self.main_dashboard_window = MainDashboard(self.session_email) 
        self.main_dashboard_window.show()
        self.close() 

    def make_sidebar_button(self, text, checked=False):
        btn = QPushButton(text)
        btn.setCheckable(True)
        btn.setChecked(checked)
        btn.setCursor(Qt.PointingHandCursor)
        btn.setMinimumHeight(46)
        return btn

    def make_stat_chip(self, text):
        chip = QLabel(text)
        chip.setStyleSheet("""
            background-color: rgba(255,255,255,0.16);
            color: white;
            padding: 7px 12px;
            border-radius: 12px;
            font-size: 12px;
            font-weight: 700;
        """)
        return chip

    def make_small_chip(self, text):
        chip = QLabel(text)
        chip.setStyleSheet("""
            background-color: #e8efec; 
            color: #3a5a54; 
            border: 1px solid #d1ddd9; 
            padding: 4px 8px; 
            border-radius: 8px; 
            font-size: 10px; 
            font-weight: 700;
        """)
        return chip

    def create_car_card(self, car):
        card = QFrame()
        card.setMinimumHeight(360)
        card.setMaximumHeight(360)
        
        card.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 1px solid #d1ddd9;
                border-radius: 15px;
            }
            QFrame:hover {
                border: 1px solid #cfd9e8;
            }
        """)

        layout = QVBoxLayout(card)
        layout.setContentsMargins(18, 18, 18, 18)
        layout.setSpacing(12)

        top_row = QHBoxLayout()

        name_wrap = QVBoxLayout()
        name_wrap.setSpacing(2)

        title = QLabel(f"{car['brand']} {car['model']}")
        title.setStyleSheet("""
            color: #1d2736;
            font-size: 18px;
            font-weight: 800;
            border: none;
        """)

        subtitle = QLabel(f'{car["cc"]} cc • {car["production_year"]}')
        subtitle.setStyleSheet("""
            color: #6b7788;
            font-size: 12px;
            font-weight: 500;
            border: none;
        """)

        name_wrap.addWidget(title)
        name_wrap.addWidget(subtitle)

        status_badge = QLabel(car["state"])
        if car["state"] == "Available":
            status_style = """
                background-color: #eafaf0;
                color: #1f9d55;
            """
        elif car["state"] == "Reserved":
            status_style = """
                background-color: #fff4e6;
                color: #d97706;
            """
        else:
            status_style = """
                background-color: #ffe9e9;
                color: #dc2626;
            """

        status_badge.setStyleSheet(f"""
            {status_style}
            padding: 6px 10px;
            border-radius: 11px;
            font-size: 11px;
            font-weight: 800;
        """)

        top_row.addLayout(name_wrap)
        top_row.addStretch()
        top_row.addWidget(status_badge)

        image_box = QFrame()
        image_box.setFixedHeight(140) 
        
        image_box.setStyleSheet("""
            QFrame {
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:0,
                    stop:0 #eef4fb,
                    stop:1 #f8fbff
                );
                border: 1px solid #eef2f7;
                border-radius: 12px;
            }
        """)
        def open_date_picker(self):
            dialog = DatePickerDialog(self)
            if dialog.exec() == QDialog.Accepted:
                start_date, end_date = dialog.get_dates()
                
                # Εδώ έχεις τις ημερομηνίες έτοιμες για το st = datetime.strptime(...)
                print(f"Selected Start: {start_date}")
                print(f"Selected End: {end_date}")
                
                # Μπορείς να ενημερώσεις το UI ή να φιλτράρεις τα αυτοκίνητα
                self.btn_pick_dates.setText(f"📅 {start_date} to {end_date}")
        image_layout = QVBoxLayout(image_box)
        image_layout.setContentsMargins(0, 0, 0, 0)
        
        car_image = QLabel()
        car_image.setAlignment(Qt.AlignCenter)
        car_image.setStyleSheet("background: transparent; border: none;")

        img_path = car["image_path"].lstrip("/")
        pixmap = QPixmap(img_path)
    
        if not pixmap.isNull():
            scaled_pixmap = pixmap.scaled(
                340, 140, 
                Qt.KeepAspectRatioByExpanding, 
                Qt.SmoothTransformation
            )
            
            car_image.setFixedSize(340, 140) 
            car_image.setPixmap(scaled_pixmap)
            
        else:
            car_image.setText("🚗")
            car_image.setStyleSheet("font-size: 34px; color: #5c6b7c; background: transparent;")

        image_layout.addWidget(car_image, alignment=Qt.AlignCenter)

        chips_row = QHBoxLayout()
        chips_row.setSpacing(8)

        chips_row.addWidget(self.make_small_chip(f'{car["doors"]} Doors'))
        chips_row.addWidget(self.make_small_chip(f'{car["seats"]} Seats'))
        chips_row.addWidget(self.make_small_chip(car["transmission_type"]))
        chips_row.addWidget(self.make_small_chip(car["fuel_type"]))
        chips_row.addStretch()

        info_wrap = QVBoxLayout()
        info_wrap.setSpacing(4)

        branch = QLabel("Athens Center")
        branch.setStyleSheet("""
            color: #263142;
            font-size: 13px;
            font-weight: 700;
            border: none;
        """)

        extra = QLabel("Vehicle details available")
        extra.setStyleSheet("""
            color: #7a8799;
            font-size: 11px;
            border: none;
        """)

        info_wrap.addWidget(branch)
        info_wrap.addWidget(extra)

        bottom_row = QHBoxLayout()
        bottom_row.setSpacing(15) 

        btn_details = QPushButton("Details")
        btn_details.setCursor(Qt.PointingHandCursor)
        btn_details.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: #334155;
                border: 1px solid #d5deeb;
                border-radius: 10px;
                padding: 10px 16px;
                font-size: 13px;
                font-weight: 700;
            }
            QPushButton:hover {
                background-color: #f8fafc;
            }
        """)

        btn_select = QPushButton("Select")
        btn_select.setCursor(Qt.PointingHandCursor)

        if car["state"] == "Available":
            btn_select.setStyleSheet("""
                QPushButton {
                    background-color: #2563eb;
                    color: white;
                    border: none;
                    border-radius: 10px;
                    padding: 10px 18px;
                    font-size: 13px;
                    font-weight: 800;
                }
                QPushButton:hover {
                    background-color: #1d4ed8;
                }
            """)
        else:
            btn_select.setEnabled(False)
            btn_select.setStyleSheet("""
                QPushButton {
                    background-color: #dbe3ef;
                    color: #7b8795;
                    border: none;
                    border-radius: 10px;
                    padding: 10px 18px;
                    font-size: 13px;
                    font-weight: 800;
                }
            """)

        price_label = QLabel(f"€{car['price']} <span style='color: #6b7788; font-size: 12px; font-weight: 500;'>/ day</span>")
        price_label.setStyleSheet("""
            color: #1d2736;
            font-size: 18px;
            font-weight: 800;
            background: transparent;
        """)

        bottom_row.addWidget(btn_details)
        bottom_row.addStretch()
        bottom_row.addWidget(price_label) 
        bottom_row.addWidget(btn_select)

        layout.addLayout(top_row)
        layout.addWidget(image_box)
        layout.addLayout(chips_row)
        layout.addLayout(info_wrap)
        layout.addStretch()
        layout.addLayout(bottom_row)

        return card

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ReservationsWindow(None)
    window.show()
    sys.exit(app.exec())