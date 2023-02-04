# Importing tkinter
from tkinter import *
from tkinter import ttk
from tkinter import messagebox as ms
from tkinter.font import BOLD
from PIL import ImageTk, Image
# Importing built-in python modules for use
import random
import time
# Importing SqLite, for better file-handling (for .db files instead of .txt)
import sqlite3 # Better for coding with GUI
# Builtin import to get path for files from code
import os.path

# File managing (.db), take database of users (even if not exists already) at program start up 
with sqlite3.connect('Users.db') as db:
    curs = db.cursor() # Make a simple .db file called "Users", refer it as "db" and implement it using 'curs'
# Create file in case if it doesn't exist already
curs.execute('CREATE TABLE IF NOT EXISTS user (username TEXT NOT NULL ,password TEXT NOT NULL)')
db.commit() # Test file to make sure it works
db.close() # Close file until needed
# Creating a variable for Driver/Customer then their inverse
User = ""
# File managing (.txt)
# Limit for log files is 5, to be safe from excess memory usage
# Checking if folder exists or not
if not os.path.exists('logs/'):
    os.makedirs('logs/') # If it doesn't exist, then make it

def checker(): # Function to check/create new files each time program is used
    if os.path.isfile('logs/logs5.txt'): # If limit reached (5)
        logselector = random.randint(1,5) # Re-use files
        with open(f'logs/logs{logselector}.txt','w') as adder: # Open the file
            adder.writelines('') # Clear everything in it
        return f'logs/logs{logselector}.txt' # Return path for future use
    if os.path.isfile('logs/logs4.txt'): # If 4th file exists
        with open('logs/logs5.txt','w') as adder: # Make 5th file
            adder.writelines('') # Clear everything in it
        return 'logs/logs5.txt' # Return path for future use
    elif os.path.isfile('logs/logs3.txt'): # If 3rd file exists
        with open('logs/logs4.txt','w') as adder: # Make 4th file
            adder.writelines('') # Clear everything in it
        return 'logs/logs4.txt' # Return path for future use
    elif os.path.isfile('logs/logs2.txt'): # If 2nd file exists
        with open('logs/logs3.txt','w') as adder: # Make 3rd file
            adder.writelines('') # Clear everything in it
        return 'logs/logs3.txt' # Return path for future use
    elif os.path.isfile('logs/logs1.txt'): # If 1st file exists
        with open('logs/logs2.txt','w') as adder: # Make 2nd file
            adder.writelines('') # Clear everything in it
        return 'logs/logs2.txt' # Return path for future use
    else: # If no file exists
        with open('logs/logs1.txt','w') as adder: # Make the 1st file
            adder.writelines('') # Clear everything in it
        return 'logs/logs1.txt' # Return path for future use
file_name = checker() # Store path of the file (the returned one)
print('L'+file_name[6:10],'created') # Print the file-name which was created

e_list = [] # Using list method to export data into files
def file_mng(x): # Main file managing function which stores data in files 1 by 1 lines
    print(x) # First print the data in output
    e_list.append(x) # Store in the list (to export later)
    to_add = [] # Make new list to define a new lines
    for i in e_list: # Select each line and store in 'i'
        to_add.append(str(i)) # Define them in the new list
    with open(file_name,'a') as filey: # Open the defined file as 'filey'
        filey.writelines(to_add[-1]) # Store the latest added line in the file
file_mng('Application Started\n') # Initiate file managing 

# Colors class, to define colors which can be used anywhere in the program
class Colors: 
    def __init__(self): # Initiate all colors in the constructor (__init__ is called constructor)
        self.white = "white"
        self.gold = "gold"
        self.d_gold = "#F4BB00" # Hex-Code for Dark Gold
        # Different shades of yellow (using Hex-codes)
        self.yellow = "yellow"
        self.yellow1 = "#FABD02" 
        self.yellow2 = "#FFC30B"
        self.yellow3 = "#FDA50F"
        self.yellow5 = "#FDC12A"

color = Colors() # Making an object for colors to be used anywhere
FONT = 'Calibri' # Setting a constant font to be used anywhere

# Login Class (To be called when file is ran, to start the GUI)
class Login:
    def __init__(self,master): # Importing information from "root" (root is defined at end of the file)
        # Window (Calling root in the file, as 'master' in Class)
        self.master = master
        # Some Usefull variables
        # For signing in
        self.username = StringVar()
        self.password = StringVar()
        # For signing up
        self.n_username = StringVar()
        self.n_password = StringVar()

    #Login Function
    def login(self):
        #Connecting python with file (for file handling, importing Usernames and Passwords)
        with sqlite3.connect('Users.db') as db:
            curs = db.cursor()
        #Finding user (Instructions for .db file)
        find_user = ('SELECT * FROM user WHERE username = ? and password = ?')
        # Getting all usernames and passwords previously entered to log in
        curs.execute(find_user,[(self.username.get()),(self.password.get())])
        # Check for Usernames/Passwords in the file
        result = curs.fetchall()
        # If the username/passwords work, let the user continue to the main Cab-Booking window 
        if result:
            self.logf.pack_forget() # Close the login window
            self.head['text'] = (f"Welcome, {self.username.get()} - ({User})") # Grab the Username to display on Cab Window
            self.head.configure(fg="green") # Color of username (to be displayed)
            self.head.pack(fill=BOTH) # Fill 'both' x and y coordinates with this information
            application = Information(root) # Initiate the Cab Booking window (The main task)
        # If username/passwords don't work, give error and let user try again
        else:
            ms.showerror('Oops!','Username Not Found.')
    
    # In case there is no account to login, or simply for making a new account
    def new_user(self):
        #Connecting python with file (for file handling, importing Usernames and Passwords)
        with sqlite3.connect('Users.db') as db:
            curs = db.cursor()
        # Find existing username, to prevent duplicate usernames
        find_user = ('SELECT * FROM user WHERE username = ?') # Instructions for .db file
        curs.execute(find_user,[(self.username.get())]) # Getting Username        
        if curs.fetchall(): # If it exists:
            ms.showerror('Error!','Username Already Taken!')
        else: # If it doesn't exist, make it.
            ms.showinfo('Success!','Account Created!')
            self.log() # Prompt back to login menu
        # Create New Account 
        insert = 'INSERT INTO user(username,password) VALUES(?,?)' # Instructions for .db file
        # Instead of reading previously entered usernames, write them into the file (making new account)
        curs.execute(insert,[(self.n_username.get()),(self.n_password.get())]) 
        db.commit() # Saving everything in file

    # Prompting to Login menu
    def log(self):
        # Set to empty (so user can enter)
        self.username.set('')
        self.password.set('')
        self.signupf.pack_forget() # Reset information to clean workspace 
        self.head['text'] = f'Sign In ({User})' # Header text
        self.logf.pack() # Displaying

    # In case of Signing up menu (New account)
    def signup(self):
        # Set to empty (so user can enter) 
        self.n_username.set('') 
        self.n_password.set('')
        self.logf.pack_forget() # Reset information to clean workspace
        self.head['text'] = f'Sign Up ({User})'
        self.signupf.pack() # Displaying

    # If the user is the Customer
    def prompterU(self):
        global User
        User = "Customer"
        self.username.set('')
        self.password.set('')
        self.selectf.pack_forget() # Reset information to clean workspace 
        self.head['text'] = 'Sign In (Customer)' # Header text
        self.logf.pack() # Displaying
    
    # If the user is the driver
    def prompterD(self):
        global User
        User = "Driver"
        self.username.set('')
        self.password.set('')
        self.selectf.pack_forget() # Reset information to clean workspace 
        self.head['text'] = 'Sign In (Driver)' # Header text
        self.logf.pack() # Displaying

    # Going back to the selection Menu
    def backer(self):
        self.username.set('')
        self.password.set('')
        self.logf.pack_forget() # Reset information to clean workspace 
        self.signupf.pack_forget()
        self.head['text'] = 'Re-Select' # Header text
        self.selectf.pack() # Displaying       

