import json
import os
import hashlib
import tkinter as tk
from ctypes import windll

FILE_NAME = "user_data.json"

class BANKING_THING(tk.Tk):

    def __init__(self):
        super().__init__()
        self.overrideredirect(True)
        self.title("Banking")
        self.title_bar = tk.Frame(self, width=self.winfo_width(), height=10, bd=3, relief="ridge")
        self.bind("<Button-1>", self.mouse_pos_calc)
        self.bind("<B1-Motion>", self.move_window)
        self.title_bar.pack(fill="x")
        self.title_bar_elements()
        self.main_frame = tk.Frame(self, width=400, height=400, bd=10, bg="white")
        self.main_frame.pack(padx=10, pady=10)
        self.status_label = tk.Label(self.main_frame, text="Hello, Login or Make an account!", font="Arial 10 bold"); self.status_label.pack(padx=5, pady=5)
        self.make_account_button = tk.Button(self.main_frame, text="Make account", font="Arial 20 bold", command=lambda: self.make_account(1))
        self.make_account_button.pack(padx=5, pady=5)
        self.login_button = tk.Button(self.main_frame, text="      Login      ", font="Arial 20 bold", command=self.login)
        self.login_button.pack(padx=5, pady=5)
        self.delete_account_button = tk.Button(self.main_frame, text="Delete Account", font="Arial 18 bold", command=self.delete_account)
        self.delete_account_button.pack(padx=5, pady=5)
        self.after(10, self.set_appwindow)
    
    def set_appwindow(self):
        GWL_EXSTYLE = -20; WS_EX_APPWINDOW = 0x00040000; WS_EX_TOOLWINDOW = 0x00000080
        hwnd = windll.user32.GetParent(self.winfo_id()); style = windll.user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
        style = style & ~WS_EX_TOOLWINDOW; style = style | WS_EX_APPWINDOW
        windll.user32.SetWindowLongW(hwnd, GWL_EXSTYLE, style)
        self.wm_withdraw(); self.after(10, self.wm_deiconify)

    def title_bar_elements(self):
        exit_button = tk.Button(self.title_bar, text="🗙", command=lambda: self.destroy())
        exit_button.pack(side="right")
        minimize_button = tk.Button(self.title_bar, text="\u2014", command=lambda: [self.overrideredirect(False), self.iconify(), self.bind("<Map>", self.restore)])
        minimize_button.pack(side="right")
    
    def restore(self, event=None):
        if self.state() == 'normal':
            self.unbind("<Map>")
            self.overrideredirect(True)
            self.after(10, self.set_appwindow) 

    def mouse_pos_calc(self, event):
        global offset_x, offset_y;offset_x = event.x;offset_y = event.y

    def move_window(self, event):
        new_x = event.x_root - offset_x;new_y = event.y_root - offset_y;self.geometry(f'+{new_x}+{new_y}')

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

    def make_account(self, button_id):
        if hasattr(self, "user_entry"):
            self.user_entry.destroy()
            self.user_label.destroy()
            self.password_entry.destroy()
            self.password_label.destroy()
            self.get_data_button.destroy()
        self.user_label = tk.Label(self.main_frame, text="(Username)", font="Arial 8 bold"); self.user_label.pack(pady=5)
        self.user_entry = tk.Entry(self.main_frame, width=20, font="Arial 10 bold"); self.user_entry.pack(padx=5, pady=5)
        self.password_label = tk.Label(self.main_frame, text="(Password)", font="Arial 8 bold"); self.password_label.pack(pady = 5)
        self.password_entry = tk.Entry(self.main_frame, width=20, font="Arial 10 bold"); self.password_entry.pack(padx=5, pady=5)
        if button_id == 1:
            self.get_data_button = tk.Button(self.main_frame, text="Submit account", font="Arial 20 bold", command=self.submit_account); self.get_data_button.pack(padx=5, pady=5)
        elif button_id == 2:
            self.get_data_button = tk.Button(self.main_frame, text="Submit login info", font="Arial 20 bold", command=self.login); self.get_data_button.pack(padx=5, pady=5)
        else:
            self.get_data_button = tk.Button(self.main_frame, text="Delete Account", font="Arial 20 bold", command=self.delete_account); self.get_data_button.pack(padx=5, pady=5)

    def submit_account(self):
        user = self.hash_data(self.user_entry.get())
        password = self.hash_data(self.password_entry.get())
        none = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
        if user == none or password == none:
            self.status_label.config(text="Please enter text into the boxes.")
        else:
            accounts = self.load_accounts()
            if any(isinstance(acc, dict) and acc.get('USERNAME') == user for acc in accounts):
                self.status_label.config(text = "Error: Account username already taken.")
            else:
                accounts.append({"USERNAME": user, "PASSWORD": password})
                self.save_accounts(accounts)
                self.status_label.config(text = "Account created successfully (Stored as SHA-256).")

    def login(self):
        self.make_account(2)
        none = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
        user_h = self.hash_data(self.user_entry.get())
        pass_h = self.hash_data(self.password_entry.get())
        if user_h == none or pass_h == none:
            self.status_label.config(text="Please enter text into the boxes.")
        else:
            accounts = self.load_accounts()
            for acc in accounts:
                if (isinstance(acc, dict) and 
                    acc.get("USERNAME") == user_h and 
                    acc.get("PASSWORD") == pass_h):
                    self.status_label.config(text="Logged in successfully.")
                    return
                self.status_label.config(text="Account not registered or incorrect password.")

    def delete_account(self):
        self.make_account(3)
        none = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
        user_h = self.hash_data(self.user_entry.get())
        pass_h = self.hash_data(self.password_entry.get())
        if user_h == none or pass_h == none:
            self.status_label.config(text="Please enter text into both boxes.")
        else:
            accounts = self.load_accounts()
            match = next((acc for acc in accounts if isinstance(acc, dict) and acc.get('USERNAME') == user_h and acc.get('PASSWORD') == pass_h), None)
            if not match:
                self.status_label.config(text="Account not found. Please try again.")
            else:
                self.yes_button = tk.Button(self.main_frame, text="YES", font="Arial 13 bold", command=lambda: self.confirmation_of_deletion(1))
                self.yes_button.pack()
                self.no_button = tk.Button(self.main_frame, text="NO", font="Arial 13 bold", command=lambda: self.confirmation_of_deletion(2))
                self.no_button.pack()
        
    def confirmation_of_deletion(self, button_id):
        user_h = self.hash_data(self.user_entry.get())
        pass_h = self.hash_data(self.password_entry.get())
        accounts = self.load_accounts()
        match = next((acc for acc in accounts if isinstance(acc, dict) and acc.get('USERNAME') == user_h and acc.get('PASSWORD') == pass_h), None)
        if button_id == 1:
            accounts.remove(match)
            self.save_accounts(accounts)
            self.status_label.config(text="Account successfully deleted.")
        else:
            self.status_label.config(text="Aborted deletion.")

# ______ _______ _______ 
#|  ___ \   |   |    |  |
#|      <   |   |  | |  |
#|___|__|_______|__|____|

if __name__ == "__main__":
    app = BANKING_THING()
    app.mainloop()
