import mysql.connector

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
    user = classes.User.get_user_by_email(email)

    if user is None:
        return False, "Ο χρήστης με αυτό το email δεν βρέθηκε.", None

    # 4. Ελέγχουμε τον κωδικό
    if user['user_password'] == password:
        # Όλα πήγαν καλά! Στέλνουμε πίσω True, ένα μήνυμα, και τον ρόλο του.
        return True, "Επιτυχής σύνδεση", user['user_role']
    else:
        return False, "Λάθος κωδικός πρόσβασης.", None