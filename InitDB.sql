drop database if exists eCar_db;
create database eCar_db;
use eCar_db;

create table cars(car_id int(8) auto_increment primary key,
brand varchar(13) not null,
model varchar(34) not null,
production_year year not null,
license_plate char(7) unique,
seats int(1) not null,
cc int(4),
state Enum('Available', 'In_Service', 'Unavailable') default 'Available',
car_description tinytext,
fuel_type Enum('Gas', 'Diesel', 'Hybrid', 'Electric'),
transmission_type enum('Mechanical', 'Auto'),
horsepower int(4),
image_path varchar(255),
price decimal(6,1) not null,
availability boolean default true);  

create table users(user_id int(3) primary key auto_increment,
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