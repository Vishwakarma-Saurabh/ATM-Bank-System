from storage import save_account, load_accounts
from bank_account import BankAccount


def get_input(prompt):
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Please enter a valid number")


def get_positive_input(prompt):
    while True:
        try:
            value = int(input(prompt))
            if value < 0:
                print("Value must be non-negative")
            else:
                return value
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

def create_account():
    acc_no = get_input("Account number: ")
    
    if load_accounts(acc_no):
        print("Account number already exists!")
        return
    
    pin = get_input("Enter PIN: ")
    holder = get_holder_name("Holder name: ")
    balance = get_positive_input("Initial balance: ")
    account = BankAccount(acc_no, pin, holder, balance)
    try:
        save_account(account)
        print("Account created successfully")
    except ValueError as e:
        print(e)

def login():
    acc_no = get_input("Enter your account number: ")
    pin = get_input("Enter PIN: ")
    accounts = load_accounts(acc_no)
    if accounts and accounts.verify_pin(pin):
        print("Logged in successfully")
        return accounts
    print("Invalid account number or PIN")
    return None

def menu():
    print("Press respective number to select the operation: ")
    print("1. Login")
    print("2. Create account")
    print("3. Exit")
    
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
                    amount = get_positive_input("Enter amount to deposit: ")
                    current_account.deposit(amount)
                    save_account(current_account, allow_update=True)
                    print(f"Deposited {amount} successfully")

                elif choice == 2:
                    amount = get_positive_input("Enter the amount to withdraw: ")
                    current_account.withdraw(amount)
                    save_account(current_account, allow_update=True)
                    print(f"Withdrew {amount} successfully")

                elif choice == 3:
                    target_acc_no = get_input("Enter recipient account number: ")
                    target_account = load_accounts(target_acc_no)

                    if not target_account:
                        print("Recipient account does not exist.")
                    else:
                        amount = get_positive_input("Enter amount to transfer: ")
                        if current_account.transfer(target_account, amount):
                            save_account(current_account, allow_update=True)
                            save_account(target_account, allow_update=True)
                            print(f"Transferred {amount} to account {target_acc_no} successfully")

                elif choice == 4:
                    print(f"Balance: {current_account.get_balance()}")
                
                elif choice == 5:
                    history = current_account.get_history()
                    if not history:
                        print("No transaction hsitory")
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
        print("Session end")
        break
    else:
        print("Invalid choice")
