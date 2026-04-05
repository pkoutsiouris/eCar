
import mysql.connector
from . import classes

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
            
        car.imgPath = car.plate
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

def FilterCars(price: float, year: int, cc: int, horses: int):
    try:
        conn, db = ConnectDB()
        prflag = False
        yrflag = False
        ccflag = False
        horseflag = False

        query = "SELECT * FROM cars"

        if price is not None:
            query += " WHERE "
            prflag = True
            query += "price=" + str(price)

        if year is not None:
            if prflag:
                query += " AND production_year=" + str(year)
            else:
                query += " WHERE production_year=" + str(year)
            yrflag = True

        if cc is not None:
            if prflag or yrflag:
                query += " AND cc=" + str(cc)
            else:
                query += " WHERE cc=" + str(cc)
            ccflag = True

        if horses is not None:
            if prflag or yrflag or ccflag:
                query += " AND horsepower=" + str(horses)
            else:
                query += " WHERE horsepower=" + str(horses)
            horseflag = True

        query += ";"

        print(query)  # debug
        db.execute(query)
        cars = db.fetchall()
        return cars

    except mysql.connector.Error as err:
        print(f"Σφάλμα σύνδεσης με τη βάση: {err}")
        return False
    finally:
        db.close()
        conn.close()

#TODO update/cars, register  

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

def CreateUser(user: classes.User):
    try:
        conn,db = ConnectDB()
        if CheckUserExists(user):
            print("User already exists with email: " + user.email)  
            return False
        
        query=" INSERT INTO users (user_password, " \
        "user_role, first_name, surname, email, phone_number, " \
        "license_number, license_type) VALUES (" \
        "%s , %s ,%s ,%s ,%s ,%s ,%s ,%s)"
        db.execute(query,(user.password,user.role,user.firstname,user.surname,user.email,user.phone,user.license_no,
                          user.license_type))
        conn.commit()
        return True
    except mysql.connector.Error as err:
        print(f"Σφάλμα σύνδεσης με τη βάση: {err}")   
        return False
    finally:
        db.close()
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