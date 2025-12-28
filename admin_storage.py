
import pickle
import os
import json
from admin import Admin

Admin_File = "admin.json"

def save_admin(admin):
    admins = load_admins()
    for a in admins:
        if a.username == admin.username:
            raise ValueError("Admin already exists")
    
    admins.append(admin)
    with open(Admin_File, "w") as f:
        json.dump([
                   {
                       "username": a.username,
                       "password": a.password,
                       "role": a.role
                   } for a in admins], f, indent=4
                   )

def load_admins():
    if not os.path.exists(Admin_File):
        return []
    with open(Admin_File, "r") as f:
        data = json.load(f)

    admins = []
    for a in data:
        admins.append(Admin(a["username"], a["password"], a["role"]))
    return admins
        
def initialize_supreme_admin():
    admins = load_admins()
    if not admins:
        print("No admin found. Create Supreme Admin")
        username = input("Supreme admin username: ")
        password = input("Supreme admin password: ")
        supreme = Admin(username, password, role="supreme")
        save_admin(supreme)
        print("Supreme Admin created successfully")