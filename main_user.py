import sys
import os
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QScrollArea, QGridLayout, QFrame, QButtonGroup, QDialog , QFormLayout, QLineEdit, QStackedWidget, QComboBox, 
)
from PySide6.QtCore import Qt, QTimer
from back_end import functions
from datetime import datetime
from reservation_page import ReservationsWindow
from PySide6.QtGui import QPixmap, QIcon

class FilterDialog(QDialog):
    def __init__(self, parent=None): 
        super().__init__(parent)
        self.setWindowTitle("Filter")

        layout = QVBoxLayout(self)

        form = QFormLayout()

        self.price_input = QLineEdit()
        self.year_input = QLineEdit()
        self.cc_input = QLineEdit()
        self.hp_input = QLineEdit()

        self.price_input.setPlaceholderText("e.g. 50")
        self.year_input.setPlaceholderText("e.g. 2020")
        self.cc_input.setPlaceholderText("e.g. 1400")
        self.hp_input.setPlaceholderText("e.g. 100")

        form.addRow("Max Price (€):", self.price_input)
        form.addRow("Min Year:", self.year_input)
        form.addRow("Min CC:", self.cc_input)
        form.addRow("Min HP:", self.hp_input)

        layout.addLayout(form)

        btn = QPushButton("Apply")
        btn.clicked.connect(self.accept)
        layout.addWidget(btn)

    def get_values(self):
        p = self.price_input.text().strip()
        y = self.year_input.text().strip()
        cc = self.cc_input.text().strip()
        hp = self.hp_input.text().strip()

        return (
            float(p) if p else None,
            int(y) if y else None,
            int(cc) if cc else None,
            int(hp) if hp else None
        )
class RentDetails(QDialog):
    def __init__(self, total_price, parent=None): 
        super().__init__(parent)
        self.setWindowTitle("Confirm Reservation")
        self.setFixedWidth(300)
        
        layout = QVBoxLayout(self)
        
        # Εμφάνιση Τιμής
        message = QLabel(f"Η συνολική τιμή είναι: <b>€{total_price}</b>")
        message.setAlignment(Qt.AlignCenter)
        message.setStyleSheet("font-size: 16px; margin: 20px;")
        layout.addWidget(message)

        question = QLabel("Θέλετε να προχωρήσετε στην κράτηση;")
        question.setAlignment(Qt.AlignCenter)
        layout.addWidget(question)

        # Buttons
        button_layout = QHBoxLayout()
        self.btn_yes = QPushButton("Yes")
        self.btn_no = QPushButton("No")
        
        # Styling
        self.btn_yes.setStyleSheet("background-color: #1f9d55; color: white; padding: 8px; font-weight: bold;")
        self.btn_no.setStyleSheet("background-color: #ef4444; color: white; padding: 8px; font-weight: bold;")
        
        button_layout.addWidget(self.btn_yes)
        button_layout.addWidget(self.btn_no)
        
        layout.addLayout(button_layout)

        # Connections
        self.btn_yes.clicked.connect(self.accept) # Κλείνει το dialog με True
        self.btn_no.clicked.connect(self.reject)  # Κλείνει το dialog με False