# Making Widgets (aka buttons) for the login menu
class Widgets(Login): # Inheritting Login
    # All buttons for the login menu
    def LoginMenu(self):
        global colors # Globalize the colors class to be used anywhere
        # Label indicates text, Entry indicates input, Button indicated button
        # Labelling Header of the file, master is root, defining MainFrame font with size 35
        self.head = Label(self.master,text = 'Selecting Menu',font = ('',35),pady = 10) # padx is x-axis, pady is y-axis
        self.head.pack() # Displaying
        self.selectf = Frame(self.master, padx = 10, pady = 10) # Defining a select menu for driver/user
        Label(self.selectf,text = 'Enter as:- ',font = ('',22),pady=5,padx=5).grid(sticky = W) # Using selecting frame to show text on GUI
        # Using Selecting frame to select joining as "Driver" or "Customer" button to go to Sign in Window
        Button(self.selectf,bg = color.yellow5,text = ' User ',bd = 3 ,font = ('',15),padx=8,pady=8,command=self.prompterU).grid(row=3,column=0) # Using command 'signup'
        Label(self.selectf,text = '     ',font = ('',20),pady=5,padx=5).grid(row=3,column=1) # Adding Empty space between buttons
        Button(self.selectf,bg = color.yellow5,text = ' Driver ',bd = 3 ,font = ('',15),padx=8,pady=8,command=self.prompterD).grid(row=3,column=2) # Using command 'signup'
        self.selectf.pack() # Display on GUI


        self.logf = Frame(self.master,padx = 10, pady = 10) # Defining a Login frame
        # Using Login frame to show text on the GUI
        Label(self.logf,text = 'Username: ',font = ('',20),pady=5,padx=5).grid(sticky = W)
        # Using Login frame to get username from user on the GUI (stores whatever user inputs in a variable)
        Entry(self.logf,bg = color.white,textvariable = self.username,bd = 5,font = ('',15)).grid(row=0,column=1)
        # Using Login frame to show text on the GUI
        Label(self.logf,text = 'Password: ',font = ('',20),pady=5,padx=5).grid(sticky = W)
        # Using Login frame to get password from user on the GUI (stores whatever user inputs in a variable) 
        Entry(self.logf,bg = color.white,textvariable = self.password,bd = 5,font = ('',15),show = '*').grid(row=1,column=1) # show = '*' blurs out the password
        # Using Login frame to define a "Sign in" button to Sign in
        Button(self.logf,bg = color.yellow5,text = ' Sign In ',bd = 3 ,font = ('',15),padx=5,pady=5,command=self.login).grid(row=3,column=0) # Using command 'login'
        # Using Login frame to define a "Sign Up" button to go to Sign up Window
        Button(self.logf,bg = color.yellow5,text = ' Sign Up ',bd = 3 ,font = ('',15),padx=5,pady=5,command=self.signup).grid(row=3,column=1) # Using command 'signup'
        
        Button(self.logf,bg = color.yellow5,text = ' Back ',bd = 3 ,font = ('',15),padx=5,pady=5,command=self.backer).grid(row=3,column=2) # Using command 'signup'
        

        self.signupf = Frame(self.master,padx = 10,pady = 10) # Defining a SignUp frame
        # Using SignUp frame to show text on the GUI
        Label(self.signupf,text = 'Username: ',font = ('',20),pady=5,padx=5).grid(sticky = W)
        # Using SignUp frame to get username from user on the GUI (stores whatever user inputs in a variable)
        Entry(self.signupf,bg = color.white,textvariable = self.n_username,bd = 5,font = ('',15)).grid(row=0,column=1)
        # Using SignUp frame to show text on the GUI
        Label(self.signupf,text = 'Password: ',font = ('',20),pady=5,padx=5).grid(sticky = W)
        # Using SignUp frame to get passwords from user on the GUI (stores whatever user inputs in a variable)
        Entry(self.signupf,bg = color.white,textvariable = self.n_password,bd = 5,font = ('',15),show = '*').grid(row=1,column=1)
        # Using SignUp frame to define a "Sign Up" button to Sign Up a new account
        Button(self.signupf,bg = color.yellow5,text = 'Sign Up',bd = 3 ,font = ('',15),padx=5,pady=5,command=self.new_user).grid(row=3,column=0)
        # Using Login frame to define a "Go to Sign In" button to go back to login menu 
        Button(self.signupf,bg = color.yellow5,text = 'Go to Sign In',bd = 3 ,font = ('',15),padx=5,pady=5,command=self.log).grid(row=3,column=1)

        Button(self.signupf,bg = color.yellow5,text = ' Back ',bd = 3 ,font = ('',15),padx=5,pady=5,command=self.backer).grid(row=3,column=2) # Using command 'signup'

# Making a main frame (window) for the Cap booking application
class MainFramme: # It defines a massive window on which everything will be working.
    def __init__(self):
        MainFrame=Frame(root) # Use same 'root' to define the MainFrame
        MainFrame.pack(fill=BOTH,expand=True) # Display the MainFrame on GUI filling the screen
        
        # Making the header (title) sub-frame of MainFrame
        Tops = Frame(MainFrame,bg=color.d_gold, bd=20, width=1350,relief=RIDGE) 
        Tops.pack(side=TOP,fill=X,expand=True) # Displaying the header frame on GUI

        # Defining the title on the header frame, the text is defined with 18 empty spaces then the title
        self.lblTitle=Label(Tops,bg=color.d_gold,font=(FONT,64,'bold'),text=(" " * 18) + "Online Cab Booking System")
        self.lblTitle.grid(row=0,column=0) # Specifiying its location
        # Defining Multi-line string, (" " * 35) shows 35 empty spaces and so on..
        Made_by = "\n"+(" " * 35) + "Made by: \n" + (" " * 35) + "Kiran Qaiser\n" + (" " * 35) + "251683919"
        # Defining the sub-title on the header frame
        self.lblSubTitle=Label(Tops,bg=color.d_gold,font=(FONT,14,'bold'),text=Made_by)
        self.lblSubTitle.grid(row=0,column=1) # Specifying its location

        global CustomerDetailsFrame # Globalizing frame so it can be used anywhere
        # Making the CustomerDetailsFrame, a sub-frame of MainFrame
        # It contains all Customer related info
        CustomerDetailsFrame=LabelFrame(MainFrame, width=1350,bd=20, pady=5, relief=RIDGE)
        CustomerDetailsFrame.pack(side=BOTTOM,fill=BOTH,expand=True) # Display on GUI

        global FrameDetails # Globalizing frame so it can be used anywhere
        # Making 'FrameDetails', a sub-frame of CustomerDetails
        # It contains all customer's details (info/vehicletype/journeytype/driver/payment)
        FrameDetails=Frame(CustomerDetailsFrame, width=880,bd=10, relief=RIDGE)
        FrameDetails.pack(side=LEFT,fill=BOTH,expand=True) # Displaying on GUI

'''
Important Note: 
StringVar() / IntVar() or similar keywords
are builtin Class-Methods which allow us to get/set
then use/edit the variables/integers how-ever we want.
Normally this is preffered to be done the python way (to directly declare)
but this way tkinter can easily run these methods in the back-end with more efficiency
Example:
x = "" is same thing as x = StringVar()
x = 0 is same thing as x = IntVar()
'''

# Making a class for type of vehicle (Veh) and type of journey (Jor), hence VehJorType
# Type of vehicle selects 'Car' or 'Bike'
# Type of journey selects 'Drop only' or 'Drop and Return' 
class VehJorType: # Initiating Class
    def __init__(self): # Constructor to define basic variables for this function
        self.Bike=StringVar() # Making 'Bike' string
        self.Car=StringVar() # Making 'Car' string
        self.carType = IntVar() # Making 'carType' integer (0 for 'None', 1 for 'Bike', 2 for 'Car)
        # Making 'journeyType' integer (0 for 'None', 1 for 'Drop only', 1 for 'Drop and Return')
        self.journeyType = IntVar()

        self.Bike.set("0") # Setting 'Bike' as 0 (0 means it cannot be used)
        self.Car.set("0") # Setting 'Car' as 0 (0 means it cannot be used)
        self.carType.set(0) # Setting 'carType' as 0 
        self.journeyType.set(0) # Setting 'journeyType' as 0

        # Defining 'Booking Frame', a sub-frame of 'FrameDetails'
        # It contains the Option to book for carType and journeyType
        Book_Frame=LabelFrame(FrameDetails,width=300,height=150,relief=FLAT)
        Book_Frame.grid(row=1,column=0) # Display on GUI
    
        # Making a method to select vehicle
        def selectCar():
            global Item5 # Globalizing variable (Different price for Car/Bike)
            if self.carType.get() == 1: # If type is '1'
                self.txtCar.configure(state = DISABLED) # Disable use of Car
                self.Car.set("0") # Set Car as 0, making it unusable
                self.txtBike.configure(state = NORMAL) # Enable use of Bike
                Item5 = float(8) # Price of Bike
                self.Bike.set("Rs "+ str(Item5)) # Setting Bike's Price
            elif self.carType.get() == 2: # If type is '2'
                self.txtBike.configure(state =DISABLED) # Disable use of Bike
                self.Bike.set("0") # Setting Bike as 0, making it unusable
                self.txtCar.configure(state = NORMAL) # Enable use of Car
                Item5 = float(10) # Price of Car
                self.Car.set("Rs "+ str(Item5)) # Setting Car's Price
            else: # In case of '0' or anything else except '1' or '2', disable both Car and Bike
                self.txtBike.configure(state =DISABLED) # Disable Bike
                self.Bike.set("0") # Set Bikes to 0
                self.txtCar.configure(state = DISABLED) # Disable Car
                self.Car.set("0") # Set Cars to 0
        
        #
        # Buttons on GUI to select vehicleType/JourneyType
        #

        # "Radio Button" means that only 1 instance (from same variable) can be selected, both Bike and Car cannot be selected.
        # Making a button for Bike, If selected, sets value to '1', which is for bike, command "selectCar" is used.
        self.chkBike = Radiobutton(Book_Frame,text="Bike",value=1,variable = self.carType,font=(FONT,14,'bold'),command=selectCar).grid(row=0, column=0, sticky=W)
        self.txtBike = Label(Book_Frame,font=(FONT,14,'bold'),width =7,textvariable=self.Bike,bd=5, state= DISABLED, justify=RIGHT,bg="white",relief=SUNKEN)
        self.txtBike.grid(row=0,column=1) # Displaying on GUI on specific position
        
        # Making a button for Car, If selected, sets value to '2', which is for car, command "selectCar" is used.
        self.chkCar = Radiobutton(Book_Frame,text="Car",value=2,variable = self.carType,font=(FONT,14,'bold'),command=selectCar).grid(row=1, column=0, sticky=W)
        self.txtCar = Label(Book_Frame,font=(FONT,14,'bold'),width =7,textvariable=self.Car,bd=5, state= DISABLED, justify=RIGHT,bg="white",relief=SUNKEN)
        self.txtCar.grid(row=1,column=1) # Displaying on GUI on specific position

        # Making buttons for type of journey
        if User == "Customer":
            # Making a button for "Drop only", If selected, sets value to '1', which is for 'Drop Only'                  
            self.chkDropOnly =Radiobutton(Book_Frame,text="Drop only",value=1,variable = self.journeyType,font=(FONT,14,'bold')).grid(row=0, column=2, sticky=W)
            # Making a button for "Drop & Return", If selected, sets value to '2', which is for 'Drop and Return'                                                              
            self.chkDropnReturn =Radiobutton(Book_Frame,text="Drop & Return",value=2,variable = self.journeyType,font=(FONT,14,'bold')).grid(row=1, column=2, sticky=W)
        if User == "Driver":
            # Making a button for "Allowing Drop only", If selected, sets value to '1', which is for 'Drop Only'
            self.chkDropOnly =Radiobutton(Book_Frame,text="Allow Drop only?",value=1,variable = self.journeyType,font=(FONT,14,'bold')).grid(row=0, column=2, sticky=W)
            # Making a button for "Allowing Drop & Return", If selected, sets value to '2', which is for 'Drop and Return'                                                              
            self.chkDropnReturn =Radiobutton(Book_Frame,text="Allow Drop & Return?",value=2,variable = self.journeyType,font=(FONT,14,'bold')).grid(row=1, column=2, sticky=W)

