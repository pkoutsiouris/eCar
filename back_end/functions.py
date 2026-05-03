from datetime import datetime
import mysql.connector
#import classes
from back_end import classes
from back_end.session import session
def ConnectDB():
    try:
        # Προσοχή: Εδώ θα βάλετε τα δικά σας στοιχεία της MySQL
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="eCar_db"
        )
        
        cursor = conn.cursor(dictionary=True,buffered=True)
        print("AFTER CURSOR\n")
        return conn,cursor
    except mysql.connector.Error as err:
        print(f"Σφάλμα σύνδεσης με τη βάση: {err}")
        return None
    
def CheckCarExists(car: classes.Car):
    try:
        conn,db = ConnectDB()
        query = "select * from cars where license_plate=%s"
        db.execute(query,(car.plate,))
        res = db.fetchone()
        if res is None:
            return False
        else:
            return True
    except mysql.connector.Error as err:
        print(f"Σφάλμα σύνδεσης με τη βάση (checkcarexists): {err}")
        return None
    finally:
        db.close()
        conn.close()

def GetCars():
    try:
        conn,db = ConnectDB()
        query = "select * from cars;"
        db.execute(query)
        print("after db execute\n")
        car = db.fetchall()
        return car
    except mysql.connector.Error as err:
        print(f"Σφάλμα σύνδεσης με τη βάση from getcars: {err}")
        return None
    finally:
        db.close()
        conn.close()

def CreateCar(car: classes.Car):
    try:
        conn,db = ConnectDB() 
        if CheckCarExists(car):
            print("Car already exists with license plate: " + car.plate)  
            return False
            
           
        query=" INSERT INTO cars (brand, model, " \
        "production_year, license_plate, seats, cc, state, " \
        "car_description, fuel_type, transmission_type, horsepower, " \
        "image_path, price, availability) VALUES (" \
        "%s , %s ,%s ,%s ,%s ,%s ,%s ,%s ,%s ,%s ,%s ,%s,%s,%s)"
        db.execute(query,(car.brand,car.model,car.prod_year,car.plate,car.seats,car.cc,car.state,
                          car.desc,car.fuel,car.trans,car.horsepower,car.plate,car.price,car.availability))
        conn.commit()
        return True
    except mysql.connector.Error as err:
        print(f"Σφάλμα σύνδεσης με τη βάση: {err}")   
        return False
    finally:
        db.close()
        conn.close()

def GetUsers():
    try:
        conn, db = ConnectDB()
        query = "SELECT * FROM users;"
        db.execute(query)
        users = db.fetchall()
        return users
    except mysql.connector.Error as err:
        print(f"Σφάλμα κατά την ανάκτηση χρηστών (GetUsers): {err}")
        return None
    finally:
        db.close()
        conn.close()

def FilterCars(price: float, year: int, cc: int, horses: int):
    try:
        conn, db = ConnectDB()

        query = "SELECT * FROM cars WHERE 1=1"
        params = []

        if price is not None:
            query += " AND price <= %s"
            params.append(price)

        if year is not None:
            query += " AND production_year >= %s"
            params.append(year)

        if cc is not None:
            query += " AND cc >= %s"
            params.append(cc)

        if horses is not None:
            query += " AND horsepower >= %s"
            params.append(horses)

        query += ";"

        db.execute(query, tuple(params))
        cars = db.fetchall()

        return cars

    except mysql.connector.Error as err:
        print(f"FilterCars database error: {err}")
        return []

    finally:
        if 'db' in locals() and db is not None:
            db.close()
        if 'conn' in locals() and conn is not None:
            conn.close()
    

#TODO update/cars

def CheckUserExists(user: classes.User):
    try:
        conn,db = ConnectDB()
        query = "select * from users where email=%s"
        db.execute(query,(user.email,))
        res = db.fetchone()
        if res is None:
            return False
        else:
            return True
    except mysql.connector.Error as err:
        print(f"Σφάλμα σύνδεσης με τη βάση (checkuserexists): {err}")
        return None
    finally:
        db.close()
        conn.close()

