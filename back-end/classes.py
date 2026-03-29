import functions

class User:
    def __init__(self,uid: int,password: str, role: str, firstname: str ,
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
    try:
        """ car = functions.GetCars()
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
            print("Car2 does not exist") """
        cars = functions.FilterCars(None,None,None,None)
        print(cars)
    except Exception as e:
        print(f"Σφάλμα κατά την επικοινωνία με τη βάση from main: {e}")
        print("(Σιγουρέψου ότι το MySQL server τρέχει και το αρχείο functions.py είναι σωστό!)")

# Αυτό εξασφαλίζει ότι η main() τρέχει μόνο όταν εκτελείς αυτό το αρχείο απευθείας
if __name__ == "__main__":
    main() 