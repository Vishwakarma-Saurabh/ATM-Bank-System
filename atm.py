from datetime import date
from bank_account import BankAccount
from storage import save_all_accounts_to_file, save_account, load_all_accounts
from admin import Admin
from admin_storage import save_admin, load_admins
from validation import (validate_account_number, validate_pin, validate_name, validate_amount, validate_date, validate_email, validate_mobile)


def get_input(prompt, input_type='str', validation=None, validation_args=None, min_length=None, max_length=None, choices=None, min_value=None, max_value=None):
    while True:
        user_input = input(prompt).strip()

        if not user_input:
            print("❌ Input cannot be empty. Please try again.")
            continue
            
        if input_type == "int" or input_type == "menu":
            try:
                value = int(user_input)
                return value
            except ValueError:
                print("❌ Please enter a valid number.")
                continue
                
        elif input_type == "float" or input_type == "amount":
            try:
                value = float(user_input)
                if min_value is not None and value < min_value:
                    print(f"❌ Amount must be at least {min_value}.")
                    continue
                if max_value is not None and value > max_value:
                    print(f"❌ Amount cannot exceed {max_value}.")
                    continue
                return value
            except ValueError:
                print("❌ Please enter a valid number.")
                continue
        
        elif input_type == "str":
            if min_length and len(user_input) < min_length:
                print(f"❌ Must be at least {min_length} characters long.")
                continue
            if max_length and len(user_input) > max_length:
                print(f"❌ Must be at most {max_length} characters long.")
                continue
            if choices:
                if user_input.upper() not in [c.upper() for c in choices]:
                    print(f"❌ Please choose from: {', '.join(choices)}")
                    continue
                return user_input.upper()
            
            if validation:
                if validation_args:
                    is_valid, error_msg = validation(user_input, **validation_args)
                else:
                    is_valid, error_msg = validation(user_input)
                
                if not is_valid:
                    print(f"❌ {error_msg}")
                    continue
            
            return user_input
        else:
            return user_input


def create_admin():
    username = input("Admin username: ").strip()
    password = input("Admin Password: ")
    admin = Admin(username, password)
    save_admin(admin)
    print("✅ Admin account created successfully")


def admin_login():
    try:
        username = input("Enter username: ")
        password = input("Enter password: ")

        admins = load_admins()
        for admin in admins:
            if admin.verify(username, password):
                print("✅ Logged in successfully")
                return True
        print("❌ Invalid admin credentials")
        return False
    except ValueError:
        print(f"❌ Invalid admin credentials")
        return False


def admin_menu():
    print("\n" + "="*40)
    print("       ADMIN PANEL")
    print("="*40)
    print("1. Create Admin account")
    print("2. View all accounts")
    print("3. Delete account")
    print("4. Update user Name")
    print("5. Reset user PIN")
    print("6. Change Account Status")
    print("7. Logout")
    print("="*40)


def view_all_accounts():
    accounts = load_all_accounts()
    if not accounts:
        print("\n📋 No accounts found")
        return
        
    print("\n" + "="*120)
    print(f"{'ALL CUSTOMER ACCOUNTS':^120}")
    print("="*120)
    print(f"{'Acc No':<16} {'Holder':<25} {'Type':<15} {'Status':<18} {'Balance':<25} {'KYC':<12}")
    print("-"*120)

    for acc in accounts:
        if acc.status == "Active":
            status_display = "✅ Active"
        elif acc.status == "Inactive":
            status_display = "⚠️ Inactive"
        elif acc.status == "Suspended":
            status_display = "🚫 Suspended"
        elif acc.status == "Closed":
            status_display = "❌ Closed"
        elif acc.status == "Frozen":
            status_display = "🧊 Frozen"
        else:
            status_display = acc.status

        kyc_status = "✅ Yes" if acc.KYC else "❌ No"

        balance_display = f"₹ {acc.balance:,.2f}"

        print(
            f"{acc.account_number:<16} "
            f"{acc.holder:<25} "
            f"{acc.account_type:<15} "
            f"{status_display:<18} "
            f"{balance_display:<25} "
            f"{kyc_status:<12}"
        )

    print("="*120)
    print(f"{'Total Accounts:':<20} {len(accounts)}")
    print("="*120)


def show_account_info(account):
    print("\n" + "="*60)
    print("              ACCOUNT INFORMATION")
    print("="*60)
    print(f"Account Number : {account.account_number}")
    print(f"Holder Name    : {account.holder}")
    print(f"Account Type   : {account.account_type}")
    print(f"Status         : {account.status}")
    print(f"Balance        : ₹{account.get_balance():,.2f}")
    print(f"Branch Code    : {account.branch_code}")
    print(f"Opening Date   : {account.opening_date}")
    print(f"KYC Status     : {'Completed ✓' if account.KYC else 'Pending ✗'}")
    print("\n" + "-"*60)
    print("Account Type Rules & Restrictions:")
    print("-"*60)
    restrictions = account.get_account_restrictions()
    for restriction in restrictions:
        print(f"  {restriction}")
    print("="*60)


