import mysql.connector
from controller import classes
from  controller import functions 


def get_user_by_email(email):
    try:
        conn,cursor = functions.ConnectDB()
        cursor = conn.cursor(dictionary=True)
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
    email = email.strip().lower()
    allowed_domains = ["@gmail.com", "@yahoo.com", "@hotmail.com", "@outlook.com", "@hotmail.com"]
    
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
        return False, "Fill in both your email and password.", None

    if not is_valid_email(email):
        return False, "Email not valid!(try ex. @gmail.com).", None


    user = get_user_by_email(email) 

    if user is None:
        return False, "The user with this email address was not found.", None

    if user['user_password'] == password:
        return True, "Connection Successful!", user['user_role']
    else:
        return False, "Wrong password.", None