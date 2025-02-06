---

# 🚖 Taxi Booking System  

## 📌 Overview  
The **Taxi Booking System** is a **GUI-based application** built using **Python (Tkinter)** for users to **book rides** as **Customers** or **register as Drivers**. The system integrates **SQLite3 for user authentication**, a **logging mechanism for tracking activity**, and an intuitive **fare calculation system** based on distance, vehicle type, and additional options like luggage.  

## ⚡ Features  
- **User Authentication** (Login/Signup using SQLite3)  
- **Role Selection** (**Customer or Driver**)  
- **GUI-Based Interface** (Tkinter with custom themes)  
- **Ride Booking & Fare Calculation**  
- **Dynamic Location Selection** (Predefined locations with distance-based pricing)  
- **File Logging & Data Storage**  
- **Random Assignment of Customers & Drivers**  

## 🛠️ Technologies Used  
- **Python 3**  
- **Tkinter (GUI Framework)**  
- **SQLite3 (Database for User Credentials)**  
- **Pillow (For Image Handling)**  
- **OS & Random Modules (For File Management and Assignments)**  

## 🔧 Installation & Setup  

### 1️⃣ Prerequisites  
Ensure you have **Python 3** installed. Required dependencies:  
```sh
pip install pillow
```

### 2️⃣ Running the Application  
Run the Python script:  
```sh
python Taxi.py
```

## 📂 Project Structure  
```
📦 Taxi Booking System  
 ├── 📂 logs/              # Log files (rotating 5 files)  
 ├── 📂 images/            # GUI Images & Icons  
 ├── Users.db              # SQLite3 Database for User Authentication  
 ├── Taxi.py               # Main Application Script  
 ├── README.md             # Project Documentation  
```

## 🚀 How to Use  

### 1️⃣ User Authentication  
- Select **Customer** or **Driver**  
- **Sign In** if you have an account, else **Sign Up**  

### 2️⃣ Booking a Ride (For Customers)  
- **Enter Personal Details** (Name, Phone, Email, CNIC)  
- **Select Pickup & Drop Locations**  
- **Choose Vehicle Type** (Car/Bike)  
- **Optional**: Extra luggage or return trip  

### 3️⃣ Accepting a Ride (For Drivers)  
- **Enter Personal Details**  
- **Select Available Booking Requests**  
- **Confirm the ride**  

### 4️⃣ Payment Calculation  
- **Base Fare**: Fixed Rs. 50  
- **Distance Fare**: Dynamic pricing based on KM  
- **Vehicle Fare**: Rs. 8 (Bike), Rs. 10 (Car)  
- **Extra Charges**: Additional Rs. 30 for extra luggage  

## 📝 Logs & File Handling  
- The system **stores logs** in a rotating **log file system (5 files max)**  
- Each new session **appends** data to existing files  

## 🛠️ Possible Improvements  
- **Integration with Google Maps API** for real-time distance calculation  
- **Database Expansion** to store ride history  
- **Driver Rating System**  

---