# Making a class for Customer (Cust) Info and selecting drivers (Driv)
# Customer Info is completely user-dependent, they enter information
# Drivers are defined by the company, waiting for Customers to be used
class CustDriv(MainFramme): # Defining Class, inheritting the MainFrame
    def __init__(self):
        self.Firstname=StringVar() # Making 'Firstname' string
        self.Lastname=StringVar() # Making 'Lastname' string
        self.Address=StringVar() # Making 'Address' string
        self.Gender=StringVar() # Making 'Gender' string
        self.PhoneNum=StringVar() # Making 'PhoneNum' string
        self.CNIC=StringVar() # Making 'CNIC' string
        self.Email=StringVar() # Making 'Email' string
        self.License=StringVar() # Making 'License' string is user is driver

        self.Custer=StringVar() # Making 'Custer' string (To choose random customers if driver is selected, else random drivers if customer is selected)
        self.var5 = IntVar() # Making 'var5' integer, this will be used to determing the driver.
        # '1' value refers to a driver, '0' refers to "Any" driver || Every iteration will get random drivers
        self.Custer.set("Any") # Setting 'Driver' to Any (None) 

        # Defining 'Customer Info' frame, a sub-frame of 'FrameDetails'
        # It contains the frame for the user/customer to enter their information.
        CustomerInfo=LabelFrame(FrameDetails, width=150,height=250,bd=10, font=(FONT,12,'bold'),text=f"{User} Info", relief=RIDGE)
        CustomerInfo.grid(row=0,column=0) # Display on GUI at specific location

        global TravelFrame # Globalizing frame so it can be used anywhere
        # Defining 'Travel Frame', a sub-frame of 'FrameDetails', 
        # Tt contains all information regarding travelling (driver/pick/drop)
        TravelFrame = LabelFrame(FrameDetails,bd=10, width=300,height=250, font=(FONT,12,'bold'),text="Booking Detail (Customer)", relief=RIDGE)
        TravelFrame.grid(row=0,column=1) # Display on GUI at specific location
        
        # Making Custer method to get drivers/customers assigned by the company.
        def Custerr():
            global custer # Globalizing the selected customer/driver
            if (self.var5.get()==1): # If 'var5' is '1', it means the customer/driver is allowed (selected)
                self.txtCuster.configure(state = NORMAL) # Allow changing the selected customer/driver if needed
                # Different drivers assigned or customers provided by the company
                Custers = ["Qasim Khan"       , "Shahid Shoukat"   , "Kastor Arkantos",
                           "Sindhu Badam Wala", "Shafqat Mehmood"  , "Pervaiz Jutt",
                           "Ghafoor-Ullah"    , "Zain Zahideen"    , "Kamal-ud-deen",
                           "Zyahudeen"        , "Tahmoor Hayat"    , "Malik Ghafoor",
                           "Riaz Ahmed"       , "Shehryar Anjum"   , "Malik Riaz",
                           "Ammar Tamater"    , "Qureshi Sahib"    , "Sheikh Wahab", 
                           "Abu-Bakar Amir"   , "Wassay Amir"      , "Humas Hussain",
                           "Warina Kassim"    , "Abdul Ghori"      , "Shehzaad Ali",
                           "Bashir Ahmed"     , "Rashid Usama"     , "Alina Saeed",
                           "Usaid Zahid"      , "Harry Puttar"     , "Isbah Qureshi"]
                History_Rides = [", N/A",", 1",", 2",", 3",", 4",", 5",", 6",", 7",", 8",", 9"]
                # Getting a random driver from the drivers list                                           
                if User == "Customer": # If user is customer, define driver along with history of rides (how many rides)
                    custer = Custers[random.randint(0,len(Custers)-1)] + History_Rides[random.randint(0,len(History_Rides)-1)]
                if User == "Driver": # If user is driver, simply provide customer
                    custer = Custers[random.randint(0,len(Custers)-1)]
                self.Custer.set(custer) # Setting the Customer's driver as the selected driver
            elif self.var5.get() == 0: # If 'var5' is '0', it means drivers are not allowed (Any)
                self.txtCuster.configure(state=DISABLED) # Disable changing drivers
                self.Custer.set("Any") # Setting Customer's driver as "Any"
                custer = "Any" # Setting global driver as "Any"

        #
        # Getting information from CUSTOMER through GUI (Label shows text, Entry requires input)
        #

        # Making a label for 'Firstname' to show User
        self.lblFirstname=Label(CustomerInfo,font=(FONT,14,'bold'),text="Firstname",bd=7)
        self.lblFirstname.grid(row=0,column=0,sticky=W) # Display on GUI at specific location
        # Give empty space and prompt user to enter their first name
        self.txtFirstname=Entry(CustomerInfo,bg = color.white,font=(FONT,14,'bold'),textvariable=self.Firstname,bd=7,insertwidth=2,justify=RIGHT)
        self.txtFirstname.grid(row=0,column=1) # Display on GUI at specific location (in front of 'Firstname' label)

        # Making a label for 'Lastname' to show User
        self.lblLastname=Label(CustomerInfo,font=(FONT,14,'bold'),text="Lastname",bd=7)
        self.lblLastname.grid(row=1,column=0,sticky=W) # Display on GUI at specific location
        # Give empty space and prompt user to enter their last name
        self.txtLastname=Entry(CustomerInfo,bg = color.white,font=(FONT,14,'bold'),textvariable=self.Lastname,bd=7,insertwidth=2,justify=RIGHT)
        self.txtLastname.grid(row=1,column=1,sticky=W) # Display on GUI at specific location (in front of 'Lastname' label)

        # Making a label for 'Address' to show User
        self.lblAddress=Label(CustomerInfo,font=(FONT,14,'bold'),text="Address",bd=7)
        self.lblAddress.grid(row=2,column=0,sticky=W) # Display on GUI at specific location
        # Give empty space and prompt user to enter their address
        self.txtAddress=Entry(CustomerInfo,bg = color.white,font=(FONT,14,'bold'),textvariable=self.Address,bd=7,insertwidth=2,justify=RIGHT)
        self.txtAddress.grid(row=2,column=1) # Display on GUI at specific location (in front of 'Address' label)

        # Making a label for 'Gender' to show User
        self.lblGender=Label(CustomerInfo,font=(FONT,14,'bold'),text="Gender",bd=7)
        self.lblGender.grid(row=3,column=0,sticky=W) # Display on GUI at specific location
        # Give empty space and prompt user to enter their gender
        self.txtGender=Entry(CustomerInfo,bg = color.white,font=(FONT,14,'bold'),textvariable=self.Gender,bd=7,insertwidth=2,justify=RIGHT)
        self.txtGender.grid(row=3,column=1) # Display on GUI at specific location (in front of 'Gender' label)

        # Making a label for 'CNIC' to show User
        self.lblCNIC=Label(CustomerInfo,font=(FONT,14,'bold'),text="CNIC",bd=7)
        self.lblCNIC.grid(row=4,column=0,sticky=W) # Display on GUI at specific location
        # Give empty space and prompt user to enter their CNIC
        self.txtCNIC=Entry(CustomerInfo,bg = color.white,font=(FONT,14,'bold'),textvariable=self.CNIC,bd=7,insertwidth=2,justify=RIGHT)
        self.txtCNIC.grid(row=4,column=1) # Display on GUI at specific location (in front of 'CNIC' label)

        # Making a label for 'PhoneNum' to show User
        self.lblPhoneNum=Label(CustomerInfo,font=(FONT,14,'bold'),text="Phone No#",bd=7)
        self.lblPhoneNum.grid(row=5,column=0,sticky=W) # Display on GUI at specific location
        # Give empty space and prompt user to enter their phone number
        self.txtPhoneNum=Entry(CustomerInfo,bg = color.white,font=(FONT,14,'bold'),textvariable=self.PhoneNum,bd=7,insertwidth=2,justify=RIGHT)
        self.txtPhoneNum.grid(row=5,column=1) # Display on GUI at specific location (in front of 'PhoneNum' label)

        # Making a label for 'Email' to show User
        self.lblEmail=Label(CustomerInfo,font=(FONT,14,'bold'),text="Email",bd=7)
        self.lblEmail.grid(row=6,column=0,sticky=W) # Display on GUI at specific location
        # Give empty space and prompt user to enter their Email
        self.txtEmail=Entry(CustomerInfo,bg = color.white,font=(FONT,14,'bold'),textvariable=self.Email,bd=7,insertwidth=2,justify=RIGHT)
        self.txtEmail.grid(row=6,column=1) # Display on GUI at specific location (in front of 'Email' label)

        if User == "Driver": # If the user is Driveer, ask for Vehicle Number
            # Making a label for 'Email' to show DRIVER
            self.lblLicense=Label(CustomerInfo,font=(FONT,14,'bold'),text="License Num:",bd=7)
            self.lblLicense.grid(row=7,column=0,sticky=W) # Display on GUI at specific location
            # Give empty space and prompt user to enter their Email
            self.txtLicense=Entry(CustomerInfo,bg = color.white,font=(FONT,14,'bold'),textvariable=self.License,bd=7,insertwidth=2,justify=RIGHT)
            self.txtLicense.grid(row=7,column=1) # Display on GUI at specific location (in front of 'License' label)
            rrr = 7 # Row 7 if User is Driver
        else: 
            rrr = 6 # Otherwise normal

        # Making checkbutton to select specific driver or customer
        Custerlbl = "Customer name: " if User == "Driver" else "Driver name, Ride History:"
        # "Checkbutton" gives value '0' when not pressed, and value '1' when pressed
        # In this case, when value is '0', driver is set to 'Any' because nothing is specified
        # Else, when value is '1', a specific customer/driver is selected from the command (Custer()" and list "customers/drivers" to be displayed
        self.chkCuster=Checkbutton(TravelFrame,text=Custerlbl,variable = self.var5,onvalue=1, offvalue=0,font=(FONT,14,'bold'),command=Custerr).grid(row=rrr, column=0, sticky=W)
        # Making a label for 'Custer' to show CUSTOMER
        self.txtCuster=Label(TravelFrame,font=(FONT,14,'bold'),textvariable=self.Custer,bd=6,width=18,bg="white",state= DISABLED,justify=RIGHT,relief=SUNKEN)
        self.txtCuster.grid(row=rrr,column=1) # Display on GUI at specific location (in front of 'Driver/Vehicle' label)

