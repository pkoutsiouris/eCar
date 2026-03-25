import functions

class User:
    def __init__(self,uid: int,password: str, role: str, firstname: str , surname:str,email: str, phone: int, license_no: int, license_type: str):
        self.uid=uid
        self.password=password
        self.role=role
        self.firstname=firstname
        self.surname=surname
        self.email=email
        self.phone=phone
        self.license_no=license_no
        self.license_type=license_type
    

class Car: 
    def __init__(self,cid: int,brand: str, model: str, prod_year: int, plate:str, seats: int, cc: int, state: str, desc: str,fuel: str, trans: str, 
                 horsepower: int, imgPath: str, price: float, availability: bool):
        self.cid=cid
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
    
    def GetCars():
        db = functions.ConnectDB()
        query = "select * from cars;"
        db.execute(query)
        car = db.fetchone()
        print(car)
        db.close()

# Η κύρια συνάρτηση που τρέχει το πρόγραμμα
def main():
    print("Ξεκινάει η εφαρμογή...\n")

    # 2. Κλήση της μεθόδου που μιλάει με τη Βάση Δεδομένων (MySQL)
    print("\nΓίνεται κλήση στη βάση δεδομένων...")
    try:
        Car.GetCars()
    except Exception as e:
        print(f"Σφάλμα κατά την επικοινωνία με τη βάση: {e}")
        print("(Σιγουρέψου ότι το MySQL server τρέχει και το αρχείο functions.py είναι σωστό!)")

# Αυτό εξασφαλίζει ότι η main() τρέχει μόνο όταν εκτελείς αυτό το αρχείο απευθείας
if __name__ == "__main__":
    main()