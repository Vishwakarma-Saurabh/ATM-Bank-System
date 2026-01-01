from datetime import datetime

class BankAccount:
    def __init__(self, account_number, holder, gender, DOB, address, mobile, email, account_type, status, KYC, branch_code, opening_date, pin, balance=0, history=None):
        self.account_number = account_number
        self.holder = holder
        self.gender = gender
        self.DOB = DOB
        self.address = address
        self.mobile = mobile
        self.email = email
        self.account_type = account_type
        self.status = status
        self.KYC = KYC
        self.branch_code = branch_code
        self.opening_date = opening_date
        self.__pin = pin
        self.balance = float(balance)
        self.history = history if history is not None else []

    def _check_status(self):
        if self.status != "Active":
            raise ValueError(f"Transaction denied. Account status: {self.status}")
    
    def _check_account_type_for_withdrawal(self):
        restricted_types = ["Fixed Deposit", "Recurring Deposit"]
        if self.account_type in restricted_types:
            raise ValueError(f"{self.account_type} accounts do not allow withdrawals before maturity.")
    
    def _check_account_type_for_transfer(self):
        restricted_types = ["Fixed Deposit", "Recurring Deposit"]
        if self.account_type in restricted_types:
            raise ValueError(f"{self.account_type} accounts do not allow transfers.")
    
    def _check_transaction_limits(self, amount):
        limits = {
            "Savings": 50000,
            "Current": 1000000,
            "Fixed Deposit": 0,
            "Recurring Deposit": 0 
        }
        
        max_limit = limits.get(self.account_type, 50000)
        
        if max_limit > 0 and amount > max_limit:
            raise ValueError(f"{self.account_type} account transaction limit is ₹{max_limit:,.2f}")
    
    def _add_history(self, action):
        time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.history.append(f"[{time}] {action}")

    def deposit(self, amount):
        self._check_status()
        amount = float(amount)
        
        if amount <= 0:
            raise ValueError("Deposit amount must be positive")
        
        if self.account_type == "Fixed Deposit":
            raise ValueError("Fixed Deposit accounts cannot accept deposits after opening.")
        
        self._check_transaction_limits(amount)
        
        self.balance += amount
        self._add_history(f"Deposited: ₹{amount:.2f}, Balance: ₹{self.balance:.2f}")

    def withdraw(self, amount):
        self._check_status()
        self._check_account_type_for_withdrawal()
        
        amount = float(amount)
        
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive")

        if amount > self.balance:
            raise ValueError("Insufficient balance")
        
        self._check_transaction_limits(amount)
        
        if self.account_type == "Savings":
            min_balance = 1000
            if (self.balance - amount) < min_balance:
                raise ValueError(f"Savings account requires minimum balance of ₹{min_balance:.2f}")

        self.balance -= amount
        self._add_history(f"Withdrew: ₹{amount:.2f}, Balance: ₹{self.balance:.2f}")

    def transfer(self, target_account, amount):
        self._check_status()
        self._check_account_type_for_transfer()
        
        amount = float(amount)
        
        if target_account.status != "Active":
            raise ValueError(f"Recipient account is {target_account.status}. Transfer denied.")
        
        if amount <= 0:
            raise ValueError("Transfer amount must be positive")

        if amount > self.balance:
            raise ValueError("Insufficient balance")
        
        self._check_transaction_limits(amount)
        
        if self.account_type == "Savings":
            min_balance = 1000
            if (self.balance - amount) < min_balance:
                raise ValueError(f"Savings account requires minimum balance of ₹{min_balance:.2f}")
        
        if target_account.account_type == "Fixed Deposit":
            raise ValueError("Cannot transfer to Fixed Deposit accounts.")

        self.balance -= amount
        self._add_history(f"Transferred: ₹{amount:.2f} to {target_account.account_number}, Balance: ₹{self.balance:.2f}")

        target_account.balance += amount
        target_account._add_history(f"Received: ₹{amount:.2f} from {self.account_number}, Balance: ₹{target_account.balance:.2f}")

    def get_balance(self):
        return float(self.balance)

    def get_history(self):
        return self.history

    def verify_pin(self, pin):
        return self.__pin == pin

    def get_pin(self):
        return self.__pin

    def set_pin(self, new_pin):
        self.__pin = new_pin
    
    def get_account_restrictions(self):
        restrictions = {
            "Savings": [
                "✓ Deposits: Allowed",
                "✓ Withdrawals: Allowed",
                "✓ Transfers: Allowed",
                "⚠ Minimum balance: ₹1,000",
                "⚠ Max transaction: ₹50,000"
            ],
            "Current": [
                "✓ Deposits: Allowed",
                "✓ Withdrawals: Allowed",
                "✓ Transfers: Allowed",
                "✓ No minimum balance",
                "⚠ Max transaction: ₹10,00,000"
            ],
            "Fixed Deposit": [
                "✗ No additional deposits",
                "✗ No withdrawals before maturity",
                "✗ No transfers allowed",
                "⚠ Locked until maturity date"
            ],
            "Recurring Deposit": [
                "⚠ Fixed monthly deposits only",
                "✗ No withdrawals before maturity",
                "✗ No transfers allowed",
                "⚠ Locked until maturity date"
            ]
        }
        return restrictions.get(self.account_type, [])