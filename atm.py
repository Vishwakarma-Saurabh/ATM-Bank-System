from storage import save_account, load_accounts
from bank_account import BankAccount


def create_account():
    acc_no = int(input("Account number:"))
    pin = int(input("Enter PIN: "))
    holder = input("Holder name: ")
    balance = int(input("Initial balance: "))
    account = BankAccount(acc_no, pin, holder, balance)
    save_account(account)
    print("Account created successfully")

def login():
    acc_no = int(input("Enter your account number: "))
    pin = int(input("Enter PIN: "))
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
    choice = int(input("Enter your choice: "))

    if choice == 1:
        current_account = login()
        if current_account:
            while True:
                main_menu()
                choice = int(input("Enter choice: "))

                if choice == 1:
                    amount = int(input("Enter amount to deposit: "))
                    current_account.deposit(amount)
                    save_account(current_account)
                    print(f"Deposited {amount} successfully")

                elif choice == 2:
                    amount = int(input("Enter the amount to withdraw: "))
                    current_account.withdraw(amount)
                    save_account(current_account)
                    print(f"Withdrew {amount} successfully")

                elif choice == 3:
                    target_acc_no = int(input("Enter recipient account number: "))
                    target_account = load_accounts(target_acc_no)

                    if not target_account:
                        print("Recipient account does not exist.")
                    else:
                        amount = int(input("Enter amount to transfer: "))
                        if current_account.transfer(target_account, amount):
                            save_account(current_account)
                            save_account(target_account)
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
