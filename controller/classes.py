from controller import classes

class User:
    def __init__(self,username:str,password: str, role: str, firstname: str ,
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
    def __init__(self,brand: str, model: str, prod_year: int, plate:str, seats: int,doors: int, cc: int, state: str, desc: str,fuel: str, trans: str, 
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
        self.doors=doors
    

        

        
        