from datetime import datetime

class BankAccount:
    def __init__(self, account_number, pin, holder, balance=0, history=None):
        self.account_number = account_number
        self.__pin = pin
        self.holder = holder
        self.balance = balance
        self.history = history if history is not None else []

    def _add_history(self, action):
        time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.history.append(f"[{time}] {action}")

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            self._add_history(f"Deposited: {amount}")

    def withdraw(self, amount):
        if 0 < amount <= self.balance:
            self.balance -= amount
            self._add_history(f"Withdrew: {amount}")

    def get_balance(self):
        return self.balance

    def get_history(self):
        return self.history

    def verify_pin(self, pin):
        return self.__pin == pin

    def get_pin(self):
        return self.__pin

    def transfer(self, target_account, amount):
        if amount <= 0:
            print("Transfer amount must be positive.")
            return False

        if amount > self.balance:
            print("Insufficient balance.")
            return False

        # Deduct from sender
        self.balance -= amount
        self._add_history(f"Transferred {amount} to account {target_account.account_number}")

        # Add to receiver
        target_account.balance += amount
        target_account._add_history(f"Received {amount} from account {self.account_number}")

        return True