def RegisterUser(user: classes.User):
    try:
        conn,db = ConnectDB()
        if CheckUserExists(user):
            print("User already exists with email: " + user.email)  
            return False
        
        query=" INSERT INTO users (username, user_password, " \
        "user_role, first_name, surname, email, phone_number, " \
        "license_number, license_type) VALUES (" \
        "%s , %s ,%s ,%s ,%s ,%s ,%s ,%s,%s)"
        db.execute(query,(user.username,user.password,user.role,user.firstname,user.surname,user.email,user.phone,user.license_no,
                          user.license_type))
        conn.commit()
        return True
    except mysql.connector.Error as err:
        print(f"Σφάλμα σύνδεσης με τη βάση: {err}")   
        return False
    finally:
        db.close()
        conn.close()

def GiveDealerAccess(email: str):
    try:
        conn, db = ConnectDB()
        
        # 1. Ψάχνουμε να δούμε αν υπάρχει ο χρήστης
        check_query = "SELECT user_role FROM users WHERE email = %s"
        db.execute(check_query, (email,))
        user = db.fetchone()
        
        if user is None:
            print(f"Προσοχή: Δεν βρέθηκε χρήστης με το email {email}.")
            return False
            
        if user['user_role'] == 'Dealer':
            print(f"Ενημέρωση: Ο χρήστης {email} είναι ΗΔΗ Dealer! Δεν χρειάζεται αλλαγή.")
            return True
        
        # 2. Εφόσον υπάρχει και ΔΕΝ είναι Dealer, του αλλάζουμε ρόλο!
        update_query = "UPDATE users SET user_role = 'Dealer' WHERE email = %s"
        db.execute(update_query, (email,))
        conn.commit()
        
        print(f"Επιτυχία! Ο χρήστης {email} είναι πλέον Dealer.")
        return True
        
    except mysql.connector.Error as err:
        print(f"Σφάλμα κατά την αλλαγή σε Dealer: {err}")
        return False
    finally:
        if 'db' in locals() and db is not None:
            db.close()
        if 'conn' in locals() and conn is not None:
            conn.close()

def GiveAdminAccess(email: str):
    try:
        conn, db = ConnectDB()
        
        # 1. Ψάχνουμε να δούμε αν υπάρχει ο χρήστης
        check_query = "SELECT user_role FROM users WHERE email = %s"
        db.execute(check_query, (email,))
        user = db.fetchone()
        
        # Αν η βάση επιστρέψει None, ο χρήστης δεν υπάρχει!
        if user is None:
            print(f"Προσοχή: Δεν βρέθηκε χρήστης με το email {email}.")
            return False
            
        # Αν υπάρχει, ελέγχουμε τον τωρινό του ρόλο
        if user['user_role'] == 'Admin':
            print(f"Ενημέρωση: Ο χρήστης {email} είναι ΗΔΗ Admin! Δεν χρειάζεται αλλαγή.")
            return True
        
        # 2. Εφόσον υπάρχει και ΔΕΝ είναι Admin, τον αναβαθμίζουμε!
        update_query = "UPDATE users SET user_role = 'Admin' WHERE email = %s"
        db.execute(update_query, (email,))
        conn.commit()
        
        print(f"Επιτυχία! Ο χρήστης {email} αναβαθμίστηκε σε Admin.")
        return True
        
    except mysql.connector.Error as err:
        print(f"Σφάλμα κατά την αναβάθμιση σε Admin: {err}")
        return False
    finally:
        if 'db' in locals() and db is not None:
            db.close()
        if 'conn' in locals() and conn is not None:
            conn.close()

def DeleteCar(car: classes.Car):
    try:
        conn,db = ConnectDB() 
        if CheckCarExists(car):
            print("Car doesn't exists")  
            return False
           
        query = "delete from cars where car_id=%s"
        db.execute(query,(car.car_id))
        conn.commit()
    except Exception as err:
        print("Σφάλμα κατά τη διαγραφή: {err}")   
        return False
    finally:
        db.close()
        conn.close()