def delete_account():
    print("\n" + "="*50)
    print("         DELETE ACCOUNT")
    print("="*50)
    
    accounts = load_all_accounts()
    accounts_dict = {acc.account_number: acc for acc in accounts}
    
    acc_no = get_input(
        "Enter account number to delete: ",
        input_type="str",
        validation=validate_account_number,
        validation_args={'existing': accounts_dict}
    )
    
    account = accounts_dict[acc_no]
    
    print(f"\n⚠️  About to delete:")
    print(f"   Account: {acc_no}")
    print(f"   Holder: {account.holder}")
    print(f"   Balance: ₹{account.balance}")
    
    confirm = input("\nConfirm deletion? (Y/N): ").upper().strip()
    
    if confirm != 'Y':
        print("❌ Deletion cancelled")
        return
    
    del accounts_dict[acc_no]
    save_all_accounts_to_file(accounts_dict)
    print(f"✅ Account {acc_no} deleted successfully")


def update_username():
    print("\n" + "="*50)
    print("         UPDATE ACCOUNT NAME")
    print("="*50)
    
    accounts = load_all_accounts()
    accounts_dict = {acc.account_number: acc for acc in accounts}
    
    acc_no = get_input(
        "Enter account number: ",
        input_type="str",
        validation=validate_account_number,
        validation_args={'existing': accounts_dict}
    )
    
    account = accounts_dict[acc_no]
    print(f"\nCurrent name: {account.holder}")
    
    new_username = get_input(
        "Enter new name: ",
        input_type="str",
        validation=validate_name,
        min_length=2
    )
    
    confirm = input(f"\nChange '{account.holder}' to '{new_username}'? (Y/N): ").upper().strip()
    
    if confirm != 'Y':
        print("❌ Update cancelled")
        return
    
    account.holder = new_username
    save_all_accounts_to_file(accounts_dict)
    print(f"✅ Name updated to: {new_username}")


def reset_pin():
    print("\n" + "="*50)
    print("         RESET ACCOUNT PIN")
    print("="*50)
    
    accounts = load_all_accounts()
    accounts_dict = {acc.account_number: acc for acc in accounts}
    
    acc_no = get_input(
        "Enter account number: ",
        input_type="str",
        validation=validate_account_number,
        validation_args={'existing': accounts_dict}
    )
    
    account = accounts_dict[acc_no]
    print(f"\nAccount Holder: {account.holder}")
    
    new_pin = get_input(
        "Enter new 4-digit PIN: ",
        input_type="str",
        validation=validate_pin
    )
    
    confirm_pin = get_input(
        "Confirm new PIN: ",
        input_type="str",
        validation=validate_pin
    )
    
    if new_pin != confirm_pin:
        print("❌ PINs do not match")
        return
    
    account.set_pin(new_pin)
    save_all_accounts_to_file(accounts_dict)
    print(f"✅ PIN reset successful for account {acc_no}")


def change_account_status():
    print("\n" + "="*50)
    print("         CHANGE ACCOUNT STATUS")
    print("="*50)
    
    accounts = load_all_accounts()
    accounts_dict = {acc.account_number: acc for acc in accounts}
    
    acc_no = get_input(
        "Enter account number: ",
        input_type="str",
        validation=validate_account_number,
        validation_args={'existing': accounts_dict}
    )
    
    account = accounts_dict[acc_no]
    
    print(f"\n📋 Account Holder: {account.holder}")
    print(f"📋 Current Status: {account.status}")
    
    print("\n" + "-"*50)
    print("Available Status Options:")
    print("-"*50)
    print("1. Active      - Account is fully operational")
    print("2. Inactive    - Account is temporarily disabled")
    print("3. Suspended   - Account is suspended due to violations")
    print("4. Closed      - Account is permanently closed")
    print("5. Frozen      - Account is frozen (no transactions)")
    print("-"*50)
    
    status_choice = input("\nEnter new status (1-5) or 0 to cancel: ").strip()
    
    status_map = {
        '1': 'Active',
        '2': 'Inactive',
        '3': 'Suspended',
        '4': 'Closed',
        '5': 'Frozen'
    }
    
    
    if status_choice not in status_map:
        print("❌ Invalid choice")
        return
    
    new_status = status_map[status_choice]
    
    print(f"\n⚠️  Change status from '{account.status}' to '{new_status}'?")
    confirm = input("Confirm? (Y/N): ").upper().strip()
    
    if confirm != 'Y':
        print("❌ Status change cancelled")
        return
    
    old_status = account.status
    account.status = new_status
    
    accounts_dict[acc_no] = account
    save_all_accounts_to_file(accounts_dict)
    
    print(f"\n✅ Account status changed successfully!")
    print(f"   {old_status} → {new_status}")
    print(f"   Account: {acc_no} ({account.holder})")


