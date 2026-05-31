import mysql.connector
import bcrypt
import classes
import functions

def get_user_by_email(email):

    try:
        conn = mysql.connector.connect(
            host="localhost", 
            user="root",
            password="", 
            database="eCar_db"
        )
        cursor = conn.cursor(dictionary=True)
        

        query = "SELECT user_id, email, user_password, user_role FROM users WHERE email = %s"
        cursor.execute(query, (email,))
        
        user = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        return user
        
    except mysql.connector.Error as err:
        print(f"Error in sql base connection: {err}")
        return None
    
def is_valid_email(email):
    email = email.strip().lower()
    allowed_domains = ["@gmail.com", "@yahoo.com", "@hotmail.com", "@outlook.com"]
    
    if "@" not in email or email.startswith("@"):
        return False
        
    for domain in allowed_domains:
        if email.endswith(domain):
            return True
    return False

def authenticate_user(email, password):

    email = email.strip()
    password = password.strip()

    if not email or not password:
        return False, "Type email and password.", None


    if not is_valid_email(email):
        return False, "Error, type correct email form (@gmail.com , etc).", None

    user = get_user_by_email(email)

    if user is None:
        return False, "Email not found.", None

    try:
        if bcrypt.checkpw(password.encode('utf-8'), user['user_password'].encode('utf-8')):
            return True, "Login succsess", user['user_role']
        else:
            return False, "Wrong login password.", None
    except ValueError:
        return False, "Error, password is not properly hashed.", None
    
#test_main
if __name__=="__main__":
    print("--Testing--")

    test_email="admin@gmail.com"
    test_password="123"

    success, message, role = authenticate_user(test_email, test_password)

    print(f"Success: {success}")
    print(f"Message: {message}")
    print(f"Role: {role}")