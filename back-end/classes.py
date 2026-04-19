import functions

class User:
    def __init__(self, username: str, password: str, role: str, firstname: str ,
                  surname:str,email: str, phone: int, license_no: int, license_type: str):
        self.username=username
        self.password=password
        self.role=role
        self.firstname=firstname
        self.surname=surname
        self.email=email
        self.phone=phone
        self.license_no=license_no
        self.license_type=license_type
    
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
    print("\nΓίνεται κλήση στη βάση δεδομένων...")
    """try:

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

        cars = functions.FilterCars(None,None,None,None)
        print(cars)


        user2 = User("123", "Dealer", "Panagiois", "Katsioyris", "panagikat@yahoo.com", "69", "69", "B")
        response = functions.CreateUser(user2)
        print("From main ", response)

        res = functions.CheckUserExists(user2)
        if res:
            print("User exists")
        else:
            print("User does not exist")

        
        print("Test 1: Get Users")
        all_users = functions.GetUsers()
        print(f"Found{len(all_users)} in database")
        for u in all_users:
            print(f" -> Email: {u['email']} | Ρόλος: {u['user_role']}")


        print("--- ΤΕΣΤ 2: GiveAdminAccess ---")
        test_email1="panagikat@yahoo.com"
        test_email = "marisa@test.com" #email που δεν εχει καταχωρηθει
        functions.GiveAdminAccess(test_email1)
        functions.GiveAdminAccess(test_email)


        print("--- ΤΕΣΤ 3: Επιβεβαίωση (Ξανά GetUsers) ---")
        all_users_again = functions.GetUsers()
        for u in all_users_again:
            if u['email'] == test_email1:
                print(f"Ο νέος ρόλος του {u['email']} στη βάση είναι πλέον: {u['user_role']}")


        print("--- ΤΕΣΤ 4: GiveDealerAccess ---")
        functions.GiveDealerAccess(test_email)


# Δοκιμή Δημιουργίας χρήστη
    try:
        # Δημιουργούμε το αντικείμενο στη μνήμη
        new_customer = User(
        username="oti nanai250",  
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
        functions.  RegisterUser(new_customer)
    except Exception as e:
        print(f"Σφάλμα κατά την επικοινωνία με τη βάση from main: {e}")

# Test: Edit car description
    try:
        new_car = Car("Toyota","C-HR",2021,"XAL1523",5,1800,"Available",
        "Σε άριστη κατάσταση","Hybrid","Auto",122,"/imgs/chr.png",229.0,True
        )
        functions.CreateCar(new_car)

        print("Προσπάθεια επεξεργασίας περιγραφής αυτοκινήτου:")
        functions.ChangeCarDescr(new_car, "Δεκτός κάθε έλεγχος")
    except Exception as e:
        print(f"Σφάλμα κατά την επικοινωνία με τη βάση from main: {e}")

# Test: Edit car price
    try:
        new_car = Car("Toyota","C-HR",2021,"XAL1523",5,1800,"Available",
        "Σε άριστη κατάσταση","Hybrid","Auto",122,"/imgs/chr.png",229.0,True
        )
        functions.CreateCar(new_car)

        print("Προσπάθεια αλλαγής τιμής αυτοκινήτου:")
        functions.ChangeCarPrice(new_car, 222.0)
    except Exception as e:
        print(f"Σφάλμα κατά την επικοινωνία με τη βάση from main: {e}")
        """
"""
    # --- Test: Get User Reservations ---
    try:
        test_email_res = "marisa@test.com" # Βάλε ένα email που σίγουρα υπάρχει στη βάση
        print(f"\n--- Προσπάθεια ανάκτησης κρατήσεων για το email: {test_email_res} ---")
        
        # 1. (Προαιρετικά) Μπορούμε πρώτα να φτιάξουμε μια κράτηση για να είμαστε σίγουροι ότι υπάρχει
        # start_date = "2026-05-01 10:00"
        # end_date = "2026-05-05 10:00"
        # car_id = 1 # Υποθέτουμε ότι υπάρχει αυτοκίνητο με id 1
        # functions.CreateReservation(test_email_res, start_date, end_date, car_id)
        
        # 2. Τεστάρουμε την GetUserReservations
        reservations = functions.GetUserReservations(test_email_res)
        
        if reservations:
            print("Βρέθηκε κράτηση (ή κρατήσεις):")
            print(reservations)
        else:
            print("Δεν βρέθηκε καμία κράτηση για αυτόν τον χρήστη ή ο χρήστης δεν υπάρχει.")
            
    except Exception as e:
        print(f"Σφάλμα κατά την εκτέλεση του GetUserReservations test: {e}")
""" 

# Αυτό εξασφαλίζει ότι η main() τρέχει μόνο όταν εκτελείς αυτό το αρχείο απευθείας
if __name__ == "__main__":
    main() 