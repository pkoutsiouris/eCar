import sys
import os
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QScrollArea, QGridLayout, QFrame, QButtonGroup, 
    QDialog, QFormLayout, QLineEdit, QStackedWidget, QComboBox, QDateEdit
)
from PySide6.QtCore import Qt, QTimer, QDate
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
        
        message = QLabel(f"Η συνολική τιμή είναι: <b>€{total_price}</b>")
        message.setAlignment(Qt.AlignCenter)
        message.setStyleSheet("font-size: 16px; margin: 20px;")
        layout.addWidget(message)

        question = QLabel("Θέλετε να προχωρήσετε στην κράτηση;")
        question.setAlignment(Qt.AlignCenter)
        layout.addWidget(question)

        button_layout = QHBoxLayout()
        self.btn_yes = QPushButton("Yes")
        self.btn_no = QPushButton("No")
        
        self.btn_yes.setStyleSheet("background-color: #1f9d55; color: white; padding: 8px; font-weight: bold;")
        self.btn_no.setStyleSheet("background-color: #ef4444; color: white; padding: 8px; font-weight: bold;")
        
        button_layout.addWidget(self.btn_yes)
        button_layout.addWidget(self.btn_no)
        
        layout.addLayout(button_layout)

        self.btn_yes.clicked.connect(self.accept) 
        self.btn_no.clicked.connect(self.reject)  

