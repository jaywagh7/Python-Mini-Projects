import tkinter as tk
from tkinter import messagebox
import random
import smtplib
import time
from database import Database

# Initialize database
db = Database("users.db")

class OTPVerification:
    def __init__(self, username):
        self.username = username
        self.user_email = db.get_user_email(username)
        if not self.user_email:
            messagebox.showerror("Error", "Email not found for this user!")
            return

        self.otp = self.generate_otp()
        self.otp_expiry = time.time() + 60  # OTP expires in 60 seconds
        self.attempts = 3

        self.send_otp_email()
        self.create_window()

    def generate_otp(self):
        return str(random.randint(100000, 999999))

    def send_otp_email(self):
        sender_email = "your_email@gmail.com"
        sender_password = "your_password"
        subject = "Your OTP Code"
        body = f"Your OTP code is: {self.otp}\nThis code is valid for 60 seconds."
        message = f"Subject: {subject}\n\n{body}"

        try:
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, self.user_email, message)
            server.quit()
            print("OTP sent successfully.")
        except Exception as e:
            print("Error sending OTP:", e)
            messagebox.showerror("Error", "Failed to send OTP. Please try again.")

    def verify_otp(self):
        entered_otp = self.otp_entry.get()
        if time.time() > self.otp_expiry:
            messagebox.showerror("Error", "OTP expired! Request a new one.")
            return

        if entered_otp == self.otp:
            messagebox.showinfo("Success", "OTP Verified! Login Successful.")
            self.window.destroy()
        else:
            self.attempts -= 1
            if self.attempts > 0:
                messagebox.showerror("Error", f"Invalid OTP! {self.attempts} attempts left.")
            else:
                messagebox.showerror("Error", "Too many failed attempts. Try again later.")
                self.window.destroy()

    def resend_otp(self):
        self.otp = self.generate_otp()
        self.otp_expiry = time.time() + 60  # Reset OTP expiry time
        self.send_otp_email()
        messagebox.showinfo("Success", "New OTP sent to your email!")

    def create_window(self):
        self.window = tk.Toplevel()
        self.window.title("OTP Verification")
        self.window.geometry("300x200")

        tk.Label(self.window, text="Enter OTP sent to your email:").pack(pady=10)
        self.otp_entry = tk.Entry(self.window)
        self.otp_entry.pack(pady=5)

        self.verify_button = tk.Button(self.window, text="Verify", command=self.verify_otp)
        self.verify_button.pack(pady=5)

        self.resend_button = tk.Button(self.window, text="Resend OTP", command=self.resend_otp)
        self.resend_button.pack(pady=5)

        self.timer_label = tk.Label(self.window, text="OTP expires in 60s", fg="red")
        self.timer_label.pack(pady=5)
        self.update_timer()

    def update_timer(self):
        remaining_time = int(self.otp_expiry - time.time())
        if remaining_time > 0:
            self.timer_label.config(text=f"OTP expires in {remaining_time}s")
            self.window.after(1000, self.update_timer)
        else:
            self.timer_label.config(text="OTP Expired! Request a new one.")

# Test the OTP window
if __name__ == "__main__":
    OTPVerification("test_user")