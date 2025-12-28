from bank_account import BankAccount
from storage import save_account, load_account, load_all_accounts
from admin import Admin
from admin_storage import save_admin, load_admins, initialize_supreme_admin
from validation import (validate_account_number, validate_pin, validate_holder_name, validate_amount)


def get_input(prompt):
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Please enter a valid number")
            
def get_holder_name(prompt):
    while True:
        name = input(prompt).strip()

        if not name:
            print("Holder name cannot be empty")
        elif not name.replace(" ", "").isalpha():
            print("Holder name must contain only letters") 
        else:
            return name

def create_admin():
    username = input("Admin username: ").strip()
    password = input("Admin Password: ")
    admin = Admin(username, password)
    save_admin(admin)
    print("Admin account created successfully")

def admin_login():
    try:
        username = input("Enter username: ")
        password = input("Enter password: ")

        admins = load_admins()
        for admin in admins:
            if admin.verify(username, password):
                print("Logged in successfully")
                return True
        print("Invalid admin credentials")
        return False
    except ValueError:
        print(f"Invalid admin credentials")
        return False

def admin_menu():
    print("\nAdmin Menu")
    print("1. Create admin account")
    print("2. View all accounts")
    print("3. Delete account")
    print("4. Update User name")
    print("5. Reset user PIN")
    print("6. Logout")

def view_all_accounts():
    accounts = load_all_accounts()
    if not accounts:
        print("No accounts found")
        return
    for acc in accounts:
        print(f"Account no. {acc.account_number}, Holder: {acc.holder}, Balance: {acc.balance}")

def delete_account():
    acc_no = get_input("Enter account number to delete: ")
    accounts = load_all_accounts()
    accounts_dict = {acc.account_number: acc for acc in accounts}

    if acc_no not in accounts_dict:
        print("Account not found")
        return

    del accounts_dict[acc_no]

    from storage import FILE
    import json

    with open(FILE, "w") as f:
        json.dump(
            {
                str(acc_no): {
                    "pin": acc.get_pin(),
                    "holder": acc.holder,
                    "balance": acc.balance,
                    "history": acc.history
                }
                for acc_no, acc in accounts_dict.items()
            }, f, indent=4
        )
    print(f"Account {acc_no} deleted successfully")

def update_username():
    acc_no = get_input("Enter account number: ")
    accounts = load_all_accounts()
    accounts_dict = {acc.account_number: acc for acc in accounts}

    if acc_no not in accounts_dict:
        print("Account not found")
        return

    new_username = get_holder_name("Enter new Username: ")
    accounts_dict[acc_no].holder = new_username

    from storage import FILE
    import json

    with open(FILE, "w") as f:
        json.dump(
            {
                str(acc_no): {
                    "pin": acc.get_pin(),
                    "holder": acc.holder,
                    "balance": acc.balance,
                    "history": acc.history
                }
                for acc_no, acc in accounts_dict.items()
            }, f, indent=4
        )
    print(f"Username updated successfully for account {acc_no}")


def reset_pin():
    acc_no = get_input("Enter account number: ")
    accounts = load_all_accounts()
    
    if not accounts:
        print("No accounts found")
        return
    
    accounts_dict = {acc.account_number: acc for acc in accounts}
    
    if acc_no not in accounts_dict:
        print("Account not found")
        return

    new_pin = get_input("Enter new PIN: ")
    validate_pin(new_pin)
    
    accounts_dict[acc_no].pin = new_pin 
    accounts_dict[acc_no].set_pin(new_pin)

    from storage import FILE
    import json

    json_data = {}
    for acc_number, acc in accounts_dict.items():
        json_data[str(acc_number)] = {
            "pin": acc.get_pin(), 
            "holder": acc.holder,
            "balance": acc.balance,
            "history": acc.history
        }
    with open(FILE, "w") as f:
        json.dump(json_data, f, indent=4)
    print(f"PIN reset successfully for account {acc_no}")

def create_account():
    try:
        acc_no = get_input("Account number (6 digits): ")
        accounts = load_all_accounts()
        validate_account_number(acc_no,  {acc.account_number: acc for acc in accounts})

        pin = get_input("Enter PIN (4 digits): ")
        validate_pin(pin)

        name = get_holder_name("Enter name: ")
        validate_holder_name(name)

        balance = get_input("Initial Balance: ")
        validate_amount(balance)

        account = BankAccount(acc_no, pin, name, balance)
        save_account(account)
        print("Account created successfully")

    except ValueError as e:
        print(f"Error: {e}")
        
def login():
    try:
        acc_no = get_input("Enter your account number: ")
        pin = get_input("Enter PIN: ")
        
        account = load_account(acc_no)
        if not account:
            raise ValueError("Account not found")

        if not account.verify_pin(pin):
            raise ValueError("Incorrect PIN")

        print("Logged in successfully")
        return account

    except ValueError as e:
        print(f"Log in failed: {e}")
        return None
    
def menu():
    print("Press respective number to select the operation: ")
    print("1. Login")
    print("2. Create account")
    print("3. Admin Login")
    print("4. Exit")
    
def main_menu():
    print("1. Deposit")
    print("2. Withdraw")
    print("3. Transfer money")
    print("4. Balance")
    print("5. History")
    print("6. Logout")
    
while True:
    menu()
    choice = get_input("Enter your choice: ")

    if choice == 1:
        current_account = login()
        if current_account:
            while True:
                main_menu()
                choice = get_input("Enter choice: ")

                if choice == 1:
                    try:
                        amount = get_input("Enter amount to deposit: ")
                        validate_amount(amount)

                        current_account.deposit(amount)
                        save_account(current_account, allow_update=True)
                        print(f"Deposited {amount} successfully")
                    
                    except ValueError as e:
                        print(f"Transaction failed: {e}")

                elif choice == 2:
                    try:
                        amount = get_input("Enter the amount to withdraw: ")
                        validate_amount(amount)

                        current_account.withdraw(amount)
                        save_account(current_account, allow_update=True)
                        print(f"Withdrew {amount} successfully")

                    except ValueError as e:
                        print(f"Transaction failed: {e}")
                    
                elif choice == 3:
                    try:
                        target_acc_no = get_input("Enter recipient account number: ")
                        validate_account_number(target_acc_no)
                        target_account = load_account(target_acc_no)

                        if not target_account:
                            raise ValueError("Recipient account not found")

                        amount = get_input("Enter amount to transfer: ")
                        validate_amount(amount)

                        current_account.transfer(target_account, amount)
                        save_account(current_account, allow_update=True)
                        save_account(target_account, allow_update=True)
                        print(f"Transferred {amount} to account {target_acc_no} successfully")

                    except ValueError as e:
                        print(f"Transaction failed: {e}")

                elif choice == 4:
                    print(f"Balance: {current_account.get_balance()}")
                
                elif choice == 5:
                    history = current_account.get_history()
                    if not history:
                        print("No transaction history")
                    else:
                        for h in history:
                            print(h)

                elif choice == 6:
                    print("Logged out successfully")
                    break
                else:
                    print("Invalid choice")
        
    elif choice == 2:
        create_account()

    elif choice == 3:
        if admin_login():

            while True:
                admin_menu()

                choice = get_input("Enter choice: ")
                if choice == 1:
                    create_admin()
                elif choice == 2:
                    view_all_accounts()
                elif choice == 3:
                    delete_account()
                elif choice == 4:
                    update_username()
                elif choice == 5:
                    reset_pin()
                elif choice == 6:
                    print("Logged out successfully")
                    break
                else:
                    print("Invalid choice")
            
    elif choice == 4:
        print("Session end")
        break
    else:
        print("Invalid choice")
