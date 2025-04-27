import tkinter as tk
from tkinter import messagebox
from database import Database

class RegisterWindow:
    def __init__(self):
        self.db = Database()

        self.window = tk.Toplevel()
        self.window.title("Register")
        self.window.geometry("300x300")
        self.window.configure(bg="#34495E")

        tk.Label(self.window, text="Register", font=("Helvetica", 16, "bold"), bg="#34495E", fg="#ECF0F1").pack(pady=10)

        tk.Label(self.window, text="Username:", bg="#34495E", fg="#ECF0F1").pack()
        self.entry_username = tk.Entry(self.window)
        self.entry_username.pack(pady=5)

        tk.Label(self.window, text="Password:", bg="#34495E", fg="#ECF0F1").pack()
        self.entry_password = tk.Entry(self.window, show="*")
        self.entry_password.pack(pady=5)

        tk.Button(self.window, text="Register", command=self.register_user, bg="#E74C3C", fg="white").pack(pady=10)

    def register_user(self):
        username = self.entry_username.get()
        password = self.entry_password.get()

        if self.db.add_user(username, password):
            messagebox.showinfo("Success", "Registration Successful!")
            self.window.destroy()
        else:
            messagebox.showerror("Error", "Username already exists!")

#