def generate_account_number():
    import time
    return f"ACC{int(time.time())}"


def create_new_account():
    print("\n=== Create New Account ===\n")
    
    name = get_input(
        "Enter account holder name: ",
        input_type="str",
        validation=validate_name,
        min_length=2
    )
    
    gender = get_input(
        "Enter Gender - M (Male), F (Female), O (Others): ",
        input_type="str",
        choices=['M', 'F', 'O']
    )
    
    dob = get_input(
        "Enter date of birth (DD-MM-YYYY): ",
        input_type="str",
        validation=validate_date
    )
    
    address = get_input(
        "Enter address: ",
        input_type="str",
        min_length=10
    )
    
    mobile = get_input(
        "Enter mobile number (10 Digits): ",
        input_type="str",
        validation=validate_mobile
    )
    
    email = get_input(
        "Enter email address: ",
        input_type="str",
        validation=validate_email
    ).lower()
    
    print("\nAccount Types:")
    print("1. Savings")
    print("2. Current")
    print("3. Fixed Deposit")
    print("4. Recurring Deposit")
    
    account_type_choice = get_input("Choose account type (1-4): ", input_type="menu")
    while account_type_choice not in [1, 2, 3, 4]:
        print("❌ Invalid choice. Select 1-4.")
        account_type_choice = get_input("Choose account type (1-4): ", input_type="menu")
    
    account_types = {1: "Savings", 2: "Current", 3: "Fixed Deposit", 4: "Recurring Deposit"}
    account_type = account_types[account_type_choice]
    
    status = "Active"
    
    kyc_input = get_input(
        "Is KYC completed? (Y/N): ",
        input_type="str",
        choices=['Y', 'N']
    )
    kyc = True if kyc_input == 'Y' else False
    
    branch_code = get_input(
        "Enter branch code (e.g., BR001): ",
        input_type="str",
        min_length=3,
        max_length=10
    ).upper()
    
    opening_date = str(date.today())
    print(f"Opening date: {opening_date}")
    
    pin = get_input(
        "Create 4-digit PIN: ",
        input_type="str",
        validation=validate_pin
    )
    
    confirm_pin = get_input(
        "Confirm 4-digit PIN: ",
        input_type="str",
        validation=validate_pin
    )
    
    while pin != confirm_pin:
        print("❌ PINs don't match. Try again.")
        pin = get_input(
            "Create 4-digit PIN: ",
            input_type="str",
            validation=validate_pin
        )
        confirm_pin = get_input(
            "Confirm 4-digit PIN: ",
            input_type="str",
            validation=validate_pin
        )
    
    balance = get_input(
        "Enter initial deposit amount: ",
        input_type="amount",
        validation=validate_amount
    )
    
    acc_no = generate_account_number()
    
    print("\n" + "="*50)
    print("ACCOUNT DETAILS SUMMARY")
    print("="*50)
    print(f"Account Number: {acc_no}")
    print(f"Name: {name}")
    print(f"Gender: {gender}")
    print(f"Date Of Birth: {dob}")
    print(f"Address: {address}")
    print(f"Mobile: {mobile}")
    print(f"Email: {email}")
    print(f"Account Type: {account_type}")
    print(f"Status: {status}")
    print(f"KYC Completed: {'Yes' if kyc else 'No'}")
    print(f"Branch Code: {branch_code}")
    print(f"Opening Date: {opening_date}")
    print(f"Initial Balance: ₹{balance:.2f}")
    print("="*50)
    
    confirm = get_input(
        "\nConfirm account creation? (Y/N): ",
        input_type="str",
        choices=['Y', 'N']
    )
    
    if confirm != 'Y':
        print("❌ Account creation cancelled.")
        return None
    
    account = BankAccount(
        account_number=acc_no,
        holder=name,
        gender=gender,
        DOB=dob,
        address=address,
        mobile=mobile,
        email=email,
        account_type=account_type,
        status=status,
        KYC=kyc,
        branch_code=branch_code,
        opening_date=opening_date,
        pin=pin,
        balance=balance
    )
    
    account.set_pin(pin)
    return account


