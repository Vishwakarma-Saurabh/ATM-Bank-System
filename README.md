# Bank Management System (Python CLI)

A simple **command-line Bank Management System** built using Python.  
This project supports **user accounts and admin accounts**, with proper input validation and error handling.

----------------------------

🚀 Features

---------------------------


👤 User Features


Create a bank account with all essential field input

Automatically unique account number creation

Login using account number and PIN

Deposit money

Withdraw money

Transfer money to another account

View balance

View transaction history

Account type information ("Savings", "Current", "Fixed", "Recurring") with validation that allows/denies transaction

----------------------------


🛠️ Admin Features


Admin login

Supreme admin initialization on first run

Create admin accounts (only by existing admins)

View all bank accounts

Delete user accounts

Update user name

Reset user PIN

Change account status ("Active", "Inactive", "Closed", "Frozen", "Closed")

----------------------------


🔐 Validation & Safety


Validation for all input data

Validates account number format

Validates PIN format

Prevents duplicate accounts

Prevents invalid transactions

Handles errors without crashing

Ensures only authorized admins can create new admins & change account status

-----------------------------


📂 Project Structure


ATM_Project/
│
├── atm.py                  # Main program (menus & flow)
├── setup_admin.py          # One-time supreme admin creation 
├── bank_account.py         # BankAccount class
│
├── admin.py                # Admin class
├── admin_storage.py        # Save/load admins
│
├── storage.py              # Save/load bank accounts
├── validation.py           # All validations
│
├── data.json               # User accounts data
├── admins.json             # Admin accounts data


------------------------------


▶️ How to Run


Make sure Python is installed (Python 3.8+ recommended)

Clone the repository

Initialize the Supreme Admin (first run only):

python setup_admin.py


This will create the supreme admin account, which has full control over admin creation.

Run the main program:

python atm.py

Log in as the supreme admin to create other admin accounts.

Only existing admins (including the supreme admin) can create new admin accounts.


-------------------------------


📚 Future Improvements


Hash PINs and passwords for security

Add account freeze feature

Add unit tests

Create a GUI version

Email/mobile verification for users


-------------------------------

Author

Saurabh Vishwakarma
