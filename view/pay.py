import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QFrame, QMessageBox, QHBoxLayout)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap, QIcon
from controller import classes
class PaymentWindow(QWidget):
    

    def __init__(self, session_email,start_date, end_date, car):
        super().__init__()
        self.session_email = session_email
        self.car_data = car
        self.start_date = start_date
        self.end_date = end_date
        
        from datetime import datetime
        st = datetime.strptime(start_date, "%Y-%m-%d %H:%M")
        et = datetime.strptime(end_date, "%Y-%m-%d %H:%M")
        days = max((et - st).days, 1)
        self.total_amount = days * self.car_data['price']

        self.setWindowTitle("Car Rental - Secure Payment")
        self.setWindowIcon(QIcon('assets/icon.png'))

        # Background
        self.bg_label = QLabel(self)
        self.bg_label.lower() 
        self.original_pixmap = QPixmap('assets/bg.jpg')

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        container = QWidget()
        container.setStyleSheet("background: transparent;") 
        main_layout.addWidget(container)

        outer_layout = QVBoxLayout(container)
        outer_layout.setAlignment(Qt.AlignCenter)
        
        # Logo & Info
        logo_label = QLabel("eCar Rental")
        logo_label.setStyleSheet("color: white; font-size: 34px; font-weight: bold; background: transparent;")
        outer_layout.addWidget(logo_label, alignment=Qt.AlignCenter)

        # Card
        card = QFrame()
        card.setFixedWidth(400)
        card.setStyleSheet("background-color: rgba(255, 255, 255, 235); border-radius: 20px;")
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(30, 30, 30, 30)

        # Summary Info
        summary = QLabel(f"Total to Pay: <b>€{self.total_amount}</b><br><small>Vehicle: {self.car_data['brand']} {self.car_data['model']}</small>")
        summary.setAlignment(Qt.AlignCenter)
        summary.setStyleSheet("color: #1e293b; font-size: 16px; margin-bottom: 10px;")
        card_layout.addWidget(summary)

        input_style = "QLineEdit { background: white; color: black; border: 1px solid #cbd5e1; border-radius: 8px; padding: 10px; font-size: 14px; }"
        header_style = "color: #64748b; font-size: 11px; font-weight: bold;"

        # Fields
        card_layout.addWidget(QLabel("CARDHOLDER NAME", styleSheet=header_style))
        self.name_input = QLineEdit(placeholderText="Full Name")
        self.name_input.setStyleSheet(input_style)
        card_layout.addWidget(self.name_input)

        card_layout.addWidget(QLabel("CARD NUMBER", styleSheet=header_style))
        self.card_input = QLineEdit()
        self.card_input.setPlaceholderText("0000 0000 0000 0000")
        self.card_input.setMaxLength(19)
        self.card_input.setStyleSheet(input_style)
        self.card_input.textChanged.connect(self.format_card)
        card_layout.addWidget(self.card_input)

        row = QHBoxLayout()
        exp_lt = QVBoxLayout() 
        exp_lt.addWidget(QLabel("EXPIRY", styleSheet=header_style))
        self.exp_input = QLineEdit()
        self.exp_input.setPlaceholderText("MM/YY")
        self.exp_input.setStyleSheet(input_style)
        self.exp_input.textChanged.connect(self.format_expiry)
        exp_lt.addWidget(self.exp_input)
        row.addLayout(exp_lt)

        cvv_lt = QVBoxLayout(); cvv_lt.addWidget(QLabel("CVV", styleSheet=header_style))
        self.cvv_input = QLineEdit(); self.cvv_input.setEchoMode(QLineEdit.Password); self.cvv_input.setMaxLength(3); self.cvv_input.setStyleSheet(input_style)
        cvv_lt.addWidget(self.cvv_input); row.addLayout(cvv_lt)
        card_layout.addLayout(row)

        self.pay_btn = QPushButton(f"CONFIRM PAYMENT (€{self.total_amount})")
        self.pay_btn.setCursor(Qt.PointingHandCursor)
        self.pay_btn.setStyleSheet("QPushButton { background: #1f9d55; color: white; font-weight: bold; padding: 12px; border-radius: 8px; margin-top: 15px; }")
        self.pay_btn.clicked.connect(self.process_payment)
        card_layout.addWidget(self.pay_btn)

        outer_layout.addWidget(card)

        # Cancel Button -ΕΠΙΣΤΡΟΦΗ ΣΤΟ MAIN USER
        self.cancel_btn = QPushButton("Cancel and Go Back")
        self.cancel_btn.setCursor(Qt.PointingHandCursor)
        self.cancel_btn.setStyleSheet("color: white; background: transparent; text-decoration: underline;")
        self.cancel_btn.clicked.connect(self.go_to_main)
        outer_layout.addWidget(self.cancel_btn, alignment=Qt.AlignCenter)

        self.showMaximized()

    def go_to_main(self):
        from main_user import MainDashboard 
        self.main_win = MainDashboard(self.session_email)
        self.main_win.show()
        self.close()

    def process_payment(self):
        if len(self.card_input.text().strip()) < 19 or len(self.cvv_input.text()) < 3:
            QMessageBox.warning(self, "Error", "Invalid card details.")
            return

        from controller import functions
        try:
            print("Car ID: "+ str(self.car_data['car_id']))
            functions.CreateReservation(self.session_email, self.start_date, self.end_date, str(self.car_data['car_id']))
            QMessageBox.information(self, "Success", "Payment Successful! Your car is reserved.")
            self.go_to_main()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Database error: {e}")

    def format_card(self, text):
        digits = ''.join(filter(str.isdigit, text))
        
        digits = digits[:16]
        
        formatted = ' '.join(digits[i:i+4] for i in range(0, len(digits), 4))
        
        self.card_input.blockSignals(True)
        self.card_input.setText(formatted)
        self.card_input.setCursorPosition(len(formatted))
        self.card_input.blockSignals(False)

    def format_expiry(self, text):
        digits = ''.join(filter(str.isdigit, text))
        
        digits = digits[:4]
        
        formatted = digits
        if len(digits) > 2:
            formatted = digits[:2] + '/' + digits[2:]
            
        self.exp_input.blockSignals(True)
        self.exp_input.setText(formatted)
        self.exp_input.setCursorPosition(len(formatted))
        self.exp_input.blockSignals(False)

    def resizeEvent(self, event):
        if not self.original_pixmap.isNull():
            scaled = self.original_pixmap.scaled(self.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
            self.bg_label.setPixmap(scaled)
            self.bg_label.resize(self.size())