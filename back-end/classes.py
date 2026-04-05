import functions

class User:
    def __init__(self,uid: int, password: str, role: str, firstname: str ,
                  surname:str,email: str, phone: int, license_no: int, license_type: str):
        self.uid=uid
        self.password=password
        self.role=role
        self.firstname=firstname
        self.surname=surname
        self.email=email
        self.phone=phone
        self.license_no=license_no
        self.license_type=license_type
        
    #Εγγραφή χρήστη στο σύστημα
    #Instance method (μέθοδος του ίδιου του αντικειμένου)
    #Πρώτα δημιουργείται αντικείμενο User με τα στοιχεία που έδωσε ο πελάτης
    # και μετά του λέμε "αποθήκευσε τον εαυτό σου στη βάση"
    def RegisterUser(self):
        # Σύνδεση στη βάση
        conn, db = functions.ConnectDB()
        
        # Το SQL Query για την εισαγωγή
        # Δεν βάζουμε το User_ID, γιατί είναι AUTO_INCREMENT (το βάζει η MySQL μόνη της)
        # Ομοίως, η Registration_Date μπαίνει αυτόματα από τη βάση (CURRENT_TIMESTAMP)
        query = "INSERT INTO Users(user_password, user_role, first_name, Surname, "\
        "Email, Phone_Number, License_Number, License_Type) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);"
        
        # Τα δεδομένα του χρήστη σε μορφή tuple
        values = (
            self.role, 
            self.firstname, 
            self.surname, 
            self.email, 
            self.password,
            self.phone, 
            self.license_no, 
            self.license_type
        )
        
        try:
            # Εκτέλεση και αποθήκευση
            db.execute(query, values)
            conn.commit()
            
            # Παίρνουμε το ID που μόλις δημιούργησε η MySQL και το δίνουμε στο αντικείμενο
            self.uid = db.lastrowid
            
            print(f"Επιτυχία: Ο χρήστης {self.firstname} {self.surname} εγγράφηκε με νέο ID: {self.uid}!")
        except Exception as e:
            # Αν σκάσει, πιθανότατα ο χρήστης έβαλε Email ή Δίπλωμα που υπάρχει ήδη (λόγω του UNIQUE constraint)
            print(f"Σφάλμα κατά την εγγραφή: {e}")
            print("Μήπως το Email ή ο Αριθμός Διπλώματος χρησιμοποιούνται ήδη;")
            
        finally:
            db.close()
            conn.close()
    

class Car: 
    def __init__(self,brand: str, model: str, prod_year: int, plate:str, seats: int, cc: int, state: str, desc: str,fuel: str, trans: str, 
                 horsepower: int, imgPath: str, price: float, availability: bool):
        self.brand=brand
        self.model=model
        self.prod_year=prod_year
        self.plate=plate
        self.seats=seats
        self.cc=cc
        self.state=state
        self.desc=desc
        self.fuel=fuel
        self.trans=trans
        self.horsepower=horsepower
        self.imgPath=imgPath
        self.availability=availability
        self.price=price
    

        

            
    
 # Η κύρια συνάρτηση που τρέχει το πρόγραμμα
def main():
    print("Ξεκινάει η εφαρμογή...\n")

    # 2. Κλήση της μεθόδου που μιλάει με τη Βάση Δεδομένων (MySQL)
    """ print("\nΓίνεται κλήση στη βάση δεδομένων...")
    try:

        TEST
        car = functions.GetCars()

        car = functions.GetCars()
        print("From main ",car[2]) 
        car2 = Car( "Ford","Mustang",1969,"TES5",4,3273,"Available","Great car for showing off","Gas","Mechanical"
                   ,290,"/imgs/mustang.png",350.3,True
        )
        response = functions.CreateCar(car2)
        print("Response of getcars ",response)

        res = functions.CheckCarExists(car2)
        if res:
            print("Car2 exists")
        else:

            print("Car2 does not exist")


        user2 = User("123", "Dealer", "Panagiois", "Katsioyris", "panagikat@yahoo.com", "69", "69", "B")
        response = functions.CreateUser(user2)
        print("From main ", response)

        res = functions.CheckUserExists(user2)
        if res:
            print("User exists")
        else:
            print("User does not exist")
        TEST 

            print("Car2 does not exist") 
        cars = functions.FilterCars(None,None,None,None)
        print(cars) 
    except Exception as e:
        print(f"Σφάλμα κατά την επικοινωνία με τη βάση from main: {e}")
        print("(Σιγουρέψου ότι το MySQL server τρέχει και το αρχείο functions.py είναι σωστό!)") """

    # Δημιουργούμε το αντικείμενο στη μνήμη
    new_customer = User(
        uid=None,  # Δεν ξέρουμε ακόμα το ID
        password="5n47/Rb", 
        role="Customer", 
        firstname="Κατερίνα", 
        surname="Γεωργίου", 
        email="kater@gmail.com", 
        phone=6907339858, 
        license_no=98765434, 
        license_type="A"
    )

    # Καλούμε τη μέθοδο για να γράψουμε στη MySQL
    print("Προσπάθεια εγγραφής νέου χρήστη...")
    new_customer.RegisterUser()

# Αυτό εξασφαλίζει ότι η main() τρέχει μόνο όταν εκτελείς αυτό το αρχείο απευθείας
if __name__ == "__main__":
    main() 