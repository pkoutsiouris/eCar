import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QScrollArea, QGridLayout, QFrame, QButtonGroup, 
    QDialog, QFormLayout, QLineEdit, QStackedWidget, QComboBox, QDateEdit
)
from PySide6.QtCore import Qt, QTimer, QDate
from controller import functions
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

class CarDetailsDialog(QDialog):
    def __init__(self, car, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Car Details")
        self.setMinimumWidth(450)
        
        # Dark Theme Styling
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

        # 1. Όνομα & Κυβικά/Έτος
        title = QLabel(f"{car['brand']} {car['model']}")
        title.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(title)

        subtitle = QLabel(f"{car['cc']} cc • {car['production_year']}")
        subtitle.setStyleSheet("color: #a3a3a3; font-size: 13px;")
        layout.addWidget(subtitle)

        layout.addSpacing(8)

        

        # 2. Εικόνα Αυτοκινήτου
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

        # 3. Description
        desc = QLabel(car['car_description'])
        desc.setWordWrap(True)
        desc.setStyleSheet("""
            color: #d4d4d4;
            font-size: 14px;
            line-height: 1.4;
        """)

        layout.addWidget(desc)

        layout.addSpacing(10)

        # 3. Μπάρα Χαρακτηριστικών
        specs_str = f"{car['doors']} Doors  |  {car['seats']} Seats  |  {car['transmission_type']}  |  {car['fuel_type']}"
        specs_lbl = QLabel(specs_str)
        specs_lbl.setStyleSheet("font-size: 13px; font-weight: bold;")
        layout.addWidget(specs_lbl)
        
        layout.addSpacing(15)

        # 4. Τοποθεσία
        branch = QLabel("Athens Center")
        branch.setStyleSheet("font-size: 14px; font-weight: bold;")
        layout.addWidget(branch)

        # 5. Additional Benefits
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

        # 6. Τιμή & Rent Button
        bottom_row = QHBoxLayout()
        
        price_lbl = QLabel(f"€{car['price']} <span style='font-size: 12px; font-weight: normal;'>/ day</span>")
        price_lbl.setStyleSheet("font-size: 16px; font-weight: bold;")
        bottom_row.addWidget(price_lbl)
        
        bottom_row.addStretch()

        layout.addLayout(bottom_row)

class MainDashboard(QMainWindow):
    def __init__(self,session_email:str):
        super().__init__()
        self.setWindowTitle("Car Rental - Dashboard")
        self.setWindowIcon(QIcon('assets/icon.png'))
        self.resize(1280, 820)
        self.session_email=session_email

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

        # Main content

        self.stacked_widget = QStackedWidget()
        shell_layout.addWidget(self.stacked_widget)

        self.dashboard_container = QWidget()
        self.dashboard_container.setStyleSheet("background-color: transparent;")
        content_layout = QVBoxLayout(self.dashboard_container)
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

        self.stats_row = QHBoxLayout()
        self.stats_row.setSpacing(12)
        self.stat_chip_cars = self.make_stat_chip("0 Cars")
        self.stat_chip_available = self.make_stat_chip("Available")
        self.stats_row.addWidget(self.stat_chip_cars)
        self.stats_row.addWidget(self.stat_chip_available)
        self.stats_row.addStretch()

        banner_layout.addLayout(banner_top)
        banner_layout.addStretch()
        banner_layout.addWidget(title)
        banner_layout.addWidget(subtitle)
        banner_layout.addSpacing(8)
        banner_layout.addLayout(self.stats_row)

        content_layout.addWidget(banner)

        #Logout Button
        btn_logout = QPushButton(" Logout")
        btn_logout.setCursor(Qt.PointingHandCursor)
        btn_logout.setMinimumHeight(46)
        btn_logout.clicked.connect(self.logout)


        # Date Picker Panel (shown before car grid)

        self.date_picker_panel = QFrame()
        self.date_picker_panel.setStyleSheet("""
            QFrame {
                background-color: #f5f7fb;
            }
        """)
        date_picker_outer = QVBoxLayout(self.date_picker_panel)
        date_picker_outer.setContentsMargins(0, 0, 0, 0)
        date_picker_outer.setAlignment(Qt.AlignCenter)

        # Dark card in the center
        date_card = QFrame()
        date_card.setFixedWidth(460)
        date_card.setStyleSheet("""
            QFrame {
                background-color: #1a2b27;
                border-radius: 16px;
            }
            QLabel {
                color: white;
                background: transparent;
            }
        """)
        date_card_layout = QVBoxLayout(date_card)
        date_card_layout.setContentsMargins(32, 28, 32, 28)
        date_card_layout.setSpacing(16)

        date_card_title = QLabel("Select Dates")
        date_card_title.setStyleSheet("font-size: 20px; font-weight: 800; color: white; background: transparent;")
        date_card_title.setAlignment(Qt.AlignCenter)

        date_card_subtitle = QLabel("to check for available cars")
        date_card_subtitle.setStyleSheet("font-size: 13px; color: rgba(255,255,255,0.7); background: transparent;")
        date_card_subtitle.setAlignment(Qt.AlignCenter)

        # Pickup / Drop-off row
        dates_row = QHBoxLayout()
        dates_row.setSpacing(18)

        pickup_wrap = QVBoxLayout()
        pickup_label = QLabel("Pickup:")
        pickup_label.setStyleSheet("font-size: 13px; font-weight: 600; color: rgba(255,255,255,0.85); background: transparent;")

        # Pickup Wrap

        pickup_wrap = QVBoxLayout()
        pickup_label = QLabel("Pickup:")
        pickup_label.setStyleSheet("font-size: 13px; font-weight: 600; color: rgba(255,255,255,0.85); background: transparent;")
        
        self.pickup_input = QDateEdit()
        self.pickup_input.setCalendarPopup(True)
        self.pickup_input.setDate(QDate.currentDate()) 
        self.pickup_input.setDisplayFormat("yyyy-MM-dd")
        self.pickup_input.setMinimumHeight(44)
        self.pickup_input.setStyleSheet("""
            QDateEdit {
                background-color: white;
                color: #1a2b27;
                border: none;
                border-radius: 10px;
                padding: 10px 14px;
                font-size: 14px;
                font-weight: 600;
            }
            QDateEdit:focus {
                border: 2px solid #6a9a83;
            }
            QDateEdit::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 30px;
                border-left: none;
            }
            QDateEdit::down-arrow {
                image: url("assets/calendar.png");
                width: 30px;
                height: 30px;
            }
        """)
        pickup_wrap.addWidget(pickup_label)
        pickup_wrap.addWidget(self.pickup_input)


        # Drop-off Wrap

        dropoff_wrap = QVBoxLayout()
        dropoff_label = QLabel("Drop-off:")
        dropoff_label.setStyleSheet("font-size: 13px; font-weight: 600; color: rgba(255,255,255,0.85); background: transparent;")
        
        self.dropoff_input = QDateEdit()
        self.dropoff_input.setCalendarPopup(True) 
        self.dropoff_input.setDate(QDate.currentDate().addDays(1)) 
        self.dropoff_input.setDisplayFormat("yyyy-MM-dd")
        self.dropoff_input.setMinimumHeight(44)
        self.dropoff_input.setStyleSheet("""
            QDateEdit {
                background-color: white;
                color: #1a2b27;
                border: none;
                border-radius: 10px;
                padding: 10px 14px;
                font-size: 14px;
                font-weight: 600;
            }
            QDateEdit:focus {
                border: 2px solid #6a9a83;
            }
            QDateEdit::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 30px;
                border-left: none;
            }
            QDateEdit::down-arrow {
                image: url("assets/calendar.png");
                width: 30px;
                height: 30px;
            }
        """)
        dropoff_wrap.addWidget(dropoff_label)
        dropoff_wrap.addWidget(self.dropoff_input)

        dates_row.addLayout(pickup_wrap)
        dates_row.addLayout(dropoff_wrap)

        self.date_error_label = QLabel("")
        self.date_error_label.setStyleSheet("color: #ff7777; font-size: 12px; background: transparent;")
        self.date_error_label.setAlignment(Qt.AlignCenter)

        btn_search_dates = QPushButton("Search Available Cars")
        btn_search_dates.setCursor(Qt.PointingHandCursor)
        btn_search_dates.setMinimumHeight(46)
        btn_search_dates.clicked.connect(self.on_search_dates)
        btn_search_dates.setStyleSheet("""
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
            }
        """)

        date_card_layout.addWidget(date_card_title)
        date_card_layout.addWidget(date_card_subtitle)
        date_card_layout.addSpacing(8)
        date_card_layout.addLayout(dates_row)
        date_card_layout.addWidget(self.date_error_label)
        date_card_layout.addWidget(btn_search_dates)

        date_picker_outer.addStretch()
        date_picker_outer.addWidget(date_card, alignment=Qt.AlignCenter)
        date_picker_outer.addStretch()

        content_layout.addWidget(self.date_picker_panel)



        # Cars panel (toolbar + grid) 

        self.cars_panel = QWidget()
        self.cars_panel.setStyleSheet("background-color: transparent;")
        cars_panel_layout = QVBoxLayout(self.cars_panel)
        cars_panel_layout.setContentsMargins(0, 0, 0, 0)
        cars_panel_layout.setSpacing(0)
        self.cars_panel.hide()

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
        btn_filter.setEnabled(True) 
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

        btn_change_dates = QPushButton("✏ Change Dates")
        btn_change_dates.setCursor(Qt.PointingHandCursor)
        btn_change_dates.setMinimumHeight(38)
        btn_change_dates.clicked.connect(self.go_back_to_date_picker)
        btn_change_dates.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: #334155;
                border: 1px solid #d5deeb;
                border-radius: 10px;
                padding: 8px 14px;
                font-size: 13px;
                font-weight: 700;
            }
            QPushButton:hover {
                background-color: #f0f4f3;
            }
        """)
        toolbar_layout.addWidget(btn_change_dates)

        cars_panel_layout.addWidget(toolbar)

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

        scroll.setWidget(scroll_content)
        cars_panel_layout.addWidget(scroll)

        content_layout.addWidget(self.cars_panel)
        self.res_page = ReservationsWindow(self.session_email)
        self.settings_page = self.create_settings_page()

        self.stacked_widget.addWidget(self.dashboard_container) # Index 0
        self.stacked_widget.addWidget(self.res_page)            # Index 1
        self.stacked_widget.addWidget(self.settings_page)       # Index 2      


    

    def update_grid(self, cars_list):
        for i in reversed(range(self.grid.count())):
            widget = self.grid.itemAt(i).widget()
            if widget:
                widget.deleteLater()
                
        if not cars_list:            
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

        # AVAILABILITY
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
            available_count = sum(1 for car in sorted_cars if car["state"] == "Available")
            self.right_info_label.setText(f"Showing <b>{available_count}</b> available vehicles")
        else:
            print(f"functions.py did not return a list: {sorted_cars}")
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
                    # No filter values — just re-fetch available cars for the selected dates
                    filtered = functions.GetAvailableCarsByDates(start, end) if start and end else functions.GetCars()
                else:
                    filtered = functions.FilterCars(price, year, cc, hp, start_date=start, end_date=end)
                
                if isinstance(filtered, list):
                    self.update_grid(filtered)
                    available_count = sum(1 for car in filtered if car["state"] == "Available")
                    self.right_info_label.setText(f"Showing <b>{available_count}</b> available vehicles")
                else:
                    print(f"functions.py did not return a list: {filtered}")
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
        self.stacked_widget.setCurrentIndex(0)
        self.refresh_dashboard()
    




    def on_search_dates(self):
        """Validate dates, fetch available cars, show the grid."""
        start_str = self.pickup_input.date().toString("yyyy-MM-dd")
        end_str = self.dropoff_input.date().toString("yyyy-MM-dd")

        # Validate format
        try:
            start_dt = datetime.strptime(start_str, "%Y-%m-%d")
            end_dt = datetime.strptime(end_str, "%Y-%m-%d")
        except ValueError:
            self.date_error_label.setText("Please enter dates in YYYY-MM-DD format.")
            return

        if end_dt <= start_dt:
            self.date_error_label.setText("Drop-off date must be after pickup date.")
            return

        if start_dt < datetime.now().replace(hour=0, minute=0, second=0, microsecond=0):
            self.date_error_label.setText("Pickup date cannot be in the past.")
            return

        self.date_error_label.setText("")

        self.selected_start_date = start_str + " 00:00"
        self.selected_end_date = end_str + " 00:00"

        # Fetch cars available for these dates
        available_cars = functions.GetAvailableCarsByDates(start_str, end_str)
        if available_cars is None:
            available_cars = []
        self.cars = available_cars

        # Update banner stats
        self.stat_chip_cars.setText(f"{len(self.cars)} Cars")

        # Show the cars panel, hide the date picker
        self.date_picker_panel.hide()
        self.cars_panel.show()

        # Update the grid and the info label
        self.update_grid(self.cars)
        available_count = sum(1 for car in self.cars if car["state"] == "Available")
        self.right_info_label.setText(f"Showing <b>{available_count}</b> vehicles")

    def go_back_to_date_picker(self):
        """Go back to the date picker panel."""
        self.cars_panel.hide()
        self.date_picker_panel.show()
        self.selected_start_date = None
        self.selected_end_date = None

    def refresh_dashboard(self):
        # When navigating back to Dashboard tab, show date picker again
        self.cars_panel.hide()
        self.date_picker_panel.show()
        self.selected_start_date = None
        self.selected_end_date = None
        self.cars = []
        self.stat_chip_cars.setText("0 Cars")
    
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
        # If dates are already selected from the dashboard search, skip the date picker
        if self.selected_start_date and self.selected_end_date:
            start_str = self.selected_start_date
            end_str = self.selected_end_date
        else:
            date_dialog = DatePickerDialog(self)
            if date_dialog.exec() == QDialog.Accepted:
                start_str, end_str = date_dialog.get_dates()
            else:
                return

        st = datetime.strptime(start_str, "%Y-%m-%d %H:%M")
        et = datetime.strptime(end_str, "%Y-%m-%d %H:%M")
        days = (et - st).days
        if days <= 0: days = 1 
        
        total_price = days * car['price']
        from pay import PaymentWindow
        print("Car plate from main: ", car['license_plate'])
        self.payment_screen = PaymentWindow(self.session_email, start_str, end_str,car)
        self.payment_screen.show()
        self.close()

    def show_car_details(self, car):
        dialog = CarDetailsDialog(car, self)
        dialog.exec()

    def create_car_card(self, car):
        card = QFrame()
        card.setFixedWidth(320)
        card.setMinimumHeight(460)
        card.setMaximumHeight(460)
        
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
        image_box.setFixedHeight(220) 
        
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
        
        filename = f"{car['image_path']}.png"

        full_path = os.path.join(BASE_DIR, "imgs", filename)

        print(full_path)
        pixmap = QPixmap(full_path)
    
        if not pixmap.isNull():
            scaled_pixmap = pixmap.scaled(
                280, 200, 
                Qt.KeepAspectRatioByExpanding, 
                Qt.SmoothTransformation
            )
            
            #car_image.setFixedSize(280, 210) 
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
        btn_details.clicked.connect(lambda checked=False, c=car: self.show_car_details(c))
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
        btn_rent.clicked.connect(lambda checked=False, c=car: self.handle_rent(c))

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