def GetSortedCars(sort_by: str, descending: bool = False):
    try:
        conn, db = ConnectDB()

        valid_columns = {
            "price": "price",
            "year": "production_year",
            "cc": "cc"
        }
        if sort_by not in valid_columns:
            print(f"Προσοχή: Μη έγκυρο κριτήριο ταξινόμησης '{sort_by}'.")
            return None
        
        db_column = valid_columns[sort_by]
        order = "DESC" if descending else "ASC"

        query = f"SELECT * FROM cars ORDER BY {db_column} {order};"
        db.execute(query)

        cars = db.fetchall()
        return cars
    
    except mysql.connector.Error as err:
        print(f"Σφάλμα κατά την ταξινόμηση (GetSortedCars): {err}")
        return None
    finally:
        if 'db' in locals() and db is not None:
            db.close()
        if 'conn' in locals() and conn is not None:
            conn.close()
def GetUserSession(email:str):
    try:
        conn, db = ConnectDB()
        query = "SELECT * FROM users WHERE email=%s"
        db.execute(query,(email, ))
        user = db.fetchone()
        return user
    except mysql.connector.Error as err:
        print(f"Could not find users: {err}")
        return None
    finally:
        db.close()
        conn.close()   

def GetCarByLicense(license:str):
    try:
        conn,db = ConnectDB()
        query = "select * from cars where license_plate=%s"
        db.execute(query,(license, ))
        print("after db execute\n")
        car = db.fetchone()
        return car
    except mysql.connector.Error as err:
        print(f"Error getting car by license plate: {err}")
        return None
    finally:
        db.close()
        conn.close()

def GetCarbyID(ID:str):
    try:
        conn,db = ConnectDB()
        query = "select * from cars where car_id=%s"
        db.execute(query,(ID, ))
        print("afer db execute\n")
        car = db.fetchone()
        return car
    except mysql.connector.Error as err:
        print(f"Error getting car by license plate: {err}")
        return None
    finally:
        db.close()
        conn.close()

def CreateReservation(email:str,start_date, end_date,car_id):
    
    try:
        conn, db = ConnectDB()
        user = GetUserSession(email)
        car=GetCarbyID(car_id)
       # car = GetCarByLicense(car_plate)
        #print("the car id is: "+car['car_id'])
        st = datetime.strptime(start_date, "%Y-%m-%d %H:%M")
        et = datetime.strptime(end_date, "%Y-%m-%d %H:%M")
        """ st_str = st.strftime("%Y-%m-%d %H:%M")
        et_str = et.strftime("%Y-%m-%d %H:%M") """
        duration = (et - st).days
        print("Duration is: ",duration)
        rate= float(car["price"])
        total_price=duration*rate
        print("Total price is: ", total_price)
        print(st)
        print(et)
        print("User id ", user["user_id"])
        reservation_status=True
        query = "INSERT INTO reservations (car_id, user_id, start_date, end_date, total_price, reservation_status) VALUES (%s, %s, %s, %s, %s, %s)"
        db.execute(query,(car_id,user["user_id"],st,et,total_price,reservation_status))
        conn.commit()
        query = "UPDATE cars SET availability=0 , state='Unavailable' WHERE car_id=%s"
        db.execute(query,(car_id,))
        conn.commit()

        return True
    except mysql.connector.Error as err:
        print(f"Could not find users: {err}")
        return None
    finally:
        db.close()
        conn.close()   
def GetUserReservations(email:str):
    try:
        conn,db = ConnectDB()
        user = GetUserSession(email)
        query = "select * from reservations where user_id=%s"
        db.execute(query,(user["user_id"], ))
        print("after db execute\n")
        reservation = db.fetchall()
        return reservation
    except mysql.connector.Error as err:
        print(f"Error getting car by license plate: {err}")
        return None
    finally:
        db.close()
        conn.close()
def UpdateUserRole(email: str, new_role: str):
    try:
        conn, db = ConnectDB()
        query = "UPDATE users SET user_role = %s WHERE email = %s"
        db.execute(query, (new_role, email))
        conn.commit()
        return True
    except mysql.connector.Error as err:
        print(f"Σφάλμα κατά την αλλαγή ρόλου: {err}")
        return False
    finally:
        db.close()
        conn.close()
