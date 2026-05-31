import sys
import os
import shutil
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QFrame, QTableWidget, QTableWidgetItem, 
    QHeaderView, QStackedWidget, QButtonGroup, QMessageBox, 
    QLineEdit, QFormLayout, QComboBox, QSpinBox, QDoubleSpinBox, QScrollArea, QFileDialog, QGridLayout, QDialog, QAbstractItemView
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from back_end import functions, classes

class DealerWindow(QMainWindow):
    def __init__(self, session_email: str):
        super().__init__()
        self.session_email = session_email
        self.setWindowTitle("eCar Rental - Dealer Panel")
        self.setWindowIcon(QIcon('assets/icon.png'))
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

        btn_view = QPushButton("View Listings As User")
        btn_view.setCursor(Qt.PointingHandCursor)
        btn_view.setMinimumHeight(46)
        btn_view.setStyleSheet("""
            QPushButton {
                text-align: left;
                padding: 14px 22px;
                border: none;
                font-size: 14px;
                font-weight: 700;
                color: #94A3B8;
                background: transparent;
                border-left: 4px solid transparent;
            }
            QPushButton:hover {
                background-color: #1E293B;
                color: #ffffff;
            }
        """)
        btn_view.clicked.connect(self.view)
        sidebar_layout.addWidget(btn_view)

        btn_logout = QPushButton("Logout")
        btn_logout.setCursor(Qt.PointingHandCursor)
        btn_logout.setMinimumHeight(46)
        btn_logout.setStyleSheet("""
            QPushButton {
                text-align: left;
                padding: 14px 22px;
                border: none;
                font-size: 14px;
                font-weight: 700;
                color: #f87171;
                background: transparent;
                border-left: 4px solid transparent;
            }
            QPushButton:hover {
                background-color: #3d2424;
                color: #ff4444;
            }
        """)
        btn_logout.clicked.connect(self.logout)
        sidebar_layout.addWidget(btn_logout)
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

        self.show_dashboard()

    def make_nav_btn(self, text, checked=False):
        btn = QPushButton(text)
        btn.setCheckable(True)
        btn.setChecked(checked)
        self.nav_group.addButton(btn)
        return btn

    # --- 1. VIEW DASHBOARD -
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
        table.setEditTriggers(QTableWidget.NoEditTriggers)
        

        if cars:
            for row, car in enumerate(cars):
                table.setItem(row, 0, QTableWidgetItem(car['brand']))
                table.setItem(row, 1, QTableWidgetItem(car['model']))
                table.setItem(row, 2, QTableWidgetItem(car['license_plate']))
                table.setItem(row, 3, QTableWidgetItem(car['state']))
                table.setItem(row, 4, QTableWidgetItem(str(car['price'])))
        
        self.dash_layout.addWidget(table)
        self.pages.setCurrentIndex(0)
    def show_reservations(self):
        # Καθαρισμός layout
        for i in reversed(range(self.res_layout.count())):
            widget = self.res_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)

        # Ανάκτηση δεδομένων (πλέον περιέχουν και το πεδίο 'username')
        res_data = functions.ShowReservations() 
        
        # Ορίζουμε 6 στήλες και αλλάζουμε το User ID σε Customer
        table = QTableWidget(len(res_data) if res_data else 0, 6)
        table.setHorizontalHeaderLabels(["Res ID", "Car ID", "Customer", "Start Date", "End Date", "Total Price"])
        table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        table.setStyleSheet("color: black; background: white;")
        table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        table.setSelectionMode(QAbstractItemView.NoSelection) 
        table.setFocusPolicy(Qt.NoFocus)

        if res_data:
            for row, res in enumerate(res_data):
                table.setItem(row, 0, QTableWidgetItem(str(res['reservation_id'])))
                table.setItem(row, 1, QTableWidgetItem(str(res['car_id'])))
                
                # Εμφάνιση του Username αντί για το ID
                table.setItem(row, 2, QTableWidgetItem(str(res['username'])))
                
                # Format ημερομηνιών
                start_dt = res['start_date'].strftime("%Y-%m-%d %H:%M") if hasattr(res['start_date'], 'strftime') else str(res['start_date'])
                end_dt = res['end_date'].strftime("%Y-%m-%d %H:%M") if hasattr(res['end_date'], 'strftime') else str(res['end_date'])
                
                table.setItem(row, 3, QTableWidgetItem(start_dt))
                table.setItem(row, 4, QTableWidgetItem(end_dt))
                table.setItem(row, 5, QTableWidgetItem(f"{res['total_price']} €"))

        self.res_layout.addWidget(table)
        self.pages.setCurrentIndex(2)
    # 2. CREATE CAR (Χρήση classes.Car & CreateCar)
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

        # Στυλ για τα Input
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
            
            /* --- ΠΡΟΣΘΗΚΗ ΓΙΑ ΤΑ DROP-DOWNS --- */
            QComboBox QAbstractItemView {
                background-color: white;
                color: #1e293b;
                selection-background-color: #3b82f6; /* Μπλε χρώμα όταν περνάς το ποντίκι */
                selection-color: white; /* Λευκά γράμματα στην επιλογή */
                border: 1px solid #cbd5e1;
                border-radius: 4px;
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
        self.f_state = QComboBox(); self.f_state.addItems(['Available', 'In Service', 'Unavailable'])
        self.f_price = QDoubleSpinBox(); self.f_price.setRange(0, 5000); self.f_price.setSuffix(" €")
        self.f_desc = QLineEdit(); self.f_desc.setPlaceholderText("Short vehicle description...")

        # Τοποθέτηση στο Grid
        grid.addWidget(QLabel("Brand:"), 0, 0); grid.addWidget(self.f_brand, 0, 1)
        grid.addWidget(QLabel("Model:"), 0, 2); grid.addWidget(self.f_model, 0, 3)
        
        grid.addWidget(QLabel("Year:"), 1, 0); grid.addWidget(self.f_year, 1, 1)
        grid.addWidget(QLabel("License Plate:"), 1, 2); grid.addWidget(self.f_plate, 1, 3)

        grid.addWidget(QLabel("Seats:"), 2, 0); grid.addWidget(self.f_seats, 2, 1)
        grid.addWidget(QLabel("Doors:"), 2, 2); grid.addWidget(self.f_doors, 2, 3)

        grid.addWidget(QLabel("Engine CC:"), 3, 0); grid.addWidget(self.f_cc, 3, 1)
        grid.addWidget(QLabel("Horsepower:"), 3, 2); grid.addWidget(self.f_hp, 3, 3)

        grid.addWidget(QLabel("Fuel Type:"), 4, 0); grid.addWidget(self.f_fuel, 4, 1)
        grid.addWidget(QLabel("Transmission:"), 4, 2); grid.addWidget(self.f_trans, 4, 3)

        grid.addWidget(QLabel("Status:"), 5, 0); grid.addWidget(self.f_state, 5, 1)
        grid.addWidget(QLabel("Price / Day:"), 5, 2); grid.addWidget(self.f_price, 5, 3)

        main_layout.addLayout(grid)

        # Description
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
        
        main_layout.addStretch()

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

        # Έλεγχος αν έχει συμπληρωθεί η πινακίδα
        if not plate_text:
            QMessageBox.warning(self, "Input Error", "Please enter a License Plate first.")
            return

        final_img_name = f"{plate_text}.png"
        
        # Διαχείριση Φακέλου και Αντιγραφή Εικόνας
        if selected_img_path and os.path.exists(selected_img_path):
            try:
                dest_folder = "imgs"
                if not os.path.exists(dest_folder):
                    os.makedirs(dest_folder)
                
                dest_path = os.path.join(dest_folder, final_img_name)
                
                shutil.copy2(selected_img_path, dest_path)
            except Exception as e:
                QMessageBox.critical(self, "File Error", f"Could not save image: {str(e)}")
                return
        else:
            final_img_name = "default.png"

        # Δημιουργία instance Car
        new_car = classes.Car(
            brand=self.f_brand.text(),
            model=self.f_model.text(),
            prod_year=self.f_year.value(),
            plate=plate_text,
            seats=self.f_seats.value(),
            doors=self.f_doors.value(),
            cc=self.f_cc.value(),
            state=self.f_state.currentText().replace(' ', '_'),
            desc=self.f_desc.text(),
            fuel=self.f_fuel.currentText(),
            trans=self.f_trans.currentText(),
            horsepower=self.f_hp.value(),
            imgPath=final_img_name, 
            price=self.f_price.value(),
            availability=True
        )
        
        if functions.CreateCar(new_car): 
            QMessageBox.information(self, "Success", f"Vehicle and image {final_img_name} registered successfully.")
            self.image_path_display.clear() 
            self.show_dashboard()
        else:
            QMessageBox.warning(self, "Database Error", "Could not create car. Plate might exist.")
    # 3. VIEW RESERVATIONS 
    def create_res_page(self):
        page = QWidget()
        self.res_layout = QVBoxLayout(page)
        return page

    def show_dashboard(self):
        for i in reversed(range(self.dash_layout.count())): 
            widget = self.dash_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)
        
        cars = functions.GetCars()
        
        # Αυξάνουμε τις στήλες σε 6 για να χωρέσει το κουμπί διαγραφής
        table = QTableWidget(len(cars) if cars else 0, 6)
        table.setHorizontalHeaderLabels(["Brand", "Model", "Plate", "Status", "Price/Day", "Actions"])
        table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        table.setStyleSheet("color: black; background: white;")
        table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        table.setSelectionMode(QAbstractItemView.NoSelection) 
        table.setFocusPolicy(Qt.NoFocus)

        if cars:
            for row, car in enumerate(cars):
                table.setItem(row, 0, QTableWidgetItem(car['brand']))
                table.setItem(row, 1, QTableWidgetItem(car['model']))
                table.setItem(row, 2, QTableWidgetItem(car['license_plate']))
                table.setItem(row, 3, QTableWidgetItem(car['state']))
                table.setItem(row, 4, QTableWidgetItem(str(car['price'])))
                
                # Δημιουργία κουμπιού διαγραφής
            
                plate = car['license_plate']
                current_price = car['price']
                current_state = car['state']

                action_widget = QWidget()
                action_layout = QHBoxLayout(action_widget)
                action_layout.setContentsMargins(0, 0, 0, 0)
                action_layout.setSpacing(5)

                btn_edit = QPushButton("Edit")
                btn_edit.setCursor(Qt.PointingHandCursor)
                btn_edit.setStyleSheet("background-color: #3b82f6; color: white; border-radius: 4px; padding: 5px;")
                btn_edit.clicked.connect(lambda checked, p=plate, cp=current_price, cs=current_state: self.edit_car_action(p, cp, cs))

                btn_delete = QPushButton("Delete")
                btn_delete.setCursor(Qt.PointingHandCursor)
                btn_delete.setStyleSheet("background-color: #ef4444; color: white; border-radius: 4px; padding: 5px;")
                btn_delete.clicked.connect(lambda checked, p=plate: self.delete_car_action(p))

                action_layout.addWidget(btn_edit)
                action_layout.addWidget(btn_delete)
                
                table.setCellWidget(row, 5, action_widget)
                
        
        self.dash_layout.addWidget(table)
        self.pages.setCurrentIndex(0)
    
    def edit_car_action(self, plate, current_price, current_state):
        dialog = QDialog(self)
        dialog.setWindowTitle(f"Edit: {plate}")
        dialog.setFixedWidth(360)
        dialog.setStyleSheet("""
            QDialog { background-color: #f8fafc; border-radius: 12px; }
            QLabel { font-weight: bold; color: #334155; font-size: 14px; }
        """)
        
        layout = QVBoxLayout(dialog)
        layout.setSpacing(15)
        layout.setContentsMargins(25, 25, 25, 25)
        
        title = QLabel(f"Vehicle Settings\n{plate}")
        title.setStyleSheet("font-size: 18px; color: #1e293b; margin-bottom: 10px;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        form = QFormLayout()
        form.setSpacing(15)
        
        # Πεδίο Τιμής με προστασία
        price_input = QDoubleSpinBox()
        price_input.setRange(0, 10000)
        price_input.setSingleStep(50.0) 
        
        try:
            clean_price = float(str(current_price).replace('€', '').replace(',', '.').strip())
        except ValueError:
            clean_price = 0.0
            
        price_input.setValue(clean_price)
        price_input.setSuffix(" €")
        price_input.setStyleSheet("""
            QDoubleSpinBox {
                padding: 10px; border: 1px solid #cbd5e1; 
                border-radius: 6px; background-color: white; 
                color: #1e293b; font-size: 14px;
            }
        """)
        
        state_input = QComboBox()
        state_input.addItems(['Available', 'In Service', 'Unavailable'])
        
        display_state = str(current_state).replace('_', ' ')
        state_input.setCurrentText(display_state)
        
        state_input.setStyleSheet("""
            QComboBox {
                padding: 10px; border: 1px solid #cbd5e1; 
                border-radius: 6px; background-color: white; 
                color: #1e293b; font-size: 14px;
            }
            QComboBox QAbstractItemView {
                background-color: white; color: #1e293b;
                selection-background-color: #3b82f6; selection-color: white;
            }
        """)
        
        form.addRow("Price / Day:", price_input)
        form.addRow("State:", state_input)
        layout.addLayout(form)
        
        btn_layout = QHBoxLayout()
        btn_cancel = QPushButton("Cancel")
        btn_cancel.setCursor(Qt.PointingHandCursor)
        btn_cancel.setStyleSheet("""
            QPushButton { background-color: #e2e8f0; color: #475569; padding: 10px; border-radius: 6px; font-weight: bold; }
            QPushButton:hover { background-color: #cbd5e1; }
        """)
        btn_cancel.clicked.connect(dialog.reject)
        
        btn_save = QPushButton("Save")
        btn_save.setCursor(Qt.PointingHandCursor)
        btn_save.setStyleSheet("""
            QPushButton { background-color: #3b82f6; color: white; padding: 10px; border-radius: 6px; font-weight: bold; }
            QPushButton:hover { background-color: #2563eb; }
        """)
        btn_save.clicked.connect(dialog.accept)
        
        btn_layout.addWidget(btn_cancel)
        btn_layout.addWidget(btn_save)
        layout.addLayout(btn_layout)
        
        if dialog.exec():
            new_price = price_input.value()
            new_state = state_input.currentText().replace(' ', '_')
            
            try:
                conn, db = functions.ConnectDB()
                availability = 1 if new_state == "Available" else 0 
                
                query = "UPDATE cars SET price=%s, state=%s, availability=%s WHERE license_plate=%s"
                db.execute(query, (new_price, new_state, availability, plate))
                conn.commit()
                
                QMessageBox.information(self, "Success", f"Car Information Updated!")
                self.show_dashboard()
                
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Info Update Failed!: {e}")
            finally:
                if 'db' in locals() and db is not None: db.close()
                if 'conn' in locals() and conn is not None: conn.close()

    def delete_car_action(self, plate):
        # Παράθυρο επιβεβαίωσης
        confirm = QMessageBox.question(
            self, "Confirm Delete", 
            f"Are you sure you want to delete vehicle with plate: {plate}?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if confirm == QMessageBox.Yes:
            if hasattr(functions, 'DeleteCar'):
                success = functions.DeleteCar(plate)
                if success:
                    QMessageBox.information(self, "Success", "Vehicle deleted successfully.")
                    self.show_dashboard() # Refresh το table
                else:
                    QMessageBox.warning(self, "Error", "Could not delete vehicle. It might be linked to a reservation.")
            else:
                QMessageBox.critical(self, "System Error", "Function 'DeleteCar' not found in back_end.functions")

    def logout(self):
        from login import LoginWindow
        self.login_win = LoginWindow()
        self.login_win.show()
        self.close()
    def view(self):
        from main_dealer import MainDealerWindow
        self.dealer_win = MainDealerWindow(self.session_email)
        self.dealer_win.show()
        self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DealerWindow(None) 
    window.show()
    sys.exit(app.exec())