class MainDashboard(QMainWindow):
    def __init__(self,session_email:str):
        super().__init__()
        self.setWindowTitle("Car Rental - Dashboard")
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

        btn_dashboard = self.make_sidebar_button("Dashboard", checked=True)
        btn_dashboard.clicked.connect(self.show_dashboard)
        btn_reservations = self.make_sidebar_button("Reservations")
        btn_reservations.clicked.connect(self.reservations)
        btn_settings = self.make_sidebar_button("Settings")
        btn_settings.clicked.connect(self.show_settings)

        btn_logout = self.make_sidebar_button("Logout")

        self.nav_group.addButton(btn_dashboard)
        self.nav_group.addButton(btn_reservations)
        self.nav_group.addButton(btn_settings)

        sidebar_layout.addWidget(btn_dashboard)
        sidebar_layout.addWidget(btn_reservations)
        sidebar_layout.addWidget(btn_settings)
        sidebar_layout.addStretch()

        self.btn_reservations = QPushButton("Reservations")
        self.btn_reservations.setCursor(Qt.PointingHandCursor)
        self.btn_reservations.setMinimumHeight(46)
        self.btn_reservations.clicked.connect(self.reservations)

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
        # =========================
        # Main content (Η Στοίβα με τις σελίδες)
        # =========================
        self.stacked_widget = QStackedWidget()
        shell_layout.addWidget(self.stacked_widget)

        # Κουτί για το Dashboard
        self.dashboard_container = QWidget()
        self.dashboard_container.setStyleSheet("background-color: transparent;")
        content_layout = QVBoxLayout(self.dashboard_container) # Προσοχή, τώρα μπαίνει στο dashboard_container
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)

 

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

        title = QLabel("Available Cars")
        title.setStyleSheet("""
            color: white;
            font-size: 34px;
            font-weight: 800;
            background: transparent;
        """)

        subtitle = QLabel("Browse vehicles, view availability and continue to reservation.")
        subtitle.setStyleSheet("""
            color: rgba(255,255,255,0.88);
            font-size: 14px;
            font-weight: 500;
            background: transparent;
        """)

        stats_row = QHBoxLayout()
        stats_row.setSpacing(12)
        stats_row.addWidget(self.make_stat_chip(f"{len(self.cars)} Cars"))
        stats_row.addWidget(self.make_stat_chip("Available"))
        stats_row.addStretch()

        banner_layout.addLayout(banner_top)
        banner_layout.addStretch()
        banner_layout.addWidget(title)
        banner_layout.addWidget(subtitle)
        banner_layout.addSpacing(8)
        banner_layout.addLayout(stats_row)

        content_layout.addWidget(banner)
        
        #Logout Button
        btn_logout = QPushButton(" Logout")
        btn_logout.setCursor(Qt.PointingHandCursor)
        btn_logout.setMinimumHeight(46)
        btn_logout.clicked.connect(self.logout)


        # Toolbar
        toolbar = QWidget()
        toolbar.setFixedHeight(72)
        toolbar.setStyleSheet("background-color: white; border-bottom: 1px solid #e0e8e5;")

        toolbar_layout = QHBoxLayout(toolbar)
        toolbar_layout.setContentsMargins(28, 0, 28, 0)
        toolbar_layout.setSpacing(12)

        sort_label = QLabel("Sort by:")
        sort_label.setStyleSheet("""
            color: #2b3547;
            font-size: 14px;
            font-weight: 700;
            background: transparent;
        """)

        self.sort_combo = QComboBox()

        self.sort_combo.view().setStyleSheet("""
            background-color: white;
            color: #2b3547;
            border: 1px solid #d1ddd9;
            selection-background-color: #6a9a83;
            selection-color: white;
        """)
        self.sort_combo.addItems([
            "Price: Low to High",
            "Price: High to Low",
            "Year: Newest First",
            "Year: Oldest First",
            "CC: Low to High",
            "CC: High to Low"
        ])
        self.sort_combo.setPlaceholderText("Recommended")
        self.sort_combo.setCurrentIndex(-1)
        self.sort_combo.setMinimumHeight(38)
        self.sort_combo.setCursor(Qt.PointingHandCursor)

        self.sort_combo.setStyleSheet("""
            QComboBox {
                background-color: white;
                color: #2b3547;
                border: 1px solid #d1ddd9;
                border-radius: 10px;
                padding: 8px 12px;
                font-size: 13px;
                font-weight: 600;
            }
            QComboBox:hover {
                border: 1px solid #6a9a83;
            }
            QComboBox QAbstractItemView {
                background-color: white;
                color: #2b3547;
                border: 1px solid #d1ddd9;
                selection-background-color: #6a9a83;
                selection-color: white;
                outline: none;
            }
        """)

        

        self.right_info_label = QLabel(f"Showing <b>{len(self.cars)}</b> vehicles")
        self.right_info_label.setStyleSheet("""
            color: #556070;
            font-size: 14px;
            background: transparent;
        """)

        btn_filter = QPushButton("Filter")
        btn_filter.setEnabled(True)  # frontend only
        btn_filter.clicked.connect(self.open_filters)
        btn_filter.setStyleSheet("""
        QPushButton {
            background-color: #6a9a83; 
            color: white; 
            border-radius: 10px; 
            padding: 10px 18px; 
            font-weight: bold; 
            font-size: 13px;
            }
            QPushButton:hover { 
                background-color: #5a8571; 
            }                
            QPushButton:pressed {
                background-color: #5a8571; 
                padding-top: 12px;        
                padding-bottom: 8px;       
               
            }
        """)
        self.sort_combo.currentTextChanged.connect(self.apply_sort)

    

        toolbar_layout.addWidget(sort_label)
        toolbar_layout.addWidget(self.sort_combo)
        toolbar_layout.addStretch()
        toolbar_layout.addWidget(self.right_info_label)
        toolbar_layout.addWidget(btn_filter)

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


        self.grid = QGridLayout(scroll_content)
        self.grid.setContentsMargins(28, 24, 28, 28)
        self.grid.setHorizontalSpacing(22)
        self.grid.setVerticalSpacing(22)
        self.update_grid(self.cars)

        scroll.setWidget(scroll_content)
        content_layout.addWidget(scroll)
        # Φέρνουμε τη σελίδα των Reservations από το άλλο αρχείο
        self.res_page = ReservationsWindow(self.session_email)
        self.settings_page = self.create_settings_page()

        # Βάζουμε τις 3 σελίδες στο QStackedWidget
        self.stacked_widget.addWidget(self.dashboard_container) # Index 0
        self.stacked_widget.addWidget(self.res_page)            # Index 1
        self.stacked_widget.addWidget(self.settings_page)       # Index 2         # Index 1


    

    def update_grid(self, cars_list):
        for i in reversed(range(self.grid.count())):
            widget = self.grid.itemAt(i).widget()
            if widget:
                widget.deleteLater()
                
        if not cars_list:   # Filtered list is empty (no cars match the criteria           
                no_cars_label = QLabel("No cars matched these criteria.")
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

