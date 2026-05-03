import sys
import os
import shutil
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QFrame, QTableWidget, QTableWidgetItem, 
    QHeaderView, QStackedWidget, QButtonGroup, QMessageBox, 
    QLineEdit, QFormLayout, QComboBox, QSpinBox, QDoubleSpinBox, QScrollArea, QFileDialog, QGridLayout
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon

# Εισαγωγή από τα αρχεία που αναφέρθηκαν
from back_end import functions, classes

class DealerWindow(QMainWindow):
    def __init__(self, session_email: str):
        super().__init__()
        self.session_email = session_email
        self.setWindowTitle("eCar Rental - Dealer Panel")
        self.resize(1280, 850)

        outer = QWidget()
        self.setCentralWidget(outer)
        outer_layout = QVBoxLayout(outer)
        outer_layout.setContentsMargins(18, 18, 18, 18)
        outer.setStyleSheet("QWidget { background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #1e293b, stop:1 #ffffff); }")

        app_shell = QFrame()
        app_shell.setObjectName("AppShell")
        app_shell.setStyleSheet("""
            QFrame#AppShell { 
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #1e293b, stop:1 #334155); 
                border-radius: 20px; 
            }
        """)  
        shell_layout = QHBoxLayout(app_shell)
        shell_layout.setContentsMargins(0, 0, 0, 0)
        shell_layout.setSpacing(0)
        outer_layout.addWidget(app_shell)

        # Sidebar[cite: 3]
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
        logo = QLabel("Dealer Portal")
        logo.setStyleSheet("color: white; font-size: 22px; font-weight: 800; padding: 20px;")
        sidebar_layout.addWidget(logo)

        self.nav_group = QButtonGroup(self)
        self.btn_dash = self.make_nav_btn("View Dashboard", True)
        self.btn_create = self.make_nav_btn("Create Car")
        self.btn_res = self.make_nav_btn("View Reservations")
        
        for btn in [self.btn_dash, self.btn_create, self.btn_res]:
            sidebar_layout.addWidget(btn)
        
        sidebar_layout.addStretch()
        shell_layout.addWidget(sidebar)

        # Content Area
        self.pages = QStackedWidget()
        shell_layout.addWidget(self.pages)

        # Σύνδεση Buttons με Σελίδες
        self.btn_dash.clicked.connect(lambda: self.show_dashboard())
        self.btn_create.clicked.connect(lambda: self.pages.setCurrentIndex(1))
        self.btn_res.clicked.connect(lambda: self.show_reservations())

        # Προσθήκη Σελίδων
        self.pages.addWidget(self.create_dashboard_page())  # Index 0
        self.pages.addWidget(self.create_car_page())        # Index 1
        self.pages.addWidget(self.create_res_page())        # Index 2

    def make_nav_btn(self, text, checked=False):
        btn = QPushButton(text)
        btn.setCheckable(True)
        btn.setChecked(checked)
        self.nav_group.addButton(btn)
        return btn

    # --- 1. VIEW DASHBOARD ---
    def create_dashboard_page(self):
        page = QWidget()
        self.dash_layout = QVBoxLayout(page)
        return page

    def show_dashboard(self):
        # Καθαρισμός και ανανέωση με πραγματικά δεδομένα από GetCars()
        for i in reversed(range(self.dash_layout.count())): 
            self.dash_layout.itemAt(i).widget().setParent(None)
        
        cars = functions.GetCars()
        
        table = QTableWidget(len(cars) if cars else 0, 5)
        table.setHorizontalHeaderLabels(["Brand", "Model", "Plate", "Status", "Price/Day"])
        table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        table.setStyleSheet("color: black; background: white;")
        
        if cars:
            for row, car in enumerate(cars):
                table.setItem(row, 0, QTableWidgetItem(car['brand']))
                table.setItem(row, 1, QTableWidgetItem(car['model']))
                table.setItem(row, 2, QTableWidgetItem(car['license_plate']))
                table.setItem(row, 3, QTableWidgetItem(car['state']))
                table.setItem(row, 4, QTableWidgetItem(str(car['price'])))
        
        self.dash_layout.addWidget(table)
        self.pages.setCurrentIndex(0)

    # --- 2. CREATE CAR (Χρήση classes.Car & CreateCar) ---[cite: 1, 4]
    def create_car_page(self):
        page = QScrollArea()
        container = QWidget()
        container.setStyleSheet("background-color: white; color: #1e293b;")
        
        # Κύριο Layout με ελεγχόμενα margins
        main_layout = QVBoxLayout(container)
        main_layout.setContentsMargins(30, 20, 30, 20)
        main_layout.setSpacing(15)

        # Grid Layout για τα πεδία εισαγωγής
        grid = QGridLayout()
        grid.setSpacing(12) # Spacing ανάμεσα στα κουτάκια
        grid.setColumnStretch(1, 1) # Δίνει χώρο στα input fields
        grid.setColumnStretch(3, 1)

        # Στυλ για τα Inputs
        # Καθαρό στυλ χωρίς gradients για τα inputs
        input_style = """
            QWidget#CarContainer {
                background-color: #f1f5f9; /* Ελαφρύ γκρι φόντο για όλη τη σελίδα */
            }
            QLineEdit, QSpinBox, QDoubleSpinBox, QComboBox {
                padding: 8px;
                border: 1px solid #cbd5e1;
                border-radius: 6px;
                background-color: white; /* Σταθερό λευκό χρώμα */
                color: #1e293b;
                selection-background-color: #3b82f6;
            }
            QLineEdit:focus, QSpinBox:focus, QDoubleSpinBox:focus, QComboBox:focus {
                border: 2px solid #3b82f6;
                background-color: #ffffff;
            }
            QLabel {
                font-weight: 700;
                color: #334155;
                background: transparent; /* Σημαντικό για να μην παίρνει το gradient */
            }
        """
        container.setObjectName("CarContainer")
        container.setStyleSheet(input_style)

        # Ορισμός Πεδίων
        self.f_brand = QLineEdit(); self.f_model = QLineEdit()
        self.f_year = QSpinBox(); self.f_year.setRange(2000, 2026); self.f_year.setFixedWidth(100)
        self.f_plate = QLineEdit()
        self.f_seats = QSpinBox(); self.f_seats.setRange(1, 9)
        self.f_doors = QSpinBox(); self.f_doors.setRange(2, 5)
        self.f_cc = QSpinBox(); self.f_cc.setRange(500, 8000)
        self.f_hp = QSpinBox(); self.f_hp.setRange(50, 1500)
        self.f_fuel = QComboBox(); self.f_fuel.addItems(['Gas', 'Diesel', 'Hybrid', 'Electric'])
        self.f_trans = QComboBox(); self.f_trans.addItems(['Manual', 'Auto'])
        self.f_state = QComboBox(); self.f_state.addItems(['Available', 'In_Service', 'Unavailable'])
        self.f_price = QDoubleSpinBox(); self.f_price.setRange(0, 5000); self.f_price.setSuffix(" €")
        self.f_desc = QLineEdit(); self.f_desc.setPlaceholderText("Short vehicle description...")

        # Τοποθέτηση στο Grid (Row, Col)
        # Γραμμή 0
        grid.addWidget(QLabel("Brand:"), 0, 0); grid.addWidget(self.f_brand, 0, 1)
        grid.addWidget(QLabel("Model:"), 0, 2); grid.addWidget(self.f_model, 0, 3)
        
        # Γραμμή 1
        grid.addWidget(QLabel("Year:"), 1, 0); grid.addWidget(self.f_year, 1, 1)
        grid.addWidget(QLabel("License Plate:"), 1, 2); grid.addWidget(self.f_plate, 1, 3)

        # Γραμμή 2
        grid.addWidget(QLabel("Seats:"), 2, 0); grid.addWidget(self.f_seats, 2, 1)
        grid.addWidget(QLabel("Doors:"), 2, 2); grid.addWidget(self.f_doors, 2, 3)

        # Γραμμή 3
        grid.addWidget(QLabel("Engine CC:"), 3, 0); grid.addWidget(self.f_cc, 3, 1)
        grid.addWidget(QLabel("Horsepower:"), 3, 2); grid.addWidget(self.f_hp, 3, 3)

        # Γραμμή 4
        grid.addWidget(QLabel("Fuel Type:"), 4, 0); grid.addWidget(self.f_fuel, 4, 1)
        grid.addWidget(QLabel("Transmission:"), 4, 2); grid.addWidget(self.f_trans, 4, 3)

        # Γραμμή 5
        grid.addWidget(QLabel("Status:"), 5, 0); grid.addWidget(self.f_state, 5, 1)
        grid.addWidget(QLabel("Price / Day:"), 5, 2); grid.addWidget(self.f_price, 5, 3)

        main_layout.addLayout(grid)

        # Description (Full Width)
        main_layout.addWidget(QLabel("Description:"))
        main_layout.addWidget(self.f_desc)

        # Image Selection Section
        img_group = QHBoxLayout()
        self.image_path_display = QLineEdit(); self.image_path_display.setReadOnly(True)
        btn_import_img = QPushButton("Select Photo")
        btn_import_img.setStyleSheet("background: #64748b; color: white; padding: 7px 15px; font-weight: bold;")
        btn_import_img.clicked.connect(self.import_image)
        img_group.addWidget(self.image_path_display)
        img_group.addWidget(btn_import_img)
        main_layout.addLayout(img_group)

        # Submit Button
        main_layout.addSpacing(10)
        btn_submit = QPushButton("Add Vehicle to Fleet")
        btn_submit.setCursor(Qt.PointingHandCursor)
        btn_submit.setStyleSheet("""
            QPushButton {
                background: #3b82f6; color: white; padding: 12px; 
                font-size: 15px; font-weight: bold; border-radius: 6px;
            }
            QPushButton:hover { background: #2563eb; }
        """)
        btn_submit.clicked.connect(self.submit_car)
        main_layout.addWidget(btn_submit)
        
        main_layout.addStretch() # Σπρώχνει τα πάντα προς τα πάνω για να μην "αιωρούνται"

        page.setWidget(container)
        page.setWidgetResizable(True)
        return page
    def import_image(self):
        file_dialog = QFileDialog(self)
        file_path, _ = file_dialog.getOpenFileName(
            self, 
            "Select Car Image", 
            "", 
            "Images (*.png)"
        )
        if file_path:
            self.image_path_display.setText(file_path)
    def submit_car(self):
        selected_img_path = self.image_path_display.text()
        plate_text = self.f_plate.text().strip()

        # Έλεγχος αν έχει συμπληρωθεί η πινακίδα (απαραίτητο για το όνομα της εικόνας)
        if not plate_text:
            QMessageBox.warning(self, "Input Error", "Please enter a License Plate first.")
            return

        final_img_name = f"{plate_text}.png"
        
        # Διαχείριση Φακέλου και Αντιγραφή Εικόνας
        if selected_img_path and os.path.exists(selected_img_path):
            try:
                # Δημιουργία φακέλου imgs αν δεν υπάρχει
                dest_folder = "imgs"
                if not os.path.exists(dest_folder):
                    os.makedirs(dest_folder)
                
                # Ορισμός τελικής διαδρομής: imgs/ΠΙΝΑΚΙΔΑ.png
                dest_path = os.path.join(dest_folder, final_img_name)
                
                # Αντιγραφή του αρχείου στον φάκελο imgs
                shutil.copy2(selected_img_path, dest_path)
            except Exception as e:
                QMessageBox.critical(self, "File Error", f"Could not save image: {str(e)}")
                return
        else:
            # Αν δεν επιλέχθηκε εικόνα, ορίζουμε μια default τιμή ή αφήνουμε κενό
            final_img_name = "default.png"

        # Δημιουργία instance Car με το ΟΝΟΜΑ του αρχείου (όχι όλο το path)
        new_car = classes.Car(
            brand=self.f_brand.text(),
            model=self.f_model.text(),
            prod_year=self.f_year.value(),
            plate=plate_text,
            seats=self.f_seats.value(),
            doors=self.f_doors.value(),
            cc=self.f_cc.value(),
            state=self.f_state.currentText(),
            desc=self.f_desc.text(),
            fuel=self.f_fuel.currentText(),
            trans=self.f_trans.currentText(),
            horsepower=self.f_hp.value(),
            imgPath=final_img_name, # Αποθηκεύουμε μόνο το όνομα (π.χ. ABC-1234.png)
            price=self.f_price.value(),
            availability=True
        )
        
        if functions.CreateCar(new_car): 
            QMessageBox.information(self, "Success", f"Vehicle and image {final_img_name} registered successfully.")
            self.image_path_display.clear() 
            self.show_dashboard()
        else:
            QMessageBox.warning(self, "Database Error", "Could not create car. Plate might exist.")
    # --- 3. VIEW RESERVATIONS ---
    def create_res_page(self):
        page = QWidget()
        self.res_layout = QVBoxLayout(page)
        return page

    def show_reservations(self):
        for i in reversed(range(self.res_layout.count())):
            self.res_layout.itemAt(i).widget().setParent(None)

        # Χρήση της GetUserReservations(email) από το functions.py
        res_data = functions.GetUserReservations(self.session_email)
        
        table = QTableWidget(len(res_data) if res_data else 0, 5)
        table.setHorizontalHeaderLabels(["ID", "Car ID", "Start Date", "End Date", "Total Price"])
        table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        table.setStyleSheet("color: black; background: white;")

        if res_data:
            for row, res in enumerate(res_data):
                table.setItem(row, 0, QTableWidgetItem(str(res['reservation_id'])))
                table.setItem(row, 1, QTableWidgetItem(str(res['car_id'])))
                table.setItem(row, 2, QTableWidgetItem(str(res['start_date'])))
                table.setItem(row, 3, QTableWidgetItem(str(res['end_date'])))
                table.setItem(row, 4, QTableWidgetItem(f"{res['total_price']} €"))

        self.res_layout.addWidget(table)
        self.pages.setCurrentIndex(2)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    # Χρησιμοποιήστε ένα test email για να εκτελεστεί το παράθυρο
    window = DealerWindow("a@gmail.com") 
    window.show()
    sys.exit(app.exec())