luGG = 0 # Variable in case of no extra luggage (not important)

# Making a class for calculating the fare for the cab (taxi) 
# It defines locations as well as the distance/base fare/total fare (in case of more passengers/extra luggage)
class Payment(MainFramme): # Defining class and inheriting the mainframe
    def __init__(self):
        # Composition of class "VehJorType()" to be used for calculating payment ('Car'/'Bike) || ('Drop Only'/'Drop & return')
        self.VJtype = VehJorType() # in the variable 'VJtype'
        # Composition of class "CustDriv()" to be used for calculating payment (Locations and info given by the User)
        self.CusDri = CustDriv() # in the variable 'CusDri'

        self.PaidFare = StringVar() # Making 'PaidFare' string (base money to be paid)
        self.SubTotal = StringVar() # Making 'Subtotal' string (money after calculating locations/distance)
        self.TotalCost = StringVar() # Making 'TotalCost' string (money after doing all additional calculations)

        self.var1 = IntVar() # Making 'var1' integer, this will be used to determine the base fare.
        # '1' value refers the fare to be enabled, '0' refers to the fare being disabled
        #  CUSTOMER needs to select it everytime

        self.var2 = IntVar() # Making 'var2' integer, this will be used to determine the distance (KMs).
        # '1' value refers to the locations being selected so distance can be calculated, 
        # '0' value refers to the locations not selected, hence no distance will be calculated (Disabled)
        # CUSTOMER needs to select it everytime locations are selected
        
        self.var3 = IntVar() # Making 'var3' integer, this will be used to determine the Luggage.
        # '1' value refers that Extra luggage is selected, '0' refers that Extra luggage isn't selected

        self.locationA=StringVar() # Making 'locationA' string (helper of var2)
        self.locationB=StringVar() # Making 'locationB' string (helper of var2)
        self.paSSengers=StringVar() # Making 'passengers' string to determing amount of passengers
    
        self.CabFare=StringVar() # Making 'CabFare' string (Default Cab Fare)
        self.Km=StringVar() # Making 'Km' string (distance between locations)
        self.Luggage=StringVar() # Making 'Luggage' string (if 'var3' = 1, this is Enabled, else its disabled)

        self.CabFare.set("0") # Setting 'CabFare' as '0' (to keep it disabled at start) || If there's no taxi, why pay money
        self.Km.set("0") # Setting 'Km' as '0' (to keep it disabled at start) || If there's no location, why is there any distance
        self.Luggage.set("0") # Setting 'Luggage' as '0'

        # Defining 'Cost Frame', a sub-frame of 'FrameDetails', 
        # It contains all information regarding payment (basefare/subtotal/total)
        CostFrame = LabelFrame(FrameDetails,width=150,height=150,bd=5,relief=FLAT)
        CostFrame.grid(row=1,column=1) # Displaying on GUI at specific place
    
        # Cab Fare method to set up base fare for any Cab (Each Cab ride is worth Rs 50 no matter what)
        def Cab_Fare(): 
            global Item1 # Globalizing variable (Base fee for Cab)
            if self.var1.get() == 1: # If value of 'var1' is '1'
                self.txtCabFare.configure(state = NORMAL) # Base cab fare is Enabled
                Item1=float(50) # Value is set to Rs 50.0
                self.CabFare.set("Rs " + str(Item1)) # Value is shown to customer on GUI
            elif self.var1.get() == 0: # If value of 'var1' is '0'
                self.txtCabFare.configure(state=DISABLED) # Base cab fare is Disabled (No Fare -> No Cab -> No Program)
                self.CabFare.set("0") # Value is set to 0, and shown to customer on GUI
                Item1=0 # Variable is reset
        
        def Kilo(): # Gets 'Kilometer' distance between locationA and locationB
            ''' 
            All 16 Locations:
            Hope Tower, Hostel, FC Univ, FC College, Wahdat Colony, Emporium
            Bahriya Town, Garden Town, Johar Town, Airport, Metro Station,
            Daewoo Station, DHA Phase 1, DHA Phase 2, DHA Phase 3, Kadafi Stadium
            '''
            if self.var2.get() == 0: # If value of 'var2' is 0 and locations are blank
                self.txtKm.configure(state=DISABLED) # Distance/Locations are Disabled (No Locations -> No Distance -> No Program)
                self.Km.set("0") # Set distance to 0
            # if 'var2' is '1' and locations are defined
            elif self.var2.get() == 1 and self.locationA.get() != "" and self.locationB.get() != "": 
                self.txtKm.configure(state=NORMAL) # Distance/Locations are Enabled
                '''
                For each if/elif statement below, 
                var1 is defined as the locationA (The pick-up point)
                var2 is defined as the locationB (The drop-off point)
                Searches for distance between that locationA to locationB
                and then gives it to the program
                Example is given in first statement
                '''
                if self.locationA.get() == "Hope Tower": # If locationA is 'Hope Tower'
                    # Uses 'switch' dictionary to provide distance (answer), depending on the locationB (key)
                    switch ={"Hope Tower":     0, "Hostel":       2, "FC Univ":        3, "FC College":      4,
                             "Wahdat Colony":  5, "Emporium":    10, "Bahriya Town":  20, "Garden Town":    11,
                             "Johar Town":    15, "Airport":     25, "Metro Station": 12, "Daewoo Station": 16,
                             "DHA Phase 1":   30, "DHA Phase 2": 32, "DHA Phase 3":   34, "Kadafi Stadium":  4}
                    # Depending on locationB, distance is given (I.E locationB is Emporium, distance is 10)
                    self.Km.set(switch[self.locationB.get()]) # Sets the distance to the KM variable from dictionary
                elif self.locationA.get() == "Hostel":
                    switch ={"Hope Tower":     2, "Hostel":       0, "FC Univ":        4, "FC College":      5,
                             "Wahdat Colony":  6, "Emporium":    11, "Bahriya Town":  21, "Garden Town":    12,
                             "Johar Town":    16, "Airport":     26, "Metro Station": 13, "Daewoo Station": 17,
                             "DHA Phase 1":   31, "DHA Phase 2": 33, "DHA Phase 3":   35, "Kadafi Stadium":  5}
                    self.Km.set(switch[self.locationB.get()])
                elif self.locationA.get() == "FC Univ":
                    switch ={"Hope Tower":     3, "Hostel":       4, "FC Univ":        0, "FC College":      2,
                             "Wahdat Colony":  7, "Emporium":    12, "Bahriya Town":  22, "Garden Town":    13,
                             "Johar Town":    17, "Airport":     26, "Metro Station": 14, "Daewoo Station": 18,
                             "DHA Phase 1":   32, "DHA Phase 2": 34, "DHA Phase 3":   36, "Kadafi Stadium":  6}
                    self.Km.set(switch[self.locationB.get()])
                elif self.locationA.get() == "FC College":
                    switch ={"Hope Tower":     2, "Hostel":       3, "FC Univ":        4, "FC College":      0,
                             "Wahdat Colony":  6, "Emporium":    11, "Bahriya Town":  21, "Garden Town":    12,
                             "Johar Town":    16, "Airport":     26, "Metro Station": 13, "Daewoo Station": 17,
                             "DHA Phase 1":   31, "DHA Phase 2": 33, "DHA Phase 3":   35, "Kadafi Stadium":  5}
                    self.Km.set(switch[self.locationB.get()])
                elif self.locationA.get() == "Wahdat Colony":
                    switch ={"Hope Tower":     5, "Hostel":       6, "FC Univ":        7, "FC College":      8,
                             "Wahdat Colony":  0, "Emporium":    20, "Bahriya Town":  25, "Garden Town":    12,
                             "Johar Town":    15, "Airport":     23, "Metro Station":  7, "Daewoo Station": 15,
                             "DHA Phase 1":   32, "DHA Phase 2": 34, "DHA Phase 3":   36, "Kadafi Stadium":  9}
                    self.Km.set(switch[self.locationB.get()])
                elif self.locationA.get() == "Emporium":
                    switch ={"Hope Tower":    12, "Hostel":      13, "FC Univ":       14, "FC College":     15,
                             "Wahdat Colony": 20, "Emporium":     0, "Bahriya Town":  12, "Garden Town":    22,
                             "Johar Town":    15, "Airport":     30, "Metro Station": 22, "Daewoo Station": 24,
                             "DHA Phase 1":   40, "DHA Phase 2": 42, "DHA Phase 3":   44, "Kadafi Stadium": 15}
                    self.Km.set(switch[self.locationB.get()])
                elif self.locationA.get() == "Bahriya Town":
                    switch ={"Hope Tower":    20, "Hostel":      21, "FC Univ":       22, "FC College":     23,
                             "Wahdat Colony": 25, "Emporium":    12, "Bahriya Town":   0, "Garden Town":    24,
                             "Johar Town":     7, "Airport":     10, "Metro Station": 26, "Daewoo Station": 15,
                             "DHA Phase 1":   24, "DHA Phase 2": 26, "DHA Phase 3":   28, "Kadafi Stadium": 25}
                    self.Km.set(switch[self.locationB.get()])
                elif self.locationA.get() == "Garden Town":
                    switch ={"Hope Tower":    11, "Hostel":      12, "FC Univ":       13, "FC College":     14,
                             "Wahdat Colony": 12, "Emporium":    22, "Bahriya Town":  24, "Garden Town":     0,
                             "Johar Town":    16, "Airport":     24, "Metro Station":  8, "Daewoo Station": 16,
                             "DHA Phase 1":   33, "DHA Phase 2": 35, "DHA Phase 3":   36, "Kadafi Stadium": 10}
                    self.Km.set(switch[self.locationB.get()])
                elif self.locationA.get() == "Johar Town":
                    switch ={"Hope Tower":    15, "Hostel":      16, "FC Univ":       17, "FC College":     18,
                             "Wahdat Colony": 15, "Emporium":    15, "Bahriya Town":   8, "Garden Town":    16,
                             "Johar Town":     0, "Airport":     18, "Metro Station": 20, "Daewoo Station": 18,
                             "DHA Phase 1":   26, "DHA Phase 2": 28, "DHA Phase 3":   30, "Kadafi Stadium": 16}
                    self.Km.set(switch[self.locationB.get()])
                elif self.locationA.get() == "Airport":
                    switch ={"Hope Tower":    25, "Hostel":      26, "FC Univ":       27, "FC College":     28,
                             "Wahdat Colony": 23, "Emporium":    30, "Bahriya Town":  10, "Garden Town":    24,
                             "Johar Town":    18, "Airport":      0, "Metro Station": 25, "Daewoo Station": 6,
                             "DHA Phase 1":   20, "DHA Phase 2": 24, "DHA Phase 3":   26, "Kadafi Stadium": 24}
                    self.Km.set(switch[self.locationB.get()])
                elif self.locationA.get() == "Metro Station":
                    switch ={"Hope Tower":    12, "Hostel":      13, "FC Univ":       14, "FC College":     15,
                             "Wahdat Colony":  7, "Emporium":    22, "Bahriya Town":  26, "Garden Town":     8,
                             "Johar Town":    20, "Airport":     25, "Metro Station":  0, "Daewoo Station": 19,
                             "DHA Phase 1":   34, "DHA Phase 2": 36, "DHA Phase 3":   38, "Kadafi Stadium": 15}
                    self.Km.set(switch[self.locationB.get()])
                elif self.locationA.get() == "Daewoo Station":
                    switch ={"Hope Tower":    16, "Hostel":      17, "FC Univ":       18, "FC College":     19,
                             "Wahdat Colony": 15, "Emporium":    24, "Bahriya Town":  15, "Garden Town":    17,
                             "Johar Town":    18, "Airport":      8, "Metro Station": 19, "Daewoo Station":  0,
                             "DHA Phase 1":   22, "DHA Phase 2": 24, "DHA Phase 3":   26, "Kadafi Stadium": 18}
                    self.Km.set(switch[self.locationB.get()])
                elif self.locationA.get() == "DHA Phase 1":
                    switch ={"Hope Tower":    30, "Hostel":      31, "FC Univ":       32, "FC College":     33,
                             "Wahdat Colony": 32, "Emporium":    40, "Bahriya Town":  24, "Garden Town":    33,
                             "Johar Town":    26, "Airport":      7, "Metro Station": 34, "Daewoo Station": 22,
                             "DHA Phase 1":    0, "DHA Phase 2":  2, "DHA Phase 3":    4, "Kadafi Stadium": 32}
                    self.Km.set(switch[self.locationB.get()])
                elif self.locationA.get() == "DHA Phase 2":
                    switch ={"Hope Tower":    32, "Hostel":      33, "FC Univ":       34, "FC College":     35,
                             "Wahdat Colony": 34, "Emporium":    42, "Bahriya Town":  26, "Garden Town":    35,
                             "Johar Town":    28, "Airport":      9, "Metro Station": 36, "Daewoo Station": 24,
                             "DHA Phase 1":    2, "DHA Phase 2":  0, "DHA Phase 3":    2, "Kadafi Stadium": 34}
                    self.Km.set(switch[self.locationB.get()])
                elif self.locationA.get() == "DHA Phase 3":
                    switch ={"Hope Tower":    34, "Hostel":      35, "FC Univ":       36, "FC College":     37,
                             "Wahdat Colony": 36, "Emporium":    44, "Bahriya Town":  28, "Garden Town":    37,
                             "Johar Town":    30, "Airport":     11, "Metro Station": 38, "Daewoo Station": 26,
                             "DHA Phase 1":    4, "DHA Phase 2":  2, "DHA Phase 3":    0, "Kadafi Stadium": 36}
                    self.Km.set(switch[self.locationB.get()])
                elif self.locationA.get() == "Hope Tower":
                    switch ={"Hope Tower":     5, "Hostel":       5, "FC Univ":        5, "FC College":      6,
                             "Wahdat Colony":  9, "Emporium":    15, "Bahriya Town":  25, "Garden Town":    10,
                             "Johar Town":    16, "Airport":     24, "Metro Station": 15, "Daewoo Station": 18,
                             "DHA Phase 1":   32, "DHA Phase 2": 34, "DHA Phase 3":   36, "Kadafi Stadium":  0}
                    self.Km.set(switch[self.locationB.get()])

        # Gets Luggage in case Extra luggage is selected
        def Lug():
            global luGG # Globalizing Variable
            if (self.var3.get()==1): # If 'var3' is '1'
                self.txtLuggage.configure(state = NORMAL) # Extra Luggage is Enabled
                luGG=float(30) # Fare for Extra Luggage is assigned
                self.Luggage.set("Rs "+ str(luGG)) # Fare for Extra Luggage is shown to customer
            elif self.var3.get()== 0: # If 'var3' is '0'
                self.txtLuggage.configure(state = DISABLED) # Extra Luggage is Disabled
                self.Luggage.set("0") # Fare for Extra luggage is made 0 and shown to customer
                luGG=0 # Variable is reset

        #
        # Displaying Payment information on GUI
        #

        # Making a label for 'Paid Fare' to show CUSTOMER
        self.lblPaidFare = Label(CostFrame,font=(FONT,14,'bold'),text="Paid Fare\t\t",bd=7)
        self.lblPaidFare.grid(row=0,column=2,sticky=W) # Display on GUI at specific location
        # Making a label for the calculated fare to show CUSTOMER
        self.txtPaidFare = Label(CostFrame,font=(FONT,14,'bold'),textvariable=self.PaidFare,bd=7, width=26, justify=RIGHT,bg="white",relief=SUNKEN)
        self.txtPaidFare.grid(row=0,column=3) # Display on GUI at specific location (in front of 'Paid Fare' label)

        # Making a label for 'Sub total' to show CUSTOMER    
        self.lblSubTotal=Label(CostFrame,font=(FONT,14,'bold'),text="Sub Total",bd=7)
        self.lblSubTotal.grid(row=1,column=2,sticky=W) # Display on GUI at specific location
        # Making a label for the calculated subtotal to show CUSTOMER
        self.txtSubTotal = Label(CostFrame,font=(FONT,14,'bold'),textvariable=self.SubTotal,bd=7, width=26, justify=RIGHT,bg="white",relief=SUNKEN)
        self.txtSubTotal.grid(row=1,column=3) # Display on GUI at specific location (in front of 'Sub total' label)

        # Making a label for 'Total' to show CUSTOMER
        self.lblTotalCost=Label(CostFrame,font=(FONT,14,'bold'),text="Total Cost",bd=7)
        self.lblTotalCost.grid(row=2,column=2,sticky=W) # Display on GUI at specific location
        # Making a label for the calculated total amount to show CUSTOMER
        self.txtTotalCost = Label(CostFrame,font=(FONT,14,'bold'),textvariable=self.TotalCost,bd=7, width=26, justify=RIGHT,bg="white",relief=SUNKEN)
        self.txtTotalCost.grid(row=2,column=3) # Display on GUI at specific location (in front of 'total' label)
        
        #
        # Location information
        #
        
        # If the user is driver, the location information is not selected by them, so assining random (from company)
        if User == "Driver":
            # Defining Labels
            # Making a label for "Pick up from" window to show DRIVER
            self.txtPickk=Label(TravelFrame,font=(FONT,14,'bold'),text="Pick up from:",bd=7)
            self.txtPickk.grid(row=1,column=0,sticky=W) # Display on GUI at specific location
            # Making a label for the Pick Up location for driver chosen previously
            self.lblPickk=Label(TravelFrame, bg=color.white, font=(FONT,14,'bold'),text=self.locationA.get(),bd=7)
            self.lblPickk.grid(row=1,column=1,sticky=W) # Display on GUI at specific location

            # Making a label for "Drop at" window to show CUSTOMER
            self.txtDrop=Label(TravelFrame,font=(FONT,14,'bold'),text="Drop at:",bd=7)
            self.txtDrop.grid(row=2,column=0,sticky=W) # Display on GUI at specific location 
            # Making a label for the Pick Up location for driver chosen previously
            self.lblDrop=Label(TravelFrame, bg=color.white, font=(FONT,14,'bold'),text=self.locationB.get(),bd=7)
            self.lblDrop.grid(row=2,column=1,sticky=W) # Display on GUI at specific location

            # Making a label for amount of 'Passengers' window to show CUSTOMER
            self.txtPassengers=Label(TravelFrame,font=(FONT,14,'bold'),text="Passengers",bd=7)
            self.txtPassengers.grid(row=3,column=0,sticky=W) # Display on GUI at specific location
            # Making a label for the Pick Up location for driver chosen previously
            self.lblPassengers=Label(TravelFrame,bg=color.white,font=(FONT,14,'bold'),text=self.paSSengers.get(),bd=7)
            self.lblPassengers.grid(row=3,column=1,sticky=W) # Display on GUI at specific location

            # Getting Random Customer Info
            def RandomCust():
                # Cleaning workspace for new inputs
                self.lblPickk.grid_remove()
                self.lblDrop.grid_remove()
                self.lblPassengers.grid_remove()
                # Getting All locations then returning from a user
                Locations = ['Hope Tower','Hostel','FC Univ','FC College','Wahdat Colony',"Emporium","Bahriya Town","Garden Town","Johar Town","Airport","Metro Station","Daewoo Station","DHA Phase 1","DHA Phase 2","DHA Phase 3","Kadafi Stadium"]
                Pickk = Locations[random.randint(0,len(Locations)-1)] # Get Pick point 
                Locations.remove(Pickk) # Remove Pick point as destination
                Dropp = Locations[random.randint(0,len(Locations)-1)] # Get Drop point
                nPass = str(random.randint(1,4)) # Get Amount of passengers
                # Set in the defined variables
                self.locationA.set(Pickk)
                self.locationB.set(Dropp)
                self.paSSengers.set(nPass)

                # Update Customer Info per Button Clear (REPEATED COMMANDS)
                self.lblPickk=Label(TravelFrame, bg=color.white, font=(FONT,14,'bold'),text=self.locationA.get(),bd=7)
                self.lblPickk.grid(row=1,column=1,sticky=W) # Display on GUI at specific location
                self.lblDrop=Label(TravelFrame, bg=color.white, font=(FONT,14,'bold'),text=self.locationB.get(),bd=7)
                self.lblDrop.grid(row=2,column=1,sticky=W) # Display on GUI at specific location
                self.lblPassengers=Label(TravelFrame,bg=color.white,font=(FONT,14,'bold'),text=self.paSSengers.get(),bd=7)
                self.lblPassengers.grid(row=3,column=1,sticky=W) # Display on GUI at specific location

            Button(TravelFrame,padx=50,bd=7,font=(FONT,14,BOLD),width = 2,text='Get Customer',command=RandomCust).grid(row=0,column=1)

            # Button(TravelFrame,text = 'Get Customer',bd = 3 ,font = ('',15),padx=5,pady=5,command=RandomCust).grid(row=0,column=1) # Using command 'signup'

            
        if User == "Customer":
            # Making a label for "Pick up from" window to show CUSTOMER
            self.lblPickk=Label(TravelFrame,font=(FONT,14,'bold'),text="Pick up from:",bd=7)
            self.lblPickk.grid(row=0,column=0,sticky=W) # Display on GUI at specific location
            # Making a drop-down menu (a.k.a ttk.Combobox) which defines the string 'locationA'
            self.cboPickk =ttk.Combobox(TravelFrame, textvariable = self.locationA , state='readonly', font=(FONT,20,'bold'), width=14)
            # Locations that can be selected for locationA
            self.cboPickk['value']=('','Hope Tower','Hostel','FC Univ','FC College','Wahdat Colony',"Emporium","Bahriya Town","Garden Town","Johar Town","Airport","Metro Station","Daewoo Station","DHA Phase 1","DHA Phase 2","DHA Phase 3","Kadafi Stadium")
            self.cboPickk.current(0) # Set default location as empty (So CUSTOMER can choose their own)
            self.cboPickk.grid(row=0,column=1) # Display on GUI at specific location (in front of 'Pick up from' label)
            # Making a label for "Drop at" window to show CUSTOMER
            self.lblDrop=Label(TravelFrame,font=(FONT,14,'bold'),text="Drop at:",bd=7)
            self.lblDrop.grid(row=1,column=0,sticky=W) # Display on GUI at specific location 
            # Making a drop-down menu (a.k.a ttk.Combobox) which defines the string 'locationB'
            self.cboDrop =ttk.Combobox(TravelFrame, textvariable = self.locationB , state='readonly', font=(FONT,20,'bold'), width=14)
            # Locations that can be selected for locationB
            self.cboDrop['value']=('','Hope Tower','Hostel','FC Univ','FC College','Wahdat Colony',"Emporium","Bahriya Town","Garden Town","Johar Town","Airport","Metro Station","Daewoo Station","DHA Phase 1","DHA Phase 2","DHA Phase 3","Kadafi Stadium")
            self.cboDrop.current(0) # Set default location as empty (So CUSTOMER can choose their own)
            self.cboDrop.grid(row=1,column=1)  # Display on GUI at specific location (in front of 'Drop at' label)

            # Making a label for amount of 'Passengers' window to show CUSTOMER
            self.lblPassengers=Label(TravelFrame,font=(FONT,14,'bold'),text="Passengers",bd=7)
            self.lblPassengers.grid(row=2,column=0,sticky=W) # Display on GUI at specific location
            # Making a drop-down menu (a.k.a ttk.Combobox) which defines the string 'paSSengers'
            self.cboPassengers =ttk.Combobox(TravelFrame, textvariable = self.paSSengers , state='readonly', font=(FONT,20,'bold'), width=14)
            self.cboPassengers['value']=('','1','2','3','4') # Amount of passengers that can be selected
            self.cboPassengers.current(1) # Set default amount of passengers as '1'
            self.cboPassengers.grid(row=2,column=1) # Display on GUI at specific location (in front of 'Passengers' label)

        #    
        # Buttons to calculate payment by the customer's instruction.
        #
        
        # rrr = Row number (One more in case of Driver)
        if User == "Customer":
            rrr = 3
        elif User == "Driver":
            rrr = 4

        # Making a Button for 'var1', if checked value is '1', if unchecked value is '0'
        self.chkCabFare=Checkbutton(TravelFrame,text="Cab Fare (Base Charge)*: ",variable = self.var1, onvalue=1, offvalue=0,font=(FONT,16,'bold'),command=Cab_Fare).grid(row=rrr, column=0, sticky=W)
        # Making a label for "Cab Fare" to show CUSTOMER
        self.txtCabFare=Label(TravelFrame,font=(FONT,14,'bold'),textvariable=self.CabFare,bd=6,width=18,bg="white",state= DISABLED,justify=RIGHT,relief=SUNKEN)
        self.txtCabFare.grid(row=rrr,column=1) # Display on GUI at specific location (in front of 'Cab Fare' button)

        # Making a Button for 'var2', if checked value is '1', if unchecked value is '0'
        self.chkKm=Checkbutton(TravelFrame,text="Distance (KMs)*: ",variable = self.var2, onvalue=1, offvalue=0,font=(FONT,16,'bold'),command=Kilo).grid(row=rrr+1, column=0, sticky=W)
        # Making a label for 'KMs' (Distance) to show CUSTOMER
        self.txtKm=Label(TravelFrame,font=(FONT,14,'bold'),textvariable=self.Km,bd=6,width=18,bg="white",state= DISABLED,justify=RIGHT,relief=SUNKEN,highlightthickness=0)
        self.txtKm.grid(row=rrr+1,column=1) # Display on GUI at specific location (in front of 'KMs' (Distance) button)
    
        AE_Luggage = "Extra Luggage:" if User == "Customer" else "Allow Luggage?:"
        # Making a Button for 'var3', if checked value is '1', if unchecked value is '0'
        self.chkLuggage=Checkbutton(TravelFrame,text=AE_Luggage,variable = self.var3, onvalue=1, offvalue=0,font=(FONT,16,'bold'),command=Lug).grid(row=rrr+2, column=0, sticky=W)
        # Making a label for 'Luggage' to show CUSTOMER
        self.txtLuggage=Label(TravelFrame,font=(FONT,14,'bold'),textvariable=self.Luggage,bd=6,width=18,bg="white",state= DISABLED,justify=RIGHT,relief=SUNKEN)
        self.txtLuggage.grid(row=rrr+2,column=1) # Display on GUI at specific location (in front of 'Luggage' button)

