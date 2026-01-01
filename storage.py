import json
import os
from bank_account import BankAccount

FILE = "data.json"


def save_all_accounts_to_file(accounts_dict):
    with open(FILE, "w") as f:
        json.dump(
            {
            str(acc_no): {
                "holder": acc.holder,
                "gender": acc.gender,
                "DOB": acc.DOB,
                "address": acc.address,
                "mobile": acc.mobile,
                "email": acc.email,
                "account_type": acc.account_type,
                "Status": acc.status,
                "KYC": acc.KYC,
                "branch_code": acc.branch_code,
                "opening_date": acc.opening_date,
                "pin": acc.get_pin(),
                "balance": float(acc.balance),
                "history": acc.history
            }
            for acc_no, acc in accounts_dict.items()
            }, f, indent=4
        )

def save_account(account, allow_update=False):
    accounts = load_all_accounts()
    accounts_dict = {acc.account_number: acc for acc in accounts}
    
    if not allow_update and account.account_number in accounts_dict:
        raise ValueError("Account number already exists!")

    accounts_dict[account.account_number] = account
    save_all_accounts_to_file(accounts_dict)

def load_account(acc_no):
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
        acc["holder"],
        acc["gender"],
        acc["DOB"],
        acc["address"],
        acc["mobile"],
        acc["email"],
        acc["account_type"],
        acc["status"],
        acc["KYC"],
        acc["branch_code"],
        acc["opening_date"],
        acc["pin"],
        acc["balance"],
        acc["history"]
    )

def load_all_accounts():
    if not os.path.exists(FILE):
        return []

    with open(FILE, "r") as file:
        data = json.load(file)

    accounts = []
    for acc_no, acc_data in data.items():
            account = BankAccount(
                account_number=acc_no,
                holder=acc_data["holder"],
                gender=acc_data["gender"],
                DOB=acc_data["DOB"],
                address=acc_data["address"],
                mobile=acc_data["mobile"],
                email=acc_data["email"],
                account_type=acc_data["account_type"],
                status=acc_data.get("status", "Active"),
                KYC=acc_data["KYC"],
                branch_code=acc_data["branch_code"],
                opening_date=acc_data["opening_date"],
                pin=acc_data["pin"],
                balance=float(acc_data["balance"])
            )
            account.set_pin(acc_data["pin"])
            account.history = acc_data.get("history", [])
            accounts.append(account)
    return accounts
