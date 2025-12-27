import json
import os
from bank_account import BankAccount

FILE = "data.json"

def save_account(account, allow_update=False):
    accounts = load_all_accounts()
    accounts_dict = {acc.account_number: acc for acc in accounts}
    
    if not allow_update and account.account_number in accounts_dict:
        raise ValueError("Account number already exists!")

    accounts_dict[account.account_number] = account
    with open(FILE, "w") as file:
        json.dump(
            {
                str(acc_no): {
                    "pin": acc.get_pin(),
                    "holder": acc.holder,
                    "balance": acc.balance,
                    "history": acc.history
                }
                for acc_no, acc in accounts_dict.items()
            },
            file,
            indent=4
        )

def load_accounts(acc_no):
    if not os.path.exists(FILE):
        return None

    with open(FILE, "r") as file:
        data = json.load(file)

    acc_no = str(acc_no)
    if acc_no not in data:
        return None

    acc = data[acc_no]
    return BankAccount(
        int(acc_no),
        acc["pin"],
        acc["holder"],
        acc["balance"],
        acc["history"]
    )

def load_all_accounts():
    if not os.path.exists(FILE):
        return []

    with open(FILE, "r") as file:
        data = json.load(file)

    accounts = []
    for acc_no, acc in data.items():
        accounts.append(
            BankAccount(
                int(acc_no),
                acc["pin"],
                acc["holder"],
                acc["balance"],
                acc["history"]
            )
        )
    return accounts