custer = "Any" # Pre-define driver as "Any" if customer never asks for one

# Making a class Information which will gather information and data used thoughout the program
# It will gather and enable the CUSTOMER to make Reciepts/Logs for the Cab bookings
# After Initial Login is successful this class is called, which imports information from every other class (directly/indirectly)
class Information: # Main class which will gather information from everywhere else to make the Window
    def __init__(self,root): # Same root as defined in the driver (end of code)
        self.root = root # Window
        self.root.title("Cab booking system") # Title of Window
        self.root.geometry(geometry) # Size of Window
        self.root['background']='#856ff8' # Color of Window (Hex-Code)

        # Composition of class "MainFrame()" to be used for using and implementing functions on the Main Window
        self.mainfrrame = MainFramme() # In the variable 'mainfrrame'
        # Composition of class "Payment()" to be used for indirectly getting other composited classes and calculations
        self.payment = Payment() # In the variable 'payment'

        DateofOrder = StringVar() # Making 'Date of Booking' string
        DateofOrder.set(time.strftime("%d / %m / %Y ")) # Setting current date as the date of booking
        ReceiptNum = StringVar() # Making 'Reciept' string (Will contain all reciept information)
        reset_counter = 0 # In case of resetting all data 
        Receipt=StringVar() # Making "Reciept" string (in case if its needed)

        #
        # Instructions
        #

        # Defining 'InsFrame', a sub-frame of 'FrameDetails', 
        # It contains all Instructions on the GUI 
        InsFrame = LabelFrame(FrameDetails,bd=10, width=300,height=250, font=(FONT,12,'bold'),text="Instructions", relief=RIDGE)
        InsFrame.grid(row=0,column=2) # Displaying on GUI at a specific location
        # Making a multi-line-string of instructions
        if User == "Customer":
            Instructions = "Steps:\n1) Enter all the details in the customer info\n2) Select locations and passengers (1-4)\n3) Select type of vehicle (Car or Bike)\n4) Select type of travel (Pick only/Both)\n5) Tick unmarked boxes to get data on'em\n6) Extra Luggage is an optional property\n7) Checking driver name defines unique\ndrivers everytime its clicked\n8) 'Export' to export data to text file\n9) Use buttons under reciept to perform\ntasks, Total calculates details for Fare"
        elif User == "Driver":
            Instructions = "Steps:\n1) Enter all the details in the driver info\n2) Select type of vehicle (Car or Bike)\n3) Allow type of travel (Pick only/Both)\n4) 'Get Customer' to get locations/passengers\n5) Tick unmarked boxes to get data on'em\n6) Allow/Disallow Extra Luggage (optional)\n7) Checking customer name defines unique\ncustomerss everytime its clicked\n8) 'Export' to export data to text file\n9) Use buttons under reciept to perform\ntasks, Total calculates details for Fare"
        """ The Instructions
                        FOR CUSTOMER                                          FOR DRIVER
        Steps:                                              Steps:
            1) Enter all the details in customer info             1) Enter all the details in the driver info
            2) Select locations and passengers (1-4)              2) Select type of vehicle (Car or Bike)
            3) Select type of vehicle (Car or Bike)               3) Allow type of travel (Pick only/Both)
            4) Select type of travel (Pick only/Both)             4) 'Get Customer' to get locations/passengers
            5) Tick unmarked boxes to get data on'em              5) Tick unmarked boxes to get data on'em
            6) Extra Luggage is an optional property              6) Allow/Disallow Extra Luggage (optional)
            7) Checking driver/customer defines unique            7) Checking customer name defines unique
               drivers/vehicles everytime its used                   customerss everytime its clicked
            8) "Export" to export data to text file               8) 'Export' to export data to text file
            9) Use buttons under reciept to perform               9) Use buttons under reciept to perform
               tasks, Total calculates details for Fare              tasks, Total calculates details for Fare
        """        

        # Making a label for "Instructions" to show User
        self.lblInst=Label(InsFrame,font=(FONT,13,'bold'),text=Instructions,bd=7)
        self.lblInst.grid(row=0,column=0,sticky=W) # Displaying on GUI at a specific location

        # Extremely important method
        # Grabs the data from everywhere and stores it in one list for future use
        def update_data(): # Updates whenever it is called
        # Getting information from inheritted/associated classes and self to use for calculations
        # Making a list 'datta' to store all data, then will be used to display further
            global datta # Globalizing the list
            randomRef=random.randint(10853,500831) # Random numbers (Showing the number of reciept)
            ReceiptNum.set(str(randomRef)) # Setting the variable "Reciept" to that random number (after converting it to a string)

            # In the list, the data written inside strings "" is constant, it will always remain same. 
            # "\n" is forcing it to go to the next line
            datta = ["Receipt No#:\n",                            # Index 0 
                      ReceiptNum.get() + "\n",                    # Index 1  || Getting the 'Reciept Number' from self class (itself)
                     "Date:\n",                                   # Index 2
                      DateofOrder.get() + "\n",                   # Index 3  || Getting the 'Date of Order' from self class (itself)
                     f"{User} name:\n",                           # Index 4
                      custer+"\n",                                # Index 5  || Getting the 'Driver' (Globalized)
                     "Firstname:\n",                              # Index 6
                      self.payment.CusDri.Firstname.get() + "\n", # Index 7  || Getting the 'Firstname' from self -> Payment -> CustDriv class
                     "Lastname:\n",                               # Index 8 
                      self.payment.CusDri.Lastname.get() + "\n",  # Index 9  || Getting the 'Lastname' from self -> Payment -> CustDriv class
                     "Address:\n",                                # Index 10
                      self.payment.CusDri.Address.get() + "\n",   # Index 11 || Getting the 'Address' from self -> Payment -> CustDriv class
                     "Gender:\n",                                 # Index 12
                      self.payment.CusDri.Gender.get() + "\n",    # Index 13 || Getting the 'Gender' from self -> Payment -> CustDriv class
                     "CNIC:\n",                                   # Index 14
                      self.payment.CusDri.CNIC.get() + "\n",      # Index 15 || Getting the 'CNIC' from self -> Payment -> CustDriv class
                     "PhoneNum:\n",                               # Index 16
                      self.payment.CusDri.PhoneNum.get() + "\n",  # Index 17 || Getting the 'PhoneNum' from self -> Payment -> CustDriv class
                     "Email:\n",                                  # Index 18
                      self.payment.CusDri.Email.get() + "\n",     # Index 19 || Getting the 'Email' from self -> Payment -> CustDriv class
                     "From:\n",                                   # Index 20
                      self.payment.locationA.get() + "\n",        # Index 21 || Getting the 'locationA' from self -> Payment class
                     "To:\n",                                     # Index 22
                      self.payment.locationB.get() + "\n",        # Index 23 || Getting the 'locationB' from self -> Payment class
                     "Passengers:\n",                             # Index 24
                      self.payment.paSSengers.get() + "\n",       # Index 25 || Getting the 'passengers' from self -> Payment class
                     "Bike:\n",                                   # Index 26
                      self.payment.VJtype.Bike.get() + "\n",      # Index 27 || Getting the 'Bike' from self -> Payment -> VehJorType class
                     "Car:\n",                                    # Index 28
                      self.payment.VJtype.Car.get() + "\n",       # Index 29 || Getting the 'Car' from self -> Payment -> VehJorType class
                     "Paid:\n",                                   # Index 30
                      self.payment.PaidFare.get() + "\n",         # Index 31 || Getting the 'PaidFare' from self -> Payment class
                     "SubTotal:\n",                               # Index 32
                      str(self.payment.SubTotal.get()) + "\n",    # Index 33 || Getting the 'Subtotal' from self -> Payment class
                     "Total Cost:\n",                             # Index 34
                      str(self.payment.TotalCost.get())]          # Index 35 || Getting the 'Total' from self -> Payment class
                                        
        #
        # Main Buttons/Functions
        #
        
        # Calculate the total payment by getting values from 'payment' composited class
        '''
        Explaination:
        # Calculate base fare, reduce it to 2 decimal points, convert to string and store in "Fare"
        Fare     = "Rs " + str('%.2f'%((Cost_of_fare)*0.09)) 
        # Reduce fare to 2 decimal points, convert to string and store in "SUBTOTAL"              
        SUBTOTAL = "Rs " + str('%.2f'%((Cost_of_fare)))  
        # Get total fare adding 'Fare' and 'SUBTOTAL', reduce to 2 decimal point, convert to string and store in "TOTAL" (Total)                  
        TOTAL    = "Rs " + str('%.2f'%(Cost_of_fare+((Cost_of_fare)*0.9))) 
        '''
        def Total_Paid():
            # If 'var1' is '1' AND 'var2' is '1' OR 'var3' is 1 
            # Meaning if 'CabFair (var1) is selected' and 'Distance (var2) is calculated' or 'Luggage (var3) is selected' [Luggage is optional]
            # AND cartype/journeytype/locations are defined THEN proceed
            if ((self.payment.var1.get() == 1 and self.payment.var2.get() == 1 or self.payment.var3.get() == 1) and self.payment.VJtype.carType.get() != 0 and self.payment.VJtype.journeyType.get() != 0 and (self.payment.locationA.get() != "" and self.payment.locationB.get() !="")):
                if self.payment.VJtype.journeyType.get()==1: # If 'journeyType' is '1' [Drop only]
                    Item2 = self.payment.Km.get() # Store the distance in 'Item2'
                    Cost_of_fare = (Item1+(float(Item2)*Item5)+luGG) # Calculate Cost [Base Money + Distance * VehicleTypePrice + Luggage]
                    Fare = "Rs " + str('%.2f'%((Cost_of_fare)*0.09))
                    SUBTOTAL = "Rs " + str('%.2f'%((Cost_of_fare)))
                    TOTAL = "Rs " + str('%.2f'%(Cost_of_fare+((Cost_of_fare)*0.9)))
                elif self.payment.VJtype.journeyType.get()==2: # If 'journeyType' is '2' [Drop and Return]
                    Item2 = self.payment.Km.get() # Store the distance in 'Item2'
                    Cost_of_fare = (Item1+(float(Item2)*Item5)*1.5+luGG) # Same as previous but 1.5 times the price (due to two round trip)
                    Fare = "Rs " + str('%.2f'%((Cost_of_fare) *0.09)) 
                    SUBTOTAL = "Rs " + str('%.2f'%((Cost_of_fare)))
                    TOTAL = "Rs " + str('%.2f'%(Cost_of_fare+((Cost_of_fare)*0.9)))
                else:
                    Item2 = self.payment.Km.get() # Store the distance in 'Item2'
                    Cost_of_fare = (Item1+(float(Item2)*Item5)*2+luGG) # Same as previous but 2 times the price 
                    Fare = "Rs " + str('%.2f'%((Cost_of_fare) *0.09))
                    SUBTOTAL = "Rs " + str('%.2f'%((Cost_of_fare)))
                    TOTAL = "Rs " + str('%.2f'%(Cost_of_fare+((Cost_of_fare)*0.9)))

                self.payment.PaidFare.set(Fare) # Set the Fare to be used by GUI
                self.payment.SubTotal.set(SUBTOTAL) # Set the Subtotal to be used by GUI
                self.payment.TotalCost.set(TOTAL) # Set the Total to be used by GUI
            else: # If the initial "IF statment" doesn't work, there must be some empty input, then-
                w = ms.showwarning("Error !","Invalid Input\nPlease try again !!!") # Show Error
        
        def iExit(): # Exit function, to exit the application
            iExit = ms.askyesno("Prompt!","Do you want to exit?") # Returns value '0' if 'yes', and '1' if 'no
            if iExit > 0: # If 'yes' 
                root.destroy() # Destroy the GUI, exitting the program
                return

        def Reset(): # Reset function
            # Reset all variables changed by the CUSTOMER to their initial state (Like they were just created)
            self.payment.CabFare.set("0") # Resetting Fare
            self.payment.Km.set("0") # Resetting Distance
            self.payment.Luggage.set("0") # Resetting Luggage
            self.payment.CusDri.Custer.set("Any") # Resetting Drivers

            self.payment.VJtype.Bike.set("0") # Resetting Bikes
            self.payment.VJtype.Car.set("0") # Resetting Cars

            self.payment.CusDri.Firstname.set("") # Resetting Firstname
            self.payment.CusDri.Lastname.set("") # Resetting Lastname
            self.payment.CusDri.Address.set("") # Resetting Address
            self.payment.CusDri.Gender.set("") # Resetting Gender
            self.payment.CusDri.PhoneNum.set("") # Resetting PhoneNum
            self.payment.CusDri.CNIC.set("") # Resetting CNIC
            self.payment.CusDri.Email.set("") # Resetting Email

            self.payment.PaidFare.set("") # Resetting PaidFare
            self.payment.SubTotal.set("") # Resetting SubTotal
            self.payment.TotalCost.set("") # Resetting Total
            # Resetting the Reciept (to blank)
            self.txtReceipt1.delete("1.0",END) # Constants
            self.txtReceipt2.delete("1.0",END) # Variables
            
            self.payment.var1.set(0) # Resettong var1
            self.payment.var2.set(0) # Resetting var2
            self.payment.var3.set(0) # Resetting var3
            self.payment.locationA.set("0") # Resetting locationA
            self.payment.locationB.set("0") # Resetting locationB
            self.payment.paSSengers.set("0") # Resetting passengers

            self.payment.cboPickk.current(0) # Resetting Pick up point
            self.payment.cboDrop.current(0) # Resetting Drop off point
            self.payment.cboPassengers.current(0) # Resetting number of passengers

            # Disabling use of given variables
            self.payment.txtCabFare.configure(state=DISABLED) # Fare
            self.payment.txtKm.configure(state=DISABLED) # Locations
            self.payment.txtLuggage.configure(state=DISABLED) # Luggage
            self.payment.CusDri.txtCuster.configure(state=DISABLED) # Driver
            self.payment.VJtype.txtBike.configure(state=DISABLED) # Bike
            self.payment.VJtype.txtCar.configure(state=DISABLED) # Car

            self.reset_counter=1 # To show successfully reset.

        # Function for writing on Reciept
        def Receiptt():
            # Checking if all the information/variables/data is given before writing reciept
            if reset_counter == 0 and self.payment.CusDri.Firstname.get()!="" and self.payment.CusDri.Lastname.get()!="" and self.payment.CusDri.Address.get()!="" and self.payment.CusDri.Gender.get()!="" and self.payment.CusDri.PhoneNum.get()!="" and self.payment.CusDri.CNIC.get()!="" and self.payment.CusDri.Email.get()!="":
                # Cleaning Reciept
                self.txtReceipt1.delete("1.0",END) # Constants
                self.txtReceipt2.delete("1.0",END) # Variables
                # Exporting all data from program to GUI and displaying.
                update_data() # PREVIOUSLY DEFINED
                for i in range(0,len(datta),2): # Looping for half the amount of given data (and implementing twice to balance it)
                    self.txtReceipt1.insert(END,datta[i])   # Implementing Constants
                    self.txtReceipt2.insert(END,datta[i+1]) # Implementing Variables
            else: # If all information/variables/data is NOT given
                # Cleaning Reciept
                self.txtReceipt1.delete("1.0",END) # Constants
                self.txtReceipt2.delete("1.0",END) # Variables
                self.txtReceipt1.insert(END,"\nNo Input") # Show that there's some missing input
        
        # Exporting information to 'text' file (FILE MANAGING)
        def Exporter():
            # Checking if all the information/variables/data is given before writing reciept
            if reset_counter == 0 and self.payment.CusDri.Firstname.get()!="" and self.payment.CusDri.Lastname.get()!="" and self.payment.CusDri.Address.get()!="" and self.payment.CusDri.Gender.get()!="" and self.payment.CusDri.PhoneNum.get()!="" and self.payment.CusDri.CNIC.get()!="" and self.payment.CusDri.Email.get()!="":
                update_data() # PREVIOUSLY DEFINED
                for i in range(len(datta)): # Looping for the amount of given data
                    file_mng(datta[i]) # Exporting it to program output and given text files
                file_mng("\n\n-----\n\n") # Leaving space for more receipts
                w = ms.showinfo("Exporter ","Reciept and Information\nSuccessfully exported!") # Show message if successfully exported
            else:
                w = ms.showwarning("Error !","Invalid Input\nPlease try again !!!")

        #
        # Reciept Frames
        # 

        # Defining 'Reciept Button' frame, a sub-frame of 'CustomerDetailsFrame'
        # It contains all information summarized in a separate 'Reciept' frame
        Receipt_BottonFrame=LabelFrame(CustomerDetailsFrame,bd=10, width=450, relief=RIDGE)
        Receipt_BottonFrame.pack(side=RIGHT,fill=BOTH,expand=True) # Display it on the GUI at a specific location

        # Defining the 'Reciept Frame', a sub-frame of 'Reciept button' frame
        # It will have the blank Reciepts on it which will be filled by the program
        ReceiptFrame=LabelFrame(Receipt_BottonFrame, width=350,height=300, font=(FONT,12,'bold'),text="Receipt", relief=RIDGE)
        ReceiptFrame.grid(row=0,column=0) # Display it on the GUI at a specific location

        # Defining a blank text spot, where CONSTANTS defined in the 'datta' list will be written
        self.txtReceipt1 = Text(ReceiptFrame,bg = color.white,width = 25, height = 21,font=(FONT,11,'bold'),borderwidth=0)
        self.txtReceipt1.grid(row=0,column=0,columnspan=2) # Display it on the GUI at a specific location
        # Defining a blank text spot, where VARIABLES defined in the 'datta' list will be written
        self.txtReceipt2 = Text(ReceiptFrame,bg = color.white,width = 24, height = 21,font=(FONT,11,'bold'),borderwidth=0)
        self.txtReceipt2.grid(row=0,column=2,columnspan=2) # Display it on the GUI at a specific location

        # Defining the 'Buttons Frame', a sub-frame of 'Reciept button' frame
        # It will have the buttons "Total/Recipt/Reset/Exit"
        ButtonFrame=LabelFrame(Receipt_BottonFrame, width=350,height=100, relief=RIDGE)
        ButtonFrame.grid(row=1,column=0) # Displaying it on the GUI at a specific location
        
        # Making a button to calculate the total amount (Fare/Subtotal/Total) using the command 'Total_Paid()' and Displaying it on GUI
        self.btnTotal = Button(ButtonFrame,padx=18,bd=7,font=(FONT,11,'bold'),width = 2,text='Total',command=Total_Paid).grid(row=0,column=0)
        # Making a button to write the data on the blank RECIEPT using the command 'Receiptt()' and Displaying it on GUI
        self.btnReceipt = Button(ButtonFrame,padx=18,bd=7,font=(FONT,11,'bold'),width = 2,text='Receipt',command=Receiptt).grid(row=0,column=1)
        # Making a button to RESET all CUSTOMER's Entered data using the command 'Reset()' and Displaying it on GUI
        self.btnReset = Button(ButtonFrame,padx=18,bd=7,font=(FONT,11,'bold'),width = 2,text='Reset',command=Reset).grid(row=0,column=2)
        # Making a button to EXIT the program (GUI) using the command 'iExit()'
        self.btnExit = Button(ButtonFrame,padx=18,bd=7,font=(FONT,11,'bold'),width = 2,text='Exit', command=iExit).grid(row=0,column=3)

        # Defining the 'Export Frame', a subframe of 'FrameDetails'
        # It will have the "Export to text" button
        ExpFrame = LabelFrame(FrameDetails,bd=10, width=300,height=250, font=(FONT,12,'bold'),text="Exporter", relief=RIDGE)
        ExpFrame.grid(row=1,column=2) # Displaying it on the GUI at a specific location
        # Making a button to EXPORT the data from 'datta' to the 'text files' when clicked using the command "Exporter()"
        self.btnExport = Button(ExpFrame,padx=30,bd=10,font=(FONT,11,'bold'),width = 6,text='Export to text',command=Exporter).grid(row=0,column=0)
        

# Driver, to start up the code.
root = Tk() # Defining the imported Tkinter class into a variable for further use
root.tk_setPalette(background='gold') # Set a default color for the entire GUI
# The method "winfo_screen-" helps determine the ideal resolution for the window
w = root.winfo_screenwidth() # Width of the screen
h = root.winfo_screenheight() # Height of the screen
geometry= f'{w}x{h}+0+0' # Default Size of the window
# Initiating with login window
root.geometry("500x300+320+200") # Defining size for this window (object)
root.title('Sign In / Sign Up') # Title for the this window (object) 
root.option_add("*TCombobox*Listbox*Background",color.white)
application = Login(root) # Making the object for Login
Widgets(root).LoginMenu() # Defining instructons for Login
root.mainloop() # Starting the GUI