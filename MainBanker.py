#MAKE A FAKE BANKING DATA THING TO WRITE TO A FILE THE USERS PASSWORD AND/OR USERNAME
#MAKE INTO A CTK OR TKINTER GUI

import json
import os
import hashlib
import tkinter as tk

FILE_NAME = "user_data.json"

class BANKING_THING(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title("Banking")
        self.status_label = tk.Label(self, text="", font="Ariel 5 bold"); self.status_label.pack(padx=5, pady=5)
        self.make_account_button = tk.Button(self, text="Make account", font="Ariel 20 bold", command=self.make_account).pack(padx=10, pady=10)

    def hash_data(self, data):
        return hashlib.sha256(data.encode()).hexdigest()

    def load_accounts(self):
        if not os.path.exists(FILE_NAME):
            return []
        try:
            with open(FILE_NAME, "r") as f:
                data = json.load(f)
                return data if isinstance(data, list) else []
        except (json.JSONDecodeError, TypeError):
            return []

    def save_accounts(self, accounts):
        with open(FILE_NAME, "w") as f:
            json.dump(accounts, f, indent=4)

    def make_account(self):
        if hasattr(self, "user_entry"):
            self.user_entry.destroy()
            self.user_label.destroy()
            self.password_entry.destroy()
            self.password_label.destroy()
            self.get_data_button.destroy()
        self.user_label = tk.Label(self, text="(Username)", font="Ariel 8 bold"); self.user_label.pack(pady=5)
        self.user_entry = tk.Entry(self, width=20, font="Ariel 10 bold"); self.user_entry.pack(padx=5, pady=5)
        self.password_label = tk.Label(self, text="(Password)", font="Ariel 8 bold"); self.password_label.pack(pady = 5)
        self.password_entry = tk.Entry(self, width=20, font="Ariel 10 bold"); self.password_entry.pack(padx=5, pady=5)
        self.get_data_button = tk.Button(self, text="Submit account", font="Ariel 20 bold", command=self.submit_account); self.get_data_button.pack(padx=5, pady=5)
    
    def submit_account(self):
        user = self.hash_data(self.user_entry.get())
        password = self.hash_data(self.password_entry.get())
        accounts = self.load_accounts()
        if any(isinstance(acc, dict) and acc.get('USERNAME') == user for acc in accounts):
            self.status_label.config(text = "Error: Account username already taken.")
        else:
            accounts.append({"USERNAME": user, "PASSWORD": password})
            self.save_accounts(accounts)
            self.status_label.config(text = "Account created successfully (Stored as SHA-256).")

    def login(self):
        user_h = self.hash_data(input("Enter Username\n >> "))
        pass_h = self.hash_data(input("Enter Password\n >> "))
        accounts = self.load_accounts()
        for acc in accounts:
            if (isinstance(acc, dict) and 
                acc.get("USERNAME") == user_h and 
                acc.get("PASSWORD") == pass_h):
                print("\nLogged in successfully.")
                return
        print("\nAccount not registered or incorrect password.")

    def delete_account(self):
        user_h = self.hash_data(input("Enter Username\n >> "))
        pass_h = self.hash_data(input("Enter Password\n >> "))
        accounts = self.load_accounts()
        match = next((acc for acc in accounts if 
                      isinstance(acc, dict) and 
                      acc.get('USERNAME') == user_h and 
                      acc.get('PASSWORD') == pass_h), None)
        if not match:
            print("Account not found. Please try again.")
        else:
            if input("Are you sure? Y/N\n >> ").lower() == "y":
                accounts.remove(match)
                self.save_accounts(accounts)
                print("Account successfully deleted.")

    def get_option(self):
        options = {"1": self.make_account, "2": self.login, "3": self.delete_account, "4": exit}
        while True:
            main_input = input("banking data thingymabober\n\n\t1: Make Account\n\t2: Login\n\t3: Delete\n\t4: Exit\n >> ")
            if main_input in options:
                options[main_input]()
            else:
                print("Please enter 1, 2, 3, or 4.")

# ______ _______ _______ 
#|  ___ \   |   |    |  |
#|      <   |   |  | |  |
#|___|__|_______|__|____|

if __name__ == "__main__":
    app = BANKING_THING()
    app.mainloop()
