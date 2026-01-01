import re
from datetime import datetime


def validate_account_number(acc_no, existing=None):
    if not acc_no:
        return False, "Account number cannot be empty."
    
    acc_no = acc_no.strip().upper()
    
    pattern = r'^ACC\d+$'
    
    if not re.match(pattern, acc_no):
        return False, "Invalid format. Account number must be ACC followed by digits (e.g., ACC1767122042)."
    
    if existing is not None:
        if isinstance(existing, dict):
            if acc_no not in existing:
                return False, f"Account {acc_no} does not exist."
        elif isinstance(existing, (list, tuple, set)):
            if acc_no not in existing:
                return False, f"Account {acc_no} does not exist."
    
    return True, ""


def validate_pin(pin):
    if not pin:
        return False, "PIN cannot be empty."
    
    if not pin.isdigit():
        return False, "PIN must contain only digits."
    
    if len(pin) != 4:
        return False, "PIN must be exactly 4 digits."
    
    return True, ""


def validate_name(name):
    if not name or not name.strip():
        return False, "Name cannot be empty."
    
    name = name.strip()
    
    if not re.fullmatch(r"[A-Za-z ]+", name):
        return False, "Name must contain only letters and spaces."
    
    if len(name) < 2:
        return False, "Name must be at least 2 characters long."
    
    return True, ""


def validate_amount(amount):
    try:
        if isinstance(amount, str):
            amount = float(amount)
        
        if not isinstance(amount, (int, float)):
            return False, "Amount must be a number.", None
        
        if amount <= 0:
            return False, "Amount must be greater than zero.", None
        
        if amount > 1000000:
            return False, "Amount exceeds maximum limit of ₹10,00,000.", None
        
        return True, "", float(amount)
    
    except (ValueError, TypeError):
        return False, "Invalid amount. Please enter a valid number.", None


def validate_date(date_str):
    if not date_str:
        return False, "Date cannot be empty."
    
    try:
        datetime.strptime(date_str, '%d-%m-%Y')
        return True, ""
    except ValueError:
        return False, "Invalid date format. Use DD-MM-YYYY (e.g., 15-05-1990)."


def validate_mobile(mobile):
    if not mobile:
        return False, "Mobile number cannot be empty."
    
    mobile = str(mobile).strip()
    
    if not mobile.isdigit():
        return False, "Mobile number must contain only digits."
    
    if len(mobile) != 10:
        return False, "Mobile number must be exactly 10 digits."
    
    return True, ""


def validate_email(email):
    if not email:
        return False, "Email cannot be empty."
    
    email = email.strip()
    
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    if not re.match(pattern, email):
        return False, "Invalid email format (e.g., user@example.com)."
    
    return True, ""


def validate_gender(gender):
    if not gender:
        return False, "Gender cannot be empty."
    
    gender = gender.strip().upper()
    
    if gender not in ['M', 'F', 'O']:
        return False, "Gender must be M (Male), F (Female), or O (Other)."
    
    return True, ""


def validate_branch_code(branch_code):
    if not branch_code:
        return False, "Branch code cannot be empty."
    
    branch_code = branch_code.strip()
    
    if len(branch_code) < 3:
        return False, "Branch code must be at least 3 characters."
    
    if len(branch_code) > 10:
        return False, "Branch code cannot exceed 10 characters."
    
    if not branch_code.replace("-", "").replace("_", "").isalnum():
        return False, "Branch code must be alphanumeric."
    
    return True, ""


def validate_address(address):
    if not address or not address.strip():
        return False, "Address cannot be empty."
    
    if len(address.strip()) < 10:
        return False, "Address must be at least 10 characters long."
    
    return True, ""