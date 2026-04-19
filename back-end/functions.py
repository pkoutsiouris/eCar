from datetime import datetime
import mysql.connector
import bcrypt
import classes

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
        print("afer db execute\n")
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
                          car.desc,car.fuel,car.trans,car.horsepower,car.imgPath,car.price,car.availability))
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

def FilterCars(price: float, year: int, cc: int , horses: int):
    try:
        conn,db=ConnectDB()

        query="select * from cars"

        conditions = []
        values = []

        # Μαζεύουμε όσα φίλτρα έδωσε ο χρήστης
        if price is not None:
            conditions.append("price = %s")
            values.append(price)
        if year is not None:
            conditions.append("production_year = %s")
            values.append(year)
        if cc is not None:
            conditions.append("cc = %s")
            values.append(cc)
        if horses is not None:
            conditions.append("horsepower = %s")
            values.append(horses)

        # Αν υπάρχει έστω και ένα φίλτρο, τα ενώνουμε αυτόματα με " AND "
        if conditions:
            query += " WHERE " + " AND ".join(conditions)
            
        query += ";"
        
        # Η execute αναλαμβάνει να βάλει τις τιμές με ασφάλεια στη θέση των %s
        db.execute(query, tuple(values))
        cars = db.fetchall()
        return cars

    except mysql.connector.Error as err:
        print(f"Σφάλμα σύνδεσης με τη βάση: {err}")   
        return False
    finally:
        if 'db' in locals() and db is not None:
            db.close()
        if 'conn' in locals() and conn is not None:
            conn.close()

def ChangeCarDescr(car : classes.Car, new_desc: str):
    try:
        conn,db = ConnectDB()

        if conn is None or db is None:
            print("Failed to connect with database.")
            return
        
        if not CheckCarExists(car):
            print("Car doesn't exist")  
            return False
            
        query="update cars set car_description=%s where license_plate=%s"
        db.execute(query,(new_desc, car.plate))
        conn.commit()
        print("Επιτυχία")
        return True
    
    except Exception as e:
        print(f"Error during update: {e}")   
        return False
    
    finally:
        db.close()
        conn.close()

def ChangeCarPrice(car : classes.Car, new_price: float):
    try:
        conn,db = ConnectDB()

        if conn is None or db is None:
            print("Failed to connect with database.")
            return
        
        if not CheckCarExists(car):
            print("Car doesn't exist")  
            return False
            
        query="update cars set price=%s where license_plate=%s"
        db.execute(query,(new_price, car.plate))
        conn.commit()
        print("Επιτυχία")
        return True
    
    except Exception as e:
        print(f"Error during update: {e}")   
        return False
    
    finally:
        db.close()
        conn.close()

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
        if 'db' in locals() and db is not None:
            db.close()
        if 'conn' in locals() and conn is not None:
            conn.close()

def RegisterUser(user: classes.User):
    try:
        conn,db = ConnectDB()
        if CheckUserExists(user):
            print("User already exists with email: " + user.email)  
            return False
        
        hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        query=" INSERT INTO users (username, user_password, " \
        "user_role, first_name, surname, email, phone_number, " \
        "license_number, license_type) VALUES (" \
        "%s , %s ,%s ,%s ,%s ,%s ,%s ,%s,%s)"
        db.execute(query,(user.username,hashed_password,user.role,user.firstname,user.surname,user.email,user.phone,user.license_no,
                          user.license_type))
        conn.commit()
        return True
    except mysql.connector.Error as err:
        print(f"Σφάλμα σύνδεσης με τη βάση: {err}")   
        return False
    finally:
        if 'db' in locals() and db is not None:
            db.close()
        if 'conn' in locals() and conn is not None:
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

        if not CheckCarExists(car):
            print("Car doesn't exists")  
            return False
           
        query = "DELETE FROM cars WHERE license_plate=%s"
        # ΔΙΟΡΘΩΣΗ 1 & 2: Μπήκε το car.plate και το κόμμα (,)
        db.execute(query, (car.plate,))
        conn.commit()

        print(f"Επιτυχία: Το αυτοκίνητο {car.plate} διαγράφηκε.")
        return True

    except Exception as err:
        # ΔΙΟΡΘΩΣΗ 3: Μπήκε το f-string
        print(f"Σφάλμα κατά τη διαγραφή: {err}")   
        return False
    finally:
        if 'db' in locals() and db is not None:
            db.close()
        if 'conn' in locals() and conn is not None:
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
        print("afer db execute\n")
        car = db.fetchone()
        return car
    except mysql.connector.Error as err:
        print(f"Error getting car by license plate: {err}")
        return None
    finally:
        db.close()
        conn.close()


def CreateReservation(email:str,start_date: str, end_date:str, car_id:int):
    user=GetUserSession(email)
    print("From functions: ",user["user_id"])
    try:

        conn, db = ConnectDB()
        user = GetUserSession(email)
        st = datetime.strptime(start_date, "%Y-%m-%d %H:%M")
        et = datetime.strptime(end_date, "%Y-%m-%d %H:%M")
        """ st_str = st.strftime("%Y-%m-%d %H:%M")
        et_str = et.strftime("%Y-%m-%d %H:%M") """
        print(st)
        print(et)
        total_price = 100
        reservation_status=True
        query=query = "INSERT INTO reservations (car_id, user_id, start_date, end_date, total_price, reservation_status) VALUES (%s, %s, %s, %s, %s, %s)"
        db.execute(query,(car_id,user["user_id"],st,et,total_price,reservation_status))
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
        print("afer db execute\n")
        reservation = db.fetchone()
        return reservation
    except mysql.connector.Error as err:
        print(f"Error getting car by license plate: {err}")
        return None
    finally:
        db.close()
        conn.close()