def DeleteUserByEmail(email: str):
    try:
        conn, db = ConnectDB()
        # Διαγραφή του χρήστη βάσει email
        query = "DELETE FROM users WHERE email = %s"
        db.execute(query, (email,))
        conn.commit()
        
        # Ελέγχουμε αν όντως διαγράφηκε κάποια γραμμή
        if db.rowcount > 0:
            print(f"User {email} deleted successfully from database.")
            return True
        else:
            print(f"User {email} not found.")
            return False
    except mysql.connector.Error as err:
        print(f"Σφάλμα κατά τη διαγραφή χρήστη: {err}")
        return False
    finally:
        db.close()
        conn.close()

def ChangePassword(email: str, old_password: str, new_password: str):
    try:
        if not email:
            return False, "No user session found. Please log in again."
        
        email = email.strip()
        old_password = old_password.strip()
        new_password = new_password.strip()
        
        if not old_password or not new_password:
            return False, "Please fill in all fields."

        conn, db = ConnectDB()

        if conn is None or db is None:
            return False, "Failed to connect with database."
        
        user = GetUserSession(email)

        if user is None:
            return False, "User does not exist."

        if user["user_password"] != old_password:
            return False, "Old password is wrong."

        update_query = "UPDATE users SET user_password = %s WHERE email = %s"
        db.execute(update_query, (new_password, email))
        conn.commit()

        return True, "Password changed successfully."

    except Exception as e:
        print(f"Error during password update: {e}")
        return False, "Error while changing password."

    finally:
        if 'db' in locals() and db is not None:
            db.close()
        if 'conn' in locals() and conn is not None:
            conn.close()


def DeleteReservation(reservation_id: int):
    try:
        conn, db = ConnectDB() 

        # 1. Ελέγχουμε αν υπάρχει η κράτηση
        check_query = "SELECT * FROM reservations WHERE reservation_id = %s"
        db.execute(check_query, (reservation_id,))
        res = db.fetchone()
        
        if res is None:
            print(f"Error: The reservation with ID {reservation_id} not found.")  
            return False
            
        # 2. Προχωράμε στη διαγραφή
        delete_query = "DELETE FROM reservations WHERE reservation_id = %s"
        db.execute(delete_query, (reservation_id,))
        conn.commit()
        print("Reservation car id: ", res['car_id'])
        query = "UPDATE cars SET availability=1 , state='Available' WHERE car_id=%s"
        db.execute(query,(res['car_id'],))
        conn.commit()


        print(f"The reservation with ID {reservation_id} deleted.")
        return True

    except mysql.connector.Error as err:
        print(f"Error: reservation was not deleted {err}")   
        return False
    finally:
        if 'db' in locals() and db is not None:
            db.close()
        if 'conn' in locals() and conn is not None:
            conn.close()

def GetReservedCarsByUser(user_email):
    try:
        conn, db = ConnectDB()
        user = GetUserSession(user_email)
        query = """
        SELECT c.*, r.start_date, r.end_date, r.total_price, r.reservation_status
        FROM cars c
        INNER JOIN reservations r ON c.car_id = r.car_id
        WHERE r.user_id = %s
        """

        db.execute(query, (user['user_id'],))
        cars = db.fetchall()

        return cars

    except mysql.connector.Error as err:
        print(f"Error getting user's reserved cars: {err}")
        return None

    finally:
        db.close()
        conn.close()

def GetReservationByCarID(car_id: int, user_email):
    try:
        conn, db = ConnectDB()
        user_id = user = GetUserSession(user_email)
        query = "SELECT * FROM reservations WHERE car_id = %s AND user_id = %s"
        db.execute(query, (car_id, user_id['user_id']))
        reservation = db.fetchone()
        return reservation
    except mysql.connector.Error as err:
        print(f"Error getting reservation by car and user ID: {err}")
        return None
    finally:
        db.close()
        conn.close()