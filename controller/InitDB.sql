drop database if exists eCar_db;
create database eCar_db;
use eCar_db;

create table cars(car_id int(8) auto_increment primary key,
brand varchar(13) not null,
model varchar(34) not null,
production_year year not null,
license_plate char(7) unique,
seats int(1) not null,
doors int(1) not null,
cc int(4),
state Enum('Available', 'In_Service', 'Unavailable') default 'Available',
car_description tinytext,
fuel_type Enum('Gas', 'Diesel', 'Hybrid', 'Electric'),
transmission_type enum('Manual', 'Auto'),
horsepower int(4),
image_path varchar(255),
price decimal(6,1) not null,
availability boolean default true);  

create table users(user_id int(3) primary key auto_increment,
username varchar(255) not null,
user_password varchar(255) not null,
user_role enum('Admin', 'Dealer', 'Customer') default 'Customer',
first_name varchar(40) not null,
surname varchar(40) not null,
email varchar(39) unique,
phone_number varchar(15),
registration_date DATETIME DEFAULT CURRENT_TIMESTAMP,
license_number varchar(20) unique,
license_type varchar(3));
 
 create table reservations(reservation_id int auto_increment primary key,
 car_id int(8),
 user_id int(3) not null,
 start_date datetime,
 end_date datetime,
 total_price decimal(6,1),
 reservation_status varchar(21) not null,
 FOREIGN KEY (Car_ID) REFERENCES cars(Car_ID) ON DELETE RESTRICT,
 FOREIGN KEY (User_ID) REFERENCES users(User_ID) ON DELETE CASCADE);

INSERT INTO cars 
(brand, model, production_year, license_plate, seats, doors, cc, state, car_description, fuel_type, transmission_type, horsepower, image_path, price, availability)
VALUES
('Toyota', 'Aygo', 2011, 'XEO9053', 5, 4, 1000, 'Available', 'TOTOYA EGG', 'Gas', 'Manual', 70, 'XEO9053', 45.0, TRUE),

('Mercedes', 'e200', 2001, 'ITT4171', 5, 4, 2000, 'Available', 'ALBANIAN MAFIA MERCEDES', 'Gas', 'Manual', 200, 'ITT4171', 250.0, TRUE),

('BMW', 'e39', 2000, 'APE9350', 5, 4, 2979, 'Available', 'Beba', 'Gas', 'Manual', 125, 'APE9350', 120.0, TRUE),

('OPEL', 'CORSA', 2003, 'ZMO9981', 2, 5, 1389, 'Available', '200 euro car', 'Gas', 'Manual', 70, 'ZMO9981', 50.0, TRUE),

('PEUGEOT', '206', 2001, 'ZZM5364', 5, 5, 1300, 'Available', 'OG peugeot', 'Gas', 'Manual', 86, 'ZZM5364', 150.0, TRUE),

('CITROEN', 'SAXO', 1998, 'AΡΕ2763', 5, 4, 1200, 'In_Service', 'Exploded', 'Gas', 'Manual', 75, 'AΡΕ2763', 30.0, TRUE);


INSERT INTO users
(username, user_password, user_role, first_name, surname, email, phone_number, license_number, license_type)
VALUES
('admin', 'a', 'Admin', 'Admin', 'Admin', 'admin@gmail.com', '6900000001', '', ''),

('user1', 'u1', 'Customer', 'Alice', 'Smith', 'user1@gmail.com', '6900000002', 'LIC67890', 'B'),

('dealer', 'd1', 'Dealer', 'Mike', 'Brown', 'dealer@gmail.com', '6900000003', 'LIC54321', 'B');

INSERT INTO reservations
(car_id, user_id, start_date, end_date, total_price, reservation_status)
VALUES

-- Toyota Corolla (car_id = 1)
(1, 1,
'2026-05-15 10:00:00',
'2026-05-18 10:00:00',
135.0,
'Confirmed'),

-- Tesla Model 3 (car_id = 2)
(2, 2,
'2026-05-20 09:00:00',
'2026-05-25 09:00:00',
600.0,
'Confirmed'),

-- Hyundai i20 (car_id = 5)
(5, 3,
'2026-05-12 14:00:00',
'2026-05-14 14:00:00',
60.0,
'Pending'),

-- Another reservation for Corolla
(1, 2,
'2026-05-22 08:00:00',
'2026-05-24 08:00:00',
90.0,
'Confirmed'),

-- Cancelled reservation (should NOT block availability)
(2, 1,
'2026-05-28 10:00:00',
'2026-05-30 10:00:00',
240.0,
'Cancelled');