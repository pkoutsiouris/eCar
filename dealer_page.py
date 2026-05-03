import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QFrame, QTableWidget, QTableWidgetItem, 
    QHeaderView, QStackedWidget, QButtonGroup, QMessageBox, 
    QLineEdit, QFormLayout, QComboBox, QSpinBox, QDoubleSpinBox, QScrollArea, QFileDialog 
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
        main_v_layout = QVBoxLayout(container) # Κύριο κάθετο layout
        form_layout = QFormLayout()
        container.setStyleSheet("color: black; padding: 10px; background: white;")
        main_v_layout.setContentsMargins(10, 10, 10, 10)
        main_v_layout.setSpacing(5)
        
        # Πεδία βάσει του InitDB.sql και του constructor της κλάσης Car[cite: 2, 4]
        self.f_brand = QLineEdit()
        self.f_model = QLineEdit()
        self.f_year = QSpinBox(); self.f_year.setRange(2000, 2026)
        self.f_plate = QLineEdit()
        self.f_seats = QSpinBox(); self.f_seats.setRange(1, 9)
        self.f_doors = QSpinBox(); self.f_doors.setRange(2, 5)
        self.f_cc = QSpinBox(); self.f_cc.setRange(500, 8000)
        self.f_state = QComboBox(); self.f_state.addItems(['Available', 'In_Service', 'Unavailable'])
        self.f_desc = QLineEdit()
        self.f_fuel = QComboBox(); self.f_fuel.addItems(['Gas', 'Diesel', 'Hybrid', 'Electric'])
        self.f_trans = QComboBox(); self.f_trans.addItems(['Manual', 'Auto'])
        self.f_hp = QSpinBox(); self.f_hp.setRange(50, 1500)
        self.f_price = QDoubleSpinBox(); self.f_price.setRange(0, 5000)
        self.image_path_display = QLineEdit()
        self.image_path_display.setReadOnly(True)
        self.image_path_display.setPlaceholderText("No image selected")
        
        btn_import_img = QPushButton("Select Car Photo")
        btn_import_img.setStyleSheet("background: #64748b; color: white; padding: 5px;")
        btn_import_img.clicked.connect(self.import_image)
        
        img_layout = QHBoxLayout()
        img_layout.addWidget(self.image_path_display)
        img_layout.addWidget(btn_import_img)

        layout.addRow("Brand:", self.f_brand)
        layout.addRow("Model:", self.f_model)
        layout.addRow("Year:", self.f_year)
        layout.addRow("License Plate:", self.f_plate)
        layout.addRow("Seats:", self.f_seats)
        layout.addRow("Doors:", self.f_doors)
        layout.addRow("CC:", self.f_cc)
        layout.addRow("State:", self.f_state)
        layout.addRow("Description:", self.f_desc)
        layout.addRow("Fuel Type:", self.f_fuel)
        layout.addRow("Transmission:", self.f_trans)
        layout.addRow("Horsepower:", self.f_hp)
        layout.addRow("Price per Day:", self.f_price)
        layout.addRow("Car Image:", img_layout)

        btn_submit = QPushButton("Add Vehicle to Database")
        btn_submit.setStyleSheet("background: #3b82f6; color: white; padding: 12px; font-weight: bold;")
        btn_submit.clicked.connect(self.submit_car)
        layout.addRow(btn_submit)

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
        selected_img = self.image_path_display.text()
        final_img_path = selected_img if selected_img != "" else self.f_plate.text()
        # Δημιουργία instance Car από τα inputs
        new_car = classes.Car(
            brand=self.f_brand.text(),
            model=self.f_model.text(),
            prod_year=self.f_year.value(),
            plate=self.f_plate.text(),
            seats=self.f_seats.value(),
            doors=self.f_doors.value(),
            cc=self.f_cc.value(),
            state=self.f_state.currentText(),
            desc=self.f_desc.text(),
            fuel=self.f_fuel.currentText(),
            trans=self.f_trans.currentText(),
            horsepower=self.f_hp.value(),
            imgPath=self.f_plate.text(), # Χρησιμοποιείται η πινακίδα ως path
            price=self.f_price.value(),
            availability=True
        )
        
        if functions.CreateCar(new_car): 
            QMessageBox.information(self, "Success", "Vehicle registered successfully.")
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