import tkinter as tk
from tkinter import messagebox
import random
import smtplib
from database import Database

db = Database()

def send_otp(email):
    otp = random.randint(100000, 999999)
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login("your_email@gmail.com", "your_email_password")
        message = f"Subject: Your OTP Code\n\nYour OTP is: {otp}"
        server.sendmail("your_email@gmail.com", email, message)
        server.quit()
        return otp
    except Exception as e:
        messagebox.showerror("Error", f"Failed to send OTP: {str(e)}")
        return None

class OTPVerification:
    def __init__(self, username):
        self.username = username
        self.window = tk.Tk()
        self.window.title("OTP Verification")
        self.window.geometry("350x250")
        self.window.configure(bg="#34495E")

        user_email = db.get_user_email(username)
        if not user_email:
            messagebox.showerror("Error", "Email not found!")
            self.window.destroy()
            return

        self.otp = send_otp(user_email)
        
        tk.Label(self.window, text="Enter OTP sent to your email", font=("Helvetica", 12), bg="#34495E", fg="#ECF0F1").pack(pady=10)
        self.entry_otp = tk.Entry(self.window)
        self.entry_otp.pack(pady=5)

        tk.Button(self.window, text="Verify", command=self.verify_otp, bg="#E74C3C", fg="white").pack(pady=10)

        self.window.mainloop()

    def verify_otp(self):
        user_otp = self.entry_otp.get()
        if str(self.otp) == user_otp:
            messagebox.showinfo("Success", "OTP Verified! Login Successful.")
            self.window.destroy()
        else:
            messagebox.showerror("Error", "Invalid OTP!")

if __name__ == "__main__":
    OTPVerification("test_user")