def login():
    print("\n" + "="*40)
    print("           LOGIN")
    print("="*40)
    
    try:
        accounts = load_all_accounts()
        accounts_dict = {acc.account_number: acc for acc in accounts}
        
        acc_no = get_input(
            "Enter your account number: ",
            input_type="str",
            validation=validate_account_number,
            validation_args={'existing': accounts_dict}
        )
        
        pin = get_input(
            "Enter PIN: ",
            input_type="str",
            validation=validate_pin
        )
        
        account = accounts_dict[acc_no]
        
        if account.status != "Active":
            print(f"❌ Login denied. Account status: {account.status}")
            print("   Please contact Bank Administration for assistance.")
            return None
        
        if not account.verify_pin(pin):
            raise ValueError("Incorrect PIN")
        
        print(f"✅ Welcome, {account.holder}!")
        return account
    
    except ValueError as e:
        print(f"❌ Login failed: {e}")
        return None


def menu():
    print("\n" + "="*40)
    print("     BANKING SYSTEM")
    print("="*40)
    print("1. Login")
    print("2. Create account")
    print("3. Admin Login")
    print("4. Exit")
    print("="*40)


def main_menu():
    print("\n" + "="*40)
    print("     CUSTOMER MENU")
    print("="*40)
    print("1. Deposit")
    print("2. Withdraw")
    print("3. Transfer money")
    print("4. Balance")
    print("5. History")
    print("6. Account Information")
    print("7. Logout")
    print("="*40)


while True:
    menu()
    choice = get_input("Enter your choice: ", input_type="menu")
    
    if choice == 1:
        current_account = login()
        if current_account:
            while True:
                main_menu()
                choice = get_input("Enter choice: ", input_type="menu")
                
                if choice == 1:
                    try:
                        amount = get_input(
                            "Enter amount to deposit: ",
                            input_type="amount",
                            validation=validate_amount
                        )
                        
                        current_account.deposit(amount)
                        save_account(current_account, allow_update=True)
                        print(f"✅ Deposited ₹{amount:.2f} successfully")
                    
                    except ValueError as e:
                        print(f"❌ Transaction failed: {e}")
                
                elif choice == 2:
                    try:
                        amount = get_input(
                            "Enter amount to withdraw: ",
                            input_type="amount",
                            min_value=1,
                            max_value=current_account.get_balance(),
                            validation=validate_amount
                        )
                        
                        current_account.withdraw(amount)
                        save_account(current_account, allow_update=True)
                        print(f"✅ Withdrew ₹{amount:.2f} successfully")
                    
                    except ValueError as e:
                        print(f"❌ Transaction failed: {e}")
                
                elif choice == 3:
                    try:
                        accounts = load_all_accounts()
                        accounts_dict = {acc.account_number: acc for acc in accounts}
                        
                        target_acc_no = get_input(
                            "Enter recipient account number: ",
                            input_type="str",
                            validation=validate_account_number,
                            validation_args={'existing': accounts_dict}
                        )
                        
                        target_account = accounts_dict[target_acc_no]
                        
                        if target_acc_no == current_account.account_number:
                            print("❌ Cannot transfer to your own account")
                            continue
                        
                        amount = get_input(
                            "Enter amount to transfer: ",
                            input_type="amount",
                            min_value=1,
                            max_value=current_account.get_balance(),
                            validation=validate_amount
                        )
                        
                        current_account.transfer(target_account, amount)
                        save_account(current_account, allow_update=True)
                        save_account(target_account, allow_update=True)
                        print(f"✅ Transferred ₹{amount:.2f} to {target_acc_no} ({target_account.holder})")
                    
                    except ValueError as e:
                        print(f"❌ Transaction failed: {e}")
                
                elif choice == 4:
                    print(f"\n💰 Current Balance: ₹{current_account.get_balance():.2f}")
                
                elif choice == 5:
                    history = current_account.get_history()
                    if not history:
                        print("\n📋 No transaction history")
                    else:
                        print("\n" + "="*50)
                        print("         TRANSACTION HISTORY")
                        print("="*50)
                        for h in history:
                            print(h)
                        print("="*50)
                
                elif choice == 6:
                    show_account_info(current_account)
                
                elif choice == 7:
                    print("👋 Logged out successfully")
                    break
                
                else:
                    print("❌ Invalid choice")
    
    elif choice == 2:
        account = create_new_account()
        if account:
            try:
                save_account(account, allow_update=False)
                print(f"\n✅ Account created successfully!")
                print(f"   Account Number: {account.account_number}")
            except ValueError as e:
                print(f"\n❌ Error: {e}")
    
    elif choice == 3:
        if admin_login():
            while True:
                admin_menu()
                
                choice = get_input("Enter choice: ", input_type="menu")
                
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
                    change_account_status()
                elif choice == 7:
                    print("👋 Logged out successfully")
                    break
                else:
                    print("❌ Invalid choice")
    
    elif choice == 4:
        print("👋 Session ended. Thank you for using our banking system!")
        break
    
    else:
        print("❌ Invalid choice. Please select 1-4.")