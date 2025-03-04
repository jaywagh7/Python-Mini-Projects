import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import requests
from io import BytesIO

# Function to manage the login
def login():
    username = entry_username.get()
    password = entry_password.get()
    
    # Hardcoded credentials for demonstration
    if username == "admin" and password == "password":
        messagebox.showinfo("Login Success", "Welcome, Jay!")
    else:
        messagebox.showerror("Login Failed", "Invalid Username or Password")

# Creating the main window
root = tk.Tk()
root.title("Login System")
root.geometry("400x450")
root.configure(bg="#2C3E50")

# Load an image from an online source
img_url = "https://cdn-icons-png.flaticon.com/512/5087/5087579.png"  # Replace with any valid image URL
response = requests.get(img_url)
img_data = Image.open(BytesIO(response.content))
img_data = img_data.resize((80, 80), Image.LANCZOS)  # Replaced ANTIALIAS with LANCZOS
img = ImageTk.PhotoImage(img_data)

# Display the image
img_label = tk.Label(root, image=img, bg="#2C3E50")
img_label.pack(pady=10)

# Styling Elements
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


btn_login = tk.Button(frame, text="Login", font=("Helvetica", 12, "bold"), bg="#E74C3C", fg="#ECF0F1", width=15, command=login)
btn_login.grid(row=2, columnspan=2, pady=20)


root.mainloop()
