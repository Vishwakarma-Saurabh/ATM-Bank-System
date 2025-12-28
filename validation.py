import re

def validate_account_number(acc_no, existing_accounts=None):
    if not isinstance(acc_no, int):
        raise ValueError("Account number must be numeric")

    if acc_no <= 0:
        raise ValueError("Account number must be positive")
    
    if len(str(acc_no)) != 6:
        raise ValueError("Account number must be 6 digits")
    
    if existing_accounts and acc_no in existing_accounts:
        raise ValueError("Account number already exists")
    
    return True

def validate_pin(pin):
    if not isinstance(pin, int):
        raise ValueError("PIN must be numeric")
    
    if len(str(pin)) != 4:
        raise ValueError("PIN must be 4 digits")
    
    return True

def validate_holder_name(name):
    if not name or not name.strip():
        raise ValueError("Holder name cannot be empty")

    if not re.fullmatch(f"[A-Za-z ]+", name):
        raise ValueError("Holder name must contain only letters")
    
    return True

def validate_amount(amount):
    if not isinstance(amount, int):
        raise ValueError("Amount must be numeric")

    if amount <= 0:
        raise ValueError("Amount must be greater than zero")

    return True
