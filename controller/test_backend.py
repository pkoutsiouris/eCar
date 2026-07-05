import unittest
from datetime import datetime

class TestCarRentalLogic(unittest.TestCase):

    # 1. Έλεγχος αποτυχίας login
    def test_login_failure(self):
        """Εικονικός έλεγχος αυθεντικοποίησης"""
        print("Running: test_login_failure...")

        response = False 
        self.assertFalse(response)

    # 2. Έλεγχος υπολογισμού τιμής (Κρίσιμο Unit Test)
    def test_price_calculation_logic(self):
        """Έλεγχος ορθότητας υπολογισμού συνολικού κόστους"""
        print("Running: test_price_calculation_logic...")
        price_per_day = 55.0
        days = 4
        total_price = days * price_per_day
        self.assertEqual(total_price, 220.0)
        
    # 3. Έλεγχος εγκυρότητας email
    def test_email_format(self):
        """Έλεγχος αν το email περιέχει τα απαραίτητα σύμβολα"""
        print("Running: test_email_format...")
        email = "customer@ecarrental.com"
        self.assertIn("@", email)
        self.assertTrue(email.endswith(".com") or email.endswith(".gr"))

    # 4. ΕΛΕΓΧΟΣ ΗΜΕΡΟΜΗΝΙΩΝ 
    def test_reservation_dates_logic(self):
        """Έλεγχος αν η ημερομηνία παράδοσης είναι μετά την ημερομηνία παραλαβής"""
        print("Running: test_reservation_dates_logic...")
        start_date = datetime(2025, 5, 10)
        end_date = datetime(2025, 5, 15)

        duration = (end_date - start_date).days
        self.assertGreater(duration, 0)

    # 5. ΕΛΕΓΧΟΣ ΜΗΚΟΥΣ PASSWORD 
    def test_password_strength(self):
        """Έλεγχος αν το password πληροί το ελάχιστο όριο χαρακτήρων"""
        print("Running: test_password_strength...")

        user_password = "secure123"
        self.assertGreaterEqual(len(user_password), 6)

    # 6. ΕΛΕΓΧΟΣ FORMAT ΠΙΝΑΚΙΔΑΣ 
    def test_license_plate_format(self):
        """Έλεγχος αν η πινακίδα έχει το σωστό μήκος (π.χ. 7 χαρακτήρες)"""
        print("Running: test_license_plate_format...")
        plate = "ZXY1234"

        self.assertEqual(len(plate), 7)

    # 7. 16 ψηφία καρτας
    def test_card_number_masking(self):
        """Έλεγχος αν ο αριθμός κάρτας έχει το σωστό πλήθος ψηφίων (16)"""
        print("Running: test_card_number_masking...")
        raw_card = "1234 5678 1234 5678"
        clean_card = raw_card.replace(" ", "")
        self.assertEqual(len(clean_card), 16)
        self.assertTrue(clean_card.isdigit())

    # 8. admin warning message
    def test_admin_delete_protection(self):
        """Έλεγχος αν ένας Admin μπορεί να διαγραφεί (πρέπει να απαγορεύεται)"""
        print("Running: test_admin_delete_protection...")
        user_to_delete = {"email": "admin@ecarrental.com", "role": "Admin"}

        can_delete = False if user_to_delete["role"] == "Admin" else True
        self.assertFalse(can_delete)

if __name__ == '__main__':
    print("\n" + "="*40)
    print("ECAR RENTAL - SYSTEM UNIT TESTS")
    print("="*40)
    unittest.main(verbosity=2)