class CarDetailsDialog(QDialog):
    def __init__(self, car, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Car Details")
        self.setMinimumWidth(450)
        
        self.setStyleSheet("""
            QDialog {
                background-color: #1a1a1a;
                border-radius: 12px;
            }
            QLabel {
                color: #ffffff;
                background: transparent;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(12)

        title = QLabel(f"{car['brand']} {car['model']}")
        title.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(title)

        subtitle = QLabel(f"{car['cc']} cc • {car['production_year']}")
        subtitle.setStyleSheet("color: #a3a3a3; font-size: 13px;")
        layout.addWidget(subtitle)

        layout.addSpacing(8)

        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        filename = f"{car['image_path']}.png"
        full_path = os.path.join(BASE_DIR, "imgs", filename)
        
        car_image = QLabel()
        pixmap = QPixmap(full_path)
        if not pixmap.isNull():
            scaled_pixmap = pixmap.scaled(400, 150, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
            car_image.setPixmap(scaled_pixmap)
        else:
            car_image.setText("[εικόνα]")
            car_image.setAlignment(Qt.AlignCenter)
            car_image.setStyleSheet("color: #a3a3a3; border: 1px dashed #444; padding: 40px;")
            
        layout.addWidget(car_image)
        layout.addSpacing(10)

        desc = QLabel(car['car_description'])
        desc.setWordWrap(True)
        desc.setStyleSheet("""
            color: #d4d4d4;
            font-size: 14px;
            line-height: 1.4;
        """)
        layout.addWidget(desc)
        layout.addSpacing(10)

        specs_str = f"{car['doors']} Doors  |  {car['seats']} Seats  |  {car['transmission_type']}  |  {car['fuel_type']}"
        specs_lbl = QLabel(specs_str)
        specs_lbl.setStyleSheet("font-size: 13px; font-weight: bold;")
        layout.addWidget(specs_lbl)
        
        layout.addSpacing(15)

        branch = QLabel("Athens Center")
        branch.setStyleSheet("font-size: 14px; font-weight: bold;")
        layout.addWidget(branch)

        benefits_title = QLabel("Additional Benefits")
        benefits_title.setStyleSheet("color: #a3a3a3; font-size: 14px;")
        layout.addWidget(benefits_title)

        benefits_layout = QVBoxLayout()
        benefits_layout.setSpacing(6)
        
        benefits = [
            "Full insurance package",
            "Instant confirmation",
            "Free cancellation",
            "Same to same fuel policy"
        ]

        for b in benefits:
            b_lbl = QLabel(f"✓ {b}")
            b_lbl.setStyleSheet("color: #ffb84d; font-size: 13px; font-weight: bold;") 
            benefits_layout.addWidget(b_lbl)

        layout.addLayout(benefits_layout)
        layout.addSpacing(20)

        bottom_row = QHBoxLayout()
        price_lbl = QLabel(f"€{car['price']} <span style='font-size: 12px; font-weight: normal;'>/ day</span>")
        price_lbl.setStyleSheet("font-size: 16px; font-weight: bold;")
        bottom_row.addWidget(price_lbl)
        bottom_row.addStretch()
        layout.addLayout(bottom_row)

class MainDealerWindow(QMainWindow):
    def __init__(self, session_email: str):
        super().__init__()
        self.setWindowTitle("Car Rental - Dashboard")
        self.setWindowIcon(QIcon('assets/icon.png'))
        self.resize(1280, 820)
        self.session_email = session_email
        
        self.selected_start_date = None
        self.selected_end_date = None
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

        # Sidebar
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
        logo.setStyleSheet("color: white; font-size: 24px; font-weight: 800;")
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

        # Main Content Stack
        self.stacked_widget = QStackedWidget()
        shell_layout.addWidget(self.stacked_widget)

        self.dashboard_container = QWidget()
        self.dashboard_container.setStyleSheet("background-color: transparent;")
        content_layout = QVBoxLayout(self.dashboard_container) 
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)

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

        title = QLabel("Available Cars")
        title.setStyleSheet("color: white; font-size: 34px; font-weight: 800; background: transparent;")

        subtitle = QLabel("Browse vehicles, view availability and continue to reservation.")
        subtitle.setStyleSheet("color: rgba(255,255,255,0.88); font-size: 14px; font-weight: 500; background: transparent;")

        self.stats_row = QHBoxLayout()
        self.stats_row.setSpacing(12)
        self.stat_chip_cars = self.make_stat_chip("0 Cars")
        self.stat_chip_available = self.make_stat_chip("Available")
        self.stats_row.addWidget(self.stat_chip_cars)
        self.stats_row.addWidget(self.stat_chip_available)
        self.stats_row.addStretch()

        banner_layout.addStretch()
        banner_layout.addWidget(title)
        banner_layout.addWidget(subtitle)
        banner_layout.addSpacing(8)
        banner_layout.addLayout(self.stats_row)

        content_layout.addWidget(banner)
        self.date_picker_panel = QFrame() 

        # Cars Panel(Toolbar + Grid)
        self.cars_panel = QWidget()
        self.cars_panel.setStyleSheet("background-color: transparent;")
        cars_panel_layout = QVBoxLayout(self.cars_panel)
        cars_panel_layout.setContentsMargins(0, 0, 0, 0)
        cars_panel_layout.setSpacing(0)
        self.cars_panel.show() 

        # Toolbar
        toolbar = QWidget()
        toolbar.setFixedHeight(72)
        toolbar.setStyleSheet("background-color: white; border-bottom: 1px solid #e0e8e5;")

        toolbar_layout = QHBoxLayout(toolbar)
        toolbar_layout.setContentsMargins(28, 0, 28, 0)
        toolbar_layout.setSpacing(12)

        sort_label = QLabel("Sort by:")
        sort_label.setStyleSheet("color: #2b3547; font-size: 14px; font-weight: 700; background: transparent;")

        self.sort_combo = QComboBox()
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
                background-color: white; color: #2b3547; border: 1px solid #ffffff;
                border-radius: 10px; padding: 8px 12px; font-size: 13px; font-weight: 600;
            }
            QComboBox:hover { border: 1px solid #6a9a83; }
        """)

        self.right_info_label = QLabel(f"Showing <b>{len(self.cars)}</b> vehicles")
        self.right_info_label.setStyleSheet("color: #556070; font-size: 14px; background: transparent;")

        btn_filter = QPushButton("Filter")
        btn_filter.clicked.connect(self.open_filters)
        btn_filter.setStyleSheet("""
            QPushButton {
                background-color: #6a9a83; color: white; border-radius: 10px;
                padding: 10px 18px; font-weight: bold; font-size: 13px;
            }
            QPushButton:hover { background-color: #5a8571; }
        """)
        self.sort_combo.currentTextChanged.connect(self.apply_sort)

        toolbar_layout.addWidget(sort_label)
        toolbar_layout.addWidget(self.sort_combo)
        toolbar_layout.addStretch()
        toolbar_layout.addWidget(self.right_info_label)
        toolbar_layout.addWidget(btn_filter)
        cars_panel_layout.addWidget(toolbar)

        # Scroll Area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("""
            QScrollArea { border: none; background-color: #f5f7fb; }
            QScrollBar:vertical { background: #edf2f9; width: 12px; margin: 6px 2px; border-radius: 6px; }
            QScrollBar::handle:vertical { background: #c7d3e4; border-radius: 6px; min-height: 30px; }
        """)

        scroll_content = QWidget()
        scroll_content.setStyleSheet("background-color: #f5f7fb;")

        self.grid = QGridLayout(scroll_content)
        self.grid.setContentsMargins(28, 24, 28, 28)
        self.grid.setHorizontalSpacing(22)
        self.grid.setVerticalSpacing(22)

        scroll.setWidget(scroll_content)
        cars_panel_layout.addWidget(scroll)
        content_layout.addWidget(self.cars_panel)

        # Pages Setup
        self.res_page = ReservationsWindow(self.session_email)
        self.settings_page = self.create_settings_page()

        self.stacked_widget.addWidget(self.dashboard_container) 
        self.stacked_widget.addWidget(self.res_page)            
        self.stacked_widget.addWidget(self.settings_page)       
        self.load_all_cars_immediately()

    def load_all_cars_immediately(self):
        """Φέρνει απευθείας όλα τα αυτοκίνητα χωρίς φιλτράρισμα ημερομηνιών."""
        available_cars = functions.GetCars()
        if available_cars is None:
            available_cars = []
        self.cars = available_cars

        self.stat_chip_cars.setText(f"{len(self.cars)} Cars")
        self.update_grid(self.cars)
        available_count = sum(1 for car in self.cars if car["state"] == "Available")
        self.right_info_label.setText(f"Showing <b>{len(self.cars)}</b> vehicles ({available_count} Available)")

    def update_grid(self, cars_list):
        for i in reversed(range(self.grid.count())):
            widget = self.grid.itemAt(i).widget()
            if widget:
                widget.deleteLater()
                
        if not cars_list:           
            no_cars_label = QLabel("No cars matched these criteria.")
            no_cars_label.setAlignment(Qt.AlignCenter)
            no_cars_label.setStyleSheet("color: #8a94a6; font-size: 20px; font-weight: bold; margin-top: 60px;")
            self.grid.addWidget(no_cars_label, 0, 0, 1, 3) 
            self.right_info_label.setText("Showing <b>0</b> vehicles")
            return 
                
        row = 0
        col = 0
        for car in cars_list:
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

        start = self.selected_start_date
        end = self.selected_end_date

        if selected_sort == "Price: Low to High":
            sorted_cars = functions.GetSortedCars("price", descending=False, start_date=start, end_date=end)
        elif selected_sort == "Price: High to Low":
            sorted_cars = functions.GetSortedCars("price", descending=True, start_date=start, end_date=end)
        elif selected_sort == "Year: Newest First":
            sorted_cars = functions.GetSortedCars("year", descending=True, start_date=start, end_date=end)
        elif selected_sort == "Year: Oldest First":
            sorted_cars = functions.GetSortedCars("year", descending=False, start_date=start, end_date=end)
        elif selected_sort == "CC: Low to High":
            sorted_cars = functions.GetSortedCars("cc", descending=False, start_date=start, end_date=end)
        elif selected_sort == "CC: High to Low":
            sorted_cars = functions.GetSortedCars("cc", descending=True, start_date=start, end_date=end)
        else:
            return

        if isinstance(sorted_cars, list):
            self.update_grid(sorted_cars)
            self.right_info_label.setText(f"Showing <b>{len(sorted_cars)}</b> vehicles")
        else:
            self.update_grid([])
            self.right_info_label.setText("Showing <b>0</b> vehicles")    
            
    def open_filters(self):
        dialog = FilterDialog(self)
        if dialog.exec():
            try:
                price, year, cc, hp = dialog.get_values()
                start = self.selected_start_date
                end = self.selected_end_date

                if all(v is None for v in [price, year, cc, hp]):
                    filtered = functions.GetCars() 
                else:
                    filtered = functions.FilterCars(price, year, cc, hp, start_date=start, end_date=end)
                
                if isinstance(filtered, list):
                    self.update_grid(filtered)
                    self.right_info_label.setText(f"Showing <b>{len(filtered)}</b> vehicles")
                else:
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
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #6a9a83, stop:1 #3a5a54);
            }
        """)
        banner_layout = QVBoxLayout(banner)
        banner_layout.setContentsMargins(32, 24, 32, 24)
        title = QLabel("Settings")
        title.setStyleSheet("color: white; font-size: 34px; font-weight: 800; background: transparent;")
        subtitle = QLabel("Change your account password.")
        subtitle.setStyleSheet("color: rgba(255,255,255,0.88); font-size: 14px; font-weight: 500; background: transparent;")
        banner_layout.addStretch()
        banner_layout.addWidget(title)
        banner_layout.addWidget(subtitle)
        content_layout.addWidget(banner)

        body = QWidget()
        body.setStyleSheet("background-color: #f5f7fb;")
        body_layout = QVBoxLayout(body)
        body_layout.setContentsMargins(28, 28, 28, 28)

        form_card = QFrame()
        form_card.setFixedWidth(520)
        form_card.setStyleSheet("QFrame { background-color: white; border: 1px solid #ffffff; border-radius: 15px; }")
        form_layout = QVBoxLayout(form_card)
        form_layout.setContentsMargins(28, 28, 28, 28)
        form_layout.setSpacing(14)

        card_title = QLabel("Change Password")
        card_title.setStyleSheet("color: #1d2736; font-size: 22px; font-weight: 800; background: transparent;")

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
            QLineEdit { background-color: #f8fafc; color: #1f2937; border: 1px solid #ffffff; border-radius: 10px; padding: 10px 12px; font-size: 14px; }
            QLineEdit:focus { border: 1px solid #6a9a83; background-color: white; }
        """
        self.old_password_input.setStyleSheet(input_style)
        self.new_password_input.setStyleSheet(input_style)
        self.confirm_password_input.setStyleSheet(input_style)

        btn_change_password = QPushButton("Change Password")
        btn_change_password.setCursor(Qt.PointingHandCursor)
        btn_change_password.clicked.connect(self.change_password)
        btn_change_password.setStyleSheet("QPushButton { background-color: #6a9a83; color: white; font-weight: 800; border-radius: 10px; padding: 12px; }")

        self.password_status_label = QLabel("")

        form_layout.addWidget(card_title)
        form_layout.addWidget(self.old_password_input)
        form_layout.addWidget(self.new_password_input)
        form_layout.addWidget(self.confirm_password_input)
        form_layout.addWidget(btn_change_password)
        form_layout.addWidget(self.password_status_label)

        body_layout.addWidget(form_card, alignment=Qt.AlignTop | Qt.AlignHCenter)
        content_layout.addWidget(body)
        return settings_page

    def change_password(self):
        old_password = self.old_password_input.text().strip()
        new_password = self.new_password_input.text().strip()
        confirm_password = self.confirm_password_input.text().strip()

        if not old_password or not new_password or not confirm_password:
            self.password_status_label.setText("Please fill in all fields.")
            self.password_status_label.setStyleSheet("color: #dc2626; font-size: 13px; font-weight: 600;")
            return

        if new_password != confirm_password:
            self.password_status_label.setText("New passwords do not match.")
            self.password_status_label.setStyleSheet("color: #dc2626; font-size: 13px; font-weight: 600;")
            return

        success, message = functions.ChangePassword(self.session_email, old_password, new_password)
        self.password_status_label.setText(message)
        if success:
            self.old_password_input.clear()
            self.new_password_input.clear()
            self.confirm_password_input.clear()
            self.password_status_label.setStyleSheet("color: #1f9d55; font-size: 13px; font-weight: 600;")
        else:
            self.password_status_label.setStyleSheet("color: #dc2626; font-size: 13px; font-weight: 600;")
    
    def reservations(self):  
        self.stacked_widget.setCurrentIndex(1)

    def show_dashboard(self):
        self.stacked_widget.setCurrentIndex(0)
        self.refresh_dashboard()

    def refresh_dashboard(self):
        self.load_all_cars_immediately()
    
    def make_sidebar_button(self, text, checked=False):
        btn = QPushButton(text)
        btn.setCheckable(True)
        btn.setChecked(checked)
        btn.setCursor(Qt.PointingHandCursor)
        btn.setMinimumHeight(46)
        return btn

    def make_stat_chip(self, text):
        chip = QLabel(text)
        chip.setStyleSheet("background-color: rgba(255,255,255,0.16); color: white; padding: 7px 12px; border-radius: 12px; font-size: 12px; font-weight: 700;")
        return chip

    def make_small_chip(self, text):
        chip = QLabel(text)
        chip.setStyleSheet("background-color: #e8efec; color: #3a5a54; border: 1px solid #ffffff; padding: 4px 8px; border-radius: 8px; font-size: 10px; font-weight: 700;")
        return chip

    def handle_rent(self, car):
        print("")
    def show_car_details(self, car):
        dialog = CarDetailsDialog(car, self)
        dialog.exec()

    def create_car_card(self, car):
        card = QFrame()
        card.setFixedWidth(320)
        card.setMinimumHeight(460)
        card.setMaximumHeight(460)
        card.setStyleSheet("QFrame { background-color: white; border: 1px solid #ffffff; border-radius: 15px; } QFrame:hover { border: 1px solid #ffffff; }")

        layout = QVBoxLayout(card)
        layout.setContentsMargins(18, 18, 18, 18)
        layout.setSpacing(12)

        top_row = QHBoxLayout()
        name_wrap = QVBoxLayout()
        name_wrap.setSpacing(2)

        title = QLabel(f"{car['brand']} {car['model']}")
        title.setStyleSheet("color: #1d2736; font-size: 18px; font-weight: 800;")
        subtitle = QLabel(f'{car["cc"]} cc • {car["production_year"]}')
        subtitle.setStyleSheet("color: #6b7788; font-size: 12px; font-weight: 500;")
        name_wrap.addWidget(title)
        name_wrap.addWidget(subtitle)

        status_badge = QLabel(car["state"])
        if car["state"] == "Available":
            status_style = "background-color: #eafaf0; color: #1f9d55;"
        elif car["state"] == "Reserved":
            status_style = "background-color: #fff4e6; color: #d97706;"
        else:
            status_style = "background-color: #ffe9e9; color: #dc2626;"

        status_badge.setStyleSheet(f"{status_style} padding: 6px 10px; border-radius: 11px; font-size: 11px; font-weight: 800;")
        top_row.addLayout(name_wrap)
        top_row.addStretch()
        top_row.addWidget(status_badge)

        image_box = QFrame()
        image_box.setFixedHeight(220) 
        image_box.setStyleSheet("QFrame { background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #eef4fb, stop:1 #f8fbff); border: 1px solid #ffffff; border-radius: 12px; }")
        image_layout = QVBoxLayout(image_box)
        image_layout.setContentsMargins(0, 0, 0, 0)
        
        car_image = QLabel()
        car_image.setAlignment(Qt.AlignCenter)

        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        filename = f"{car['image_path']}.png"
        full_path = os.path.join(BASE_DIR, "imgs", filename)
        pixmap = QPixmap(full_path)
    
        if not pixmap.isNull():
            scaled_pixmap = pixmap.scaled(280, 200, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
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
        branch = QLabel("Athens Center")
        branch.setStyleSheet("color: #263142; font-size: 13px; font-weight: 700;")
        extra = QLabel("Vehicle details available")
        extra.setStyleSheet("color: #7a8799; font-size: 11px;")
        info_wrap.addWidget(branch)
        info_wrap.addWidget(extra)

        bottom_row = QHBoxLayout()
        btn_details = QPushButton("Details")
        btn_details.setCursor(Qt.PointingHandCursor)
        btn_details.clicked.connect(lambda checked=False, c=car: self.show_car_details(c))
        btn_details.setStyleSheet("QPushButton { background-color: white; color: #334155; border: 1px solid #ffffff; border-radius: 10px; padding: 10px 16px; font-size: 13px; font-weight: 700; } QPushButton:hover { background-color: #f8fafc; }")

        btn_rent = QPushButton("Rent")
        btn_rent.setCursor(Qt.PointingHandCursor)
        btn_rent.clicked.connect(lambda checked=False, c=car: self.handle_rent(c))

        if car["state"] == "Available":
            btn_rent.setStyleSheet("QPushButton { background-color: #1f9d55; color: white; border: none; border-radius: 10px; padding: 10px 18px; font-size: 13px; font-weight: 800; } QPushButton:hover { background-color: #1F7755; }")
        else:
            btn_rent.setEnabled(False)
            btn_rent.setStyleSheet("QPushButton { background-color: #dbe3ef; color: #7b8795; border: none; border-radius: 10px; padding: 10px 18px; font-size: 13px; font-weight: 800; }")

        price_label = QLabel(f"€{car['price']} <span style='color: #6b7788; font-size: 12px; font-weight: 500;'>/ day</span>")
        price_label.setStyleSheet("color: #1d2736; font-size: 18px; font-weight: 800; background: transparent;")

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
    window = MainDealerWindow(None)
    window.show()
    sys.exit(app.exec())