# ALAGH AVAILABILITY
        row = 0
        col = 0
        for car in cars_list:
            if car['state'] == 'Available':
                card = self.create_car_card(car)
                self.grid.addWidget(card, row, col)
                col += 1
                if col > 2:
                    col = 0
                    row += 1
        
    def apply_sort(self):
        selected_sort = self.sort_combo.currentText()

        if not selected_sort:
            return

        if selected_sort == "Price: Low to High":
            sorted_cars = functions.GetSortedCars("price", descending=False)

        elif selected_sort == "Price: High to Low":
            sorted_cars = functions.GetSortedCars("price", descending=True)

        elif selected_sort == "Year: Newest First":
            sorted_cars = functions.GetSortedCars("year", descending=True)

        elif selected_sort == "Year: Oldest First":
            sorted_cars = functions.GetSortedCars("year", descending=False)

        elif selected_sort == "CC: Low to High":
            sorted_cars = functions.GetSortedCars("cc", descending=False)

        elif selected_sort == "CC: High to Low":
            sorted_cars = functions.GetSortedCars("cc", descending=True)

        else:
            return

        if isinstance(sorted_cars, list):
            self.update_grid(sorted_cars)
            self.right_info_label.setText(f"Showing <b>{len(sorted_cars)}</b> vehicles")
        else:
            print(f"functions.py did not return a list: {sorted_cars}")
            self.update_grid([])
            self.right_info_label.setText("Showing <b>0</b> vehicles")    
            
 
    def open_filters(self):
        dialog = FilterDialog(self)

        if dialog.exec():
            try:
                price, year, cc, hp = dialog.get_values()
                
                if all(v is None for v in [price, year, cc, hp]):
                    filtered = functions.GetCars()
                else:
                    filtered = functions.FilterCars(price, year, cc, hp)
                
                if isinstance(filtered, list):
                    self.update_grid(filtered)
                else:
                    print(f"functions.py den esteile thn lista {filtered}")
                    self.update_grid([])

            except ValueError:
                print("Error please enter only numbers!")

    def logout(self):
        from login import LoginWindow
        self.login_window = LoginWindow() 
        self.login_window.show()
        self.close()    

    def show_settings(self):
        self.stacked_widget.setCurrentIndex(2)


    def create_settings_page(self):
        settings_page = QWidget()
        settings_page.setStyleSheet("background-color: transparent;")

        content_layout = QVBoxLayout(settings_page)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)

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

        title = QLabel("Settings")
        title.setStyleSheet("""
            color: white;
            font-size: 34px;
            font-weight: 800;
            background: transparent;
        """)

        subtitle = QLabel("Change your account password.")
        subtitle.setStyleSheet("""
            color: rgba(255,255,255,0.88);
            font-size: 14px;
            font-weight: 500;
            background: transparent;
        """)

        banner_layout.addStretch()
        banner_layout.addWidget(title)
        banner_layout.addWidget(subtitle)
        banner_layout.addSpacing(8)

        content_layout.addWidget(banner)

        body = QWidget()
        body.setStyleSheet("background-color: #f5f7fb;")

        body_layout = QVBoxLayout(body)
        body_layout.setContentsMargins(28, 28, 28, 28)
        body_layout.setSpacing(18)

        form_card = QFrame()
        form_card.setFixedWidth(520)
        form_card.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 1px solid #d1ddd9;
                border-radius: 15px;
            }
        """)

        form_layout = QVBoxLayout(form_card)
        form_layout.setContentsMargins(28, 28, 28, 28)
        form_layout.setSpacing(14)

        card_title = QLabel("Change Password")
        card_title.setStyleSheet("""
            color: #1d2736;
            font-size: 22px;
            font-weight: 800;
            background: transparent;
            border: none;
        """)

        

        self.old_password_input = QLineEdit()
        self.old_password_input.setPlaceholderText("Current password")
        self.old_password_input.setEchoMode(QLineEdit.Password)
        self.old_password_input.setMinimumHeight(44)

        self.new_password_input = QLineEdit()
        self.new_password_input.setPlaceholderText("New password")
        self.new_password_input.setEchoMode(QLineEdit.Password)
        self.new_password_input.setMinimumHeight(44)

        self.confirm_password_input = QLineEdit()
        self.confirm_password_input.setPlaceholderText("Confirm new password")
        self.confirm_password_input.setEchoMode(QLineEdit.Password)
        self.confirm_password_input.setMinimumHeight(44)

        input_style = """
            QLineEdit {
                background-color: #f8fafc;
                color: #1f2937;
                border: 1px solid #d1ddd9;
                border-radius: 10px;
                padding: 10px 12px;
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 1px solid #6a9a83;
                background-color: white;
            }
        """

        self.old_password_input.setStyleSheet(input_style)
        self.new_password_input.setStyleSheet(input_style)
        self.confirm_password_input.setStyleSheet(input_style)

        btn_change_password = QPushButton("Change Password")
        btn_change_password.setCursor(Qt.PointingHandCursor)
        btn_change_password.setMinimumHeight(46)
        btn_change_password.clicked.connect(self.change_password)
        btn_change_password.setStyleSheet("""
            QPushButton {
                background-color: #6a9a83;
                color: white;
                border: none;
                border-radius: 10px;
                padding: 10px 18px;
                font-size: 14px;
                font-weight: 800;
            }
            QPushButton:hover {
                background-color: #5a8571;
            }
            QPushButton:pressed {
                background-color: #4e7462;
                padding-top: 12px;
                padding-bottom: 8px;
            }
        """)

        self.password_status_label = QLabel("")
        self.password_status_label.setStyleSheet("""
            color: #6b7788;
            font-size: 13px;
            font-weight: 600;
            background: transparent;
            border: none;
        """)

        form_layout.addWidget(card_title)
        form_layout.addSpacing(8)
        form_layout.addWidget(self.old_password_input)
        form_layout.addWidget(self.new_password_input)
        form_layout.addWidget(self.confirm_password_input)
        form_layout.addSpacing(8)
        form_layout.addWidget(btn_change_password)
        form_layout.addWidget(self.password_status_label)

        body_layout.addWidget(form_card, alignment=Qt.AlignTop | Qt.AlignHCenter)
        body_layout.addStretch()

        content_layout.addWidget(body)

        return settings_page

    def change_password(self):
        old_password = self.old_password_input.text().strip()
        new_password = self.new_password_input.text().strip()
        confirm_password = self.confirm_password_input.text().strip()

        if not old_password or not new_password or not confirm_password:
            self.password_status_label.setText("Please fill in all fields.")
            self.password_status_label.setStyleSheet("color: #dc2626; font-size: 13px; font-weight: 600; background: transparent; border: none;")
            return

        if new_password != confirm_password:
            self.password_status_label.setText("New passwords do not match.")
            self.password_status_label.setStyleSheet("color: #dc2626; font-size: 13px; font-weight: 600; background: transparent; border: none;")
            return

        success, message = functions.ChangePassword(
            self.session_email,
            old_password,
            new_password
        )

        if success:
            self.old_password_input.clear()
            self.new_password_input.clear()
            self.confirm_password_input.clear()

            self.password_status_label.setText(message)
            self.password_status_label.setStyleSheet("color: #1f9d55; font-size: 13px; font-weight: 600; background: transparent; border: none;")
        else:
            self.password_status_label.setText(message)
            self.password_status_label.setStyleSheet("color: #dc2626; font-size: 13px; font-weight: 600; background: transparent; border: none;")
    
    def reservations(self):  
        self.stacked_widget.setCurrentIndex(1)

    def show_dashboard(self):
        self.refresh_dashboard()
        self.stacked_widget.setCurrentIndex(0)
      
    




    def refresh_dashboard(self):
        self.cars = functions.GetCars() or []
        self.update_grid(self.cars)
        available_count = sum(1 for car in self.cars if car["state"] == "Available")
        self.right_info_label.setText(f"Showing <b>{available_count}</b> vehicles")
    
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
    def handle_rent(self, car): #NEW FUNC 
        from reservation_page import DatePickerDialog 
        #def CreateReservation(email:str,start_date: str, end_date:str, car_id:int):
        date_dialog = DatePickerDialog(self)
        if date_dialog.exec() == QDialog.Accepted:
            start_str, end_str = date_dialog.get_dates()
            st = datetime.strptime(start_str, "%Y-%m-%d %H:%M")
            et = datetime.strptime(end_str, "%Y-%m-%d %H:%M")
            days = (et - st).days
            if days <= 0: days = 1 # Μίνιμουμ 1 μέρα χρέωση
            
            total_price = days * car['price']
            # Αντί για CreateReservation, ανοίγουμε το PaymentWindow
            from pay import PaymentWindow
            print("Car plate from main: ", car['license_plate'])
            self.payment_screen = PaymentWindow(self.session_email, start_str, end_str,car)
            self.payment_screen.show()
            self.close() # Κλείνουμε το dashboard όσο πληρώνει
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

        image_layout = QVBoxLayout(image_box)
        image_layout.setContentsMargins(0, 0, 0, 0)
        
        car_image = QLabel()
        car_image.setAlignment(Qt.AlignCenter)
        car_image.setStyleSheet("background: transparent; border: none;")

        BASE_DIR = os.path.dirname(os.path.abspath(__file__))

        print("BASE_DIR IS ", BASE_DIR)
        
        # 1. Add the .png extension to the car's image name
        filename = f"{car['image_path']}.png"

        # 2. Join BASE_DIR, the "imgs" folder, and the filename all together
        full_path = os.path.join(BASE_DIR, "imgs", filename)

        print(full_path)
        pixmap = QPixmap(full_path)
    
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

        btn_rent = QPushButton("Rent")
        btn_rent.setCursor(Qt.PointingHandCursor)
        btn_rent.clicked.connect(lambda: self.handle_rent(car))

        if car["state"] == "Available":
            btn_rent.setStyleSheet("""
                QPushButton {
                    background-color: #1f9d55;
                    color: white;
                    border: none;
                    border-radius: 10px;
                    padding: 10px 18px;
                    font-size: 13px;
                    font-weight: 800;
                }
                QPushButton:hover {
                    background-color: #1F7755;
                }
            """)
        else:
            btn_rent.setEnabled(False)
            btn_rent.setStyleSheet("""
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
        bottom_row.addWidget(btn_rent)

        layout.addLayout(top_row)
        layout.addWidget(image_box)
        layout.addLayout(chips_row)
        layout.addLayout(info_wrap)
        layout.addStretch()
        layout.addLayout(bottom_row)

        return card

if __name__ == "__main__":
    
    app = QApplication(sys.argv)
    window = MainDashboard(None)
    window.show()
    sys.exit(app.exec())