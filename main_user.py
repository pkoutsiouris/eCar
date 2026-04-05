import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QScrollArea, QGridLayout, QFrame, QButtonGroup
)
from PySide6.QtCore import Qt
from back_end import functions
from PySide6.QtGui import QPixmap

class MainDashboard(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Car Rental - Dashboard")
        self.resize(1280, 820)
        
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
                    stop:0 #0d4fa3,
                    stop:0.45 #1b6fd8,
                    stop:1 #4fa3ff
                );
            }
        """)

        app_shell = QFrame()
        app_shell.setObjectName("AppShell")
        app_shell.setStyleSheet("""
            QFrame#AppShell {
                background-color: #f5f7fb;
                border-radius: 18px;
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
                background-color: #101826;
                border-top-left-radius: 18px;
                border-bottom-left-radius: 18px;
            }
            QLabel {
                background: transparent;
            }
            QPushButton {
                text-align: left;
                padding: 14px 20px;
                border: none;
                font-size: 14px;
                font-weight: 600;
                color: #b6c0cf;
                background: transparent;
                border-left: 3px solid transparent;
            }
            QPushButton:hover {
                background-color: #182233;
                color: white;
            }
            QPushButton:checked {
                background-color: #253247;
                color: white;
                border-left: 3px solid #4ea1ff;
            }   
        """)

        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(0, 22, 0, 18)
        sidebar_layout.setSpacing(6)

        logo_wrap = QWidget()
        logo_layout = QVBoxLayout(logo_wrap)
        logo_layout.setContentsMargins(18, 0, 18, 10)
        logo_layout.setSpacing(2)

        logo = QLabel("CarRental")
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
        btn_reservations = self.make_sidebar_button("Reservations")
        btn_settings = self.make_sidebar_button("Settings")

        self.nav_group.addButton(btn_dashboard)
        self.nav_group.addButton(btn_reservations)
        self.nav_group.addButton(btn_settings)

        sidebar_layout.addWidget(btn_dashboard)
        sidebar_layout.addWidget(btn_reservations)
        sidebar_layout.addWidget(btn_settings)
        sidebar_layout.addStretch()

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

        # Banner
        banner = QFrame()
        banner.setFixedHeight(190)
        banner.setStyleSheet("""
            QFrame {
                border-top-right-radius: 18px;
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:1,
                    stop:0 #6ca8ff,
                    stop:0.45 #3e84e8,
                    stop:1 #1f5fbe
                );
            }
        """)

        banner_layout = QVBoxLayout(banner)
        banner_layout.setContentsMargins(32, 24, 32, 24)
        banner_layout.setSpacing(10)

        banner_top = QHBoxLayout()
        banner_top.setSpacing(10)

        section_badge = QLabel("TRAVEL / RENTALS")
        section_badge.setStyleSheet("""
            background-color: rgba(255,255,255,0.16);
            color: white;
            padding: 6px 12px;
            border-radius: 12px;
            font-size: 11px;
            font-weight: 700;
        """)

        banner_top.addWidget(section_badge)
        banner_top.addStretch()

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

        # Toolbar
        toolbar = QWidget()
        toolbar.setFixedHeight(72)
        toolbar.setStyleSheet("""
            QWidget {
                background-color: #ffffff;
                border-bottom: 1px solid #e8edf5;
            }
        """)

        toolbar_layout = QHBoxLayout(toolbar)
        toolbar_layout.setContentsMargins(28, 0, 28, 0)
        toolbar_layout.setSpacing(12)

        left_info = QLabel("Sort by: <b>Recommended</b>")
        left_info.setStyleSheet("""
            color: #2b3547;
            font-size: 14px;
            background: transparent;
        """)

        right_info = QLabel(f"Showing <b>{len(self.cars)}</b> vehicles")
        right_info.setStyleSheet("""
            color: #556070;
            font-size: 14px;
            background: transparent;
        """)

        btn_filter = QPushButton("Filter")
        btn_filter.setEnabled(False)  # frontend only
        btn_filter.setStyleSheet("""
            QPushButton {
                background-color: #eef1f5;
                color: #8a94a6;
                border: 1px solid #dde3ec;
                border-radius: 10px;
                padding: 9px 16px;
                font-size: 13px;
                font-weight: 700;
            }
        """)

    

        toolbar_layout.addWidget(left_info)
        toolbar_layout.addStretch()
        toolbar_layout.addWidget(right_info)
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

        grid = QGridLayout(scroll_content)
        grid.setContentsMargins(28, 24, 28, 28)
        grid.setHorizontalSpacing(22)
        grid.setVerticalSpacing(22)

        row = 0
        col = 0
        for car in self.cars:
            card = self.create_car_card(car)
            grid.addWidget(card, row, col)

            col += 1
            if col > 2:
                col = 0
                row += 1

        scroll.setWidget(scroll_content)
        content_layout.addWidget(scroll)

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
            background-color: #f3f6fb;
            color: #49576a;
            border: 1px solid #e5ebf4;
            padding: 5px 9px;
            border-radius: 9px;
            font-size: 11px;
            font-weight: 700;
        """)
        return chip

    def create_car_card(self, car):
        card = QFrame()
        
        # ΓΙΑΤΙ ΤΟ ΑΛΛΑΞΑΜΕ 1/3 (Συνολικό Ύψος Κάρτας):
        # Ήταν 305. Το κάναμε 360 για να δώσουμε χώρο στη νέα μεγαλύτερη φωτογραφία 
        # και να μην πέφτουν τα γράμματα το ένα πάνω στο άλλο (overflow).
        card.setMinimumHeight(360)
        card.setMaximumHeight(360)
        
        card.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 1px solid #e5ebf4;
                border-radius: 16px;
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
        
        # ΓΙΑΤΙ ΤΟ ΑΛΛΑΞΑΜΕ 2/3 (Ύψος Γκρι Κουτιού): 
        # Ήταν 92, το κάναμε 140. Αφού μεγαλώσαμε την κάρτα στο προηγούμενο βήμα,
        # τώρα δίνουμε αυτόν τον έξτρα χώρο στο γκρι κουτί για να γίνει "καμβάς" για τη φωτό.
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

        img_path = car["image_path"].lstrip("/")
        pixmap = QPixmap(img_path)
    
        if not pixmap.isNull():
            
            # ΓΙΑΤΙ ΤΟ ΑΛΛΑΞΑΜΕ 3/3 (Aspect Ratio & Cropping):
            # Ήταν KeepAspectRatio (που προσπαθούσε να χωρέσει όλη την εικόνα μικραίνοντάς την).
            # Το κάναμε KeepAspectRatioByExpanding (μεγαλώνει την εικόνα για να γεμίσει ΠΛΗΡΩΣ το νέο 140άρι κουτί, 
            # διατηρώντας όμως τις σωστές αναλογίες του αμαξιού για να μη βγει παραμορφωμένο).
            scaled_pixmap = pixmap.scaled(
                340, 140, 
                Qt.KeepAspectRatioByExpanding, 
                Qt.SmoothTransformation
            )
            
            # ...και εδώ βάζουμε το car_image να κόψει "με το μαχαίρι" (Crop) 
            # ό,τι περισσεύει από τα δεξιά/αριστερά, για να μην πέσει η εικόνα πάνω στα κουμπιά.
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
        bottom_row.setSpacing(15) # Βάλαμε λίγο παραπάνω κενό

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

        # ΓΙΑΤΙ ΤΟ ΠΡΟΣΘΕΣΑΜΕ: Φτιάχνουμε το ταμπελάκι της τιμής 
        # Τραβάει το car["price"] και του κολλάει το € και το / day
        price_label = QLabel(f"€{car['price']} <span style='color: #6b7788; font-size: 12px; font-weight: 500;'>/ day</span>")
        price_label.setStyleSheet("""
            color: #1d2736;
            font-size: 18px;
            font-weight: 800;
            background: transparent;
        """)

        bottom_row.addWidget(btn_details)
        bottom_row.addStretch()
        
        # ΠΡΟΣΘΗΚΗ: Βάζουμε την τιμή δίπλα στο κουμπί Select!
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
    window = MainDashboard()
    window.show()
    sys.exit(app.exec())