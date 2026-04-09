import mysql.connector
import bcrypt
import classes
import functions

def get_user_by_email(email):
    """
    Ψάχνει στη βάση δεδομένων να βρει τον χρήστη με το συγκεκριμένο email.
    Επιστρέφει ένα λεξικό (dict) με τα στοιχεία του ή None αν δεν βρεθεί.
    """
    try:
        # Προσοχή: Εδώ θα βάλετε τα δικά σας στοιχεία της MySQL
        conn = mysql.connector.connect(
            host="localhost", 
            user="root",
            password="", 
            database="eCar_db"
        )
        cursor = conn.cursor(dictionary=True)
        
        # Υποθέτουμε ότι ο πίνακας σας λέγεται 'users' 
        # και έχει στήλες: id, email, password, role
        query = "SELECT user_id, email, user_password, user_role FROM users WHERE email = %s"
        cursor.execute(query, (email,))
        
        user = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        return user
        
    except mysql.connector.Error as err:
        print(f"Σφάλμα σύνδεσης με τη βάση: {err}")
        return None
    
def is_valid_email(email):
    """Ελέγχει αν το email έχει σωστή μορφή (Business Logic)."""
    email = email.strip().lower()
    allowed_domains = ["@gmail.com", "@yahoo.com", "@hotmail.com", "@outlook.com"]
    
    if "@" not in email or email.startswith("@"):
        return False
        
    for domain in allowed_domains:
        if email.endswith(domain):
            return True
    return False

def authenticate_user(email, password):
    """
    Αυτή είναι η συνάρτηση που θα καλέσει ο φίλος σου από το PySide6!
    Επιστρέφει 3 πράγματα: (Επιτυχία/Αποτυχία, Μήνυμα, Ρόλος)
    """
    email = email.strip()
    password = password.strip()

    # 1. Έλεγχος αν είναι κενά
    if not email or not password:
        return False, "Συμπλήρωσε και email και password.", None

    # 2. Έλεγχος μορφής email
    if not is_valid_email(email):
        return False, "Βάλε ένα σωστό email (π.χ. @gmail.com).", None

    # 3. Ψάχνουμε τον χρήστη στη βάση μέσω του Model
    user = get_user_by_email(email)

    if user is None:
        return False, "Ο χρήστης με αυτό το email δεν βρέθηκε.", None

    # 4. Ελέγχουμε τον κωδικό
    try:
        # Το bcrypt συγκρίνει τον κωδικό που έγραψε ο χρήστης με το hash της βάσης
        if bcrypt.checkpw(password.encode('utf-8'), user['user_password'].encode('utf-8')):
            return True, "Επιτυχής σύνδεση", user['user_role']
        else:
            return False, "Λάθος κωδικός πρόσβασης.", None
    except ValueError:
        # Αυτό το βάζουμε για ασφάλεια, αν πάει να ελέγξει παλιούς μη-κρυπτογραφημένους κωδικούς
        return False, "Σφάλμα: Ο κωδικός στη βάση δεν είναι σωστά κρυπτογραφημένος.", None
    
#test_main
if __name__=="__main__":
    print("--Testing--")

    test_email="admin@gmail.com"
    test_password="123"

    success, message, role = authenticate_user(test_email, test_password)

    print(f"Success: {success}")
    print(f"Message: {message}")
    print(f"Role: {role}")