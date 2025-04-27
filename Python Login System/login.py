import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
import sqlite3
import requests
from database import Database
from forgot_password import ForgotPasswordWindow
from otp_verification import OTPVerification

# Initialize database#
db = Database("users.db")

# Function to toggle password visibility
def toggle_password():
    if entry_password.cget('show') == "*":
        entry_password.config(show="")
    else:
        entry_password.config(show="*")

# Function to handle login
attempts = 3
def login():
    global attempts
    username = entry_username.get()
    password = entry_password.get()
    
    if db.validate_user(username, password):
        email = db.get_user_email(username)
        if email:
            otp_window = OTPVerification(username)
            root.wait_window(otp_window.top)
            if otp_window.otp_verified:
                messagebox.showinfo("Login Success", f"Welcome, {username}!")
                root.destroy()
            else:
                messagebox.showerror("OTP Failed", "Invalid OTP. Login Aborted.")
        else:
            messagebox.showerror("Login Failed", "Email not found. Please contact support.")
    else:
        attempts -= 1
        if attempts > 0:
            messagebox.showerror("Login Failed", f"Invalid Username or Password! {attempts} attempts left.")
        else:
            messagebox.showerror("Account Locked", "Too many failed attempts. Please try again later.")
            root.destroy()

# Function to open registration window
def open_register():
    import register
    register.RegisterWindow()

# Function to open forgot password window
def open_forgot_password():
    ForgotPasswordWindow()

# Creating the main window
root = tk.Tk()
root.title("Login System")
root.geometry("400x550")
root.configure(bg="#2C3E50")

# Load image
img_url = "https://cdn-icons-png.flaticon.com/512/5087/5087579.png"
img_data = Image.open(requests.get(img_url, stream=True).raw)
img_data = img_data.resize((80, 80), Image.LANCZOS)
img = ImageTk.PhotoImage(img_data)

# UI Elements
img_label = tk.Label(root, image=img, bg="#2C3E50")
img_label.pack(pady=10)

label_title = tk.Label(root, text="Login System", font=("Helvetica", 16, "bold"), bg="#2C3E50", fg="#ECF0F1")
label_title.pack(pady=5)

frame = tk.Frame(root, bg="#34495E", padx=20, pady=20)
frame.pack(pady=10)

label_username = tk.Label(frame, text="👤 Username:", font=("Helvetica", 12), bg="#34495E", fg="#ECF0F1")
label_username.grid(row=0, column=0, pady=5, padx=10, sticky="w")
entry_username = tk.Entry(frame, font=("Helvetica", 12), width=20)
entry_username.grid(row=0, column=1, pady=5, padx=10)

label_password = tk.Label(frame, text="🔒 Password:", font=("Helvetica", 12), bg="#34495E", fg="#ECF0F1")
label_password.grid(row=1, column=0, pady=5, padx=10, sticky="w")
entry_password = tk.Entry(frame, font=("Helvetica", 12), width=20, show="*")
entry_password.grid(row=1, column=1, pady=5, padx=10)

# Show/Hide Password Button
btn_toggle = tk.Button(frame, text="Show", font=("Helvetica", 10), command=toggle_password)
btn_toggle.grid(row=1, column=2, padx=5)

# Login and Register Buttons in the Same Alignment
btn_frame = tk.Frame(frame, bg="#34495E")
btn_frame.grid(row=2, columnspan=2, pady=20)

btn_login = tk.Button(btn_frame, text="Login", font=("Helvetica", 12, "bold"), bg="#E74C3C", fg="#ECF0F1", width=12, command=login)
btn_login.pack(side=tk.LEFT, padx=5)

btn_register = tk.Button(btn_frame, text="Register", font=("Helvetica", 12), bg="#27AE60", fg="#ECF0F1", width=12, command=open_register)
btn_register.pack(side=tk.LEFT, padx=5)

# Forgot Password Button Centered Below
btn_forgot_password = tk.Button(root, text="Forgot Password?", font=("Helvetica", 10), bg="#3498DB", fg="#ECF0F1", command=open_forgot_password)
btn_forgot_password.pack(pady=5)

root.mainloop()