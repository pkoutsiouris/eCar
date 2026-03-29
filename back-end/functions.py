
import mysql.connector
import classes

def ConnectDB():
    try:
        # Προσοχή: Εδώ θα βάλετε τα δικά σας στοιχεία της MySQL
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="8716",
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

def FilterCars(price: float, year: int, cc: int , horses: int):
    try:
        conn,db=ConnectDB()
        prflag=False
        yrflag=False
        ccflag=False
        horseflag=False
        query="select * from cars"
        if price is not None:
            query=" where "
            prflag=True
            query=query+" price='"+str(price)+"'"

        if year is not None:
            if prflag:
                query=query+"and production_year='"+str(year)+"'"
            else:
                query=query+" production_year='"+str(year)+"'"
            yrflag=True

        if cc is not None:
            if prflag or yrflag:
                query=query + "and cc='"+str(cc)+"'"
            else:
                query=query + " cc='"+str(cc)+"'"
            ccflag=True
        if horses is not None:
            if prflag or yrflag or ccflag:
                query=query+" and horsepower='"+str(horses)+"'"
            else:
                query=query+" horsepower='"+str(horses)+"'"
            horseflag=True
            
        query=query+";"
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
