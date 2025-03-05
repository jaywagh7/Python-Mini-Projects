import tkinter as tk
from tkinter import messagebox
from database import Database

db = Database()

class ForgotPasswordWindow:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Forgot Password")
        self.window.geometry("350x300")
        self.window.configure(bg="#34495E")

        tk.Label(self.window, text="Forgot Password", font=("Helvetica", 14, "bold"), bg="#34495E", fg="#ECF0F1").pack(pady=10)
        
        tk.Label(self.window, text="Username:", bg="#34495E", fg="#ECF0F1").pack()
        self.entry_username = tk.Entry(self.window)
        self.entry_username.pack(pady=5)

        tk.Button(self.window, text="Get Security Question", command=self.get_security_question, bg="#E74C3C", fg="white").pack(pady=5)
        
        self.label_question = tk.Label(self.window, text="", bg="#34495E", fg="#ECF0F1")
        self.label_question.pack()

        self.entry_answer = tk.Entry(self.window)
        self.entry_answer.pack(pady=5)

        tk.Label(self.window, text="New Password:", bg="#34495E", fg="#ECF0F1").pack()
        self.entry_new_password = tk.Entry(self.window, show="*")
        self.entry_new_password.pack(pady=5)

        tk.Button(self.window, text="Reset Password", command=self.reset_password, bg="#E74C3C", fg="white").pack(pady=10)

        self.window.mainloop()

    def get_security_question(self):
        username = self.entry_username.get()
        question = db.get_security_question(username)
        if question:
            self.label_question.config(text=question)
        else:
            messagebox.showerror("Error", "Username not found!")

    def reset_password(self):
        username = self.entry_username.get()
        answer = self.entry_answer.get()
        new_password = self.entry_new_password.get()
        
        if db.reset_password(username, answer, new_password):
            messagebox.showinfo("Success", "Password Reset Successfully!")
            self.window.destroy()
        else:
            messagebox.showerror("Error", "Incorrect security answer!")

if __name__ == "__main__":
    ForgotPasswordWindow()
