import string
import random
from tkinter import *
from tkinter import messagebox
import sqlite3

# Initialize SQLite database
with sqlite3.connect("users.db") as db:
    cursor = db.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS users(Username TEXT NOT NULL, GeneratedPassword TEXT NOT NULL);")
db.commit()
db.close()

class PasswordGeneratorApp:
    def __init__(self, master):
        self.master = master
        self.n_username = StringVar()
        self.n_passwordlen = IntVar()
        self.n_generatedpassword = StringVar()

        self.master.title("Password Generator")
        self.master.geometry("700x550")
        self.master.config(bg="#333333")
        self.master.resizable(False, False)

        # Header
        self.label = Label(
            self.master,
            text="PASSWORD GENERATOR",
            fg="#FFFFFF",
            bg="#333333",
            font="Helvetica 22 bold underline"
        )
        self.label.pack(pady=20)

        # User input frame
        input_frame = Frame(self.master, bg="#333333")
        input_frame.pack(pady=10)

        self.user_label = Label(
            input_frame,
            text="Enter Username:",
            font="Helvetica 14",
            fg="#FFFFFF",
            bg="#333333"
        )
        self.user_label.grid(row=0, column=0, padx=10, pady=10)

        self.user_entry = Entry(
            input_frame,
            textvariable=self.n_username,
            font="Helvetica 14",
            bd=5,
            relief="ridge",
        )
        self.user_entry.grid(row=0, column=1, padx=10, pady=10)

        self.length_label = Label(
            input_frame,
            text="Password Length:",
            font="Helvetica 14",
            fg="#FFFFFF",
            bg="#333333"
        )
        self.length_label.grid(row=1, column=0, padx=10, pady=10)

        self.length_entry = Entry(
            input_frame,
            textvariable=self.n_passwordlen,
            font="Helvetica 14",
            bd=5,
            relief="ridge",
        )
        self.length_entry.grid(row=1, column=1, padx=10, pady=10)

        # Generated password display
        self.generated_label = Label(
            input_frame,
            text="Generated Password:",
            font="Helvetica 14",
            fg="#FFFFFF",
            bg="#333333"
        )
        self.generated_label.grid(row=2, column=0, padx=10, pady=10)

        self.generated_entry = Entry(
            input_frame,
            textvariable=self.n_generatedpassword,
            font="Helvetica 14 bold",
            bd=5,
            relief="ridge",
            fg="#DC143C",
            state="readonly"
        )
        self.generated_entry.grid(row=2, column=1, padx=10, pady=10)

        # Buttons
        button_frame = Frame(self.master, bg="#333333")
        button_frame.pack(pady=20)

        self.generate_button = Button(
            button_frame,
            text="Generate Password",
            font="Helvetica 14 bold",
            bg="#5CB85C",
            fg="#FFFFFF",
            padx=10,
            pady=5,
            command=self.generate_pass
        )
        self.generate_button.grid(row=0, column=0, padx=20)

        self.accept_button = Button(
            button_frame,
            text="Accept",
            font="Helvetica 14 bold",
            bg="#5BC0DE",
            fg="#FFFFFF",
            padx=10,
            pady=5,
            command=self.accept_fields
        )
        self.accept_button.grid(row=0, column=1, padx=20)

        self.reset_button = Button(
            button_frame,
            text="Reset",
            font="Helvetica 14 bold",
            bg="#D9534F",
            fg="#FFFFFF",
            padx=10,
            pady=5,
            command=self.reset_fields
        )
        self.reset_button.grid(row=0, column=2, padx=20)

    def generate_pass(self):
        upper = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        lower = "abcdefghijklmnopqrstuvwxyz"
        chars = "@#%&()\"?!"
        numbers = "1234567890"

        name = self.n_username.get()
        try:
            length = int(self.n_passwordlen.get())
        except ValueError:
            messagebox.showerror("Error", "Password length must be a number.")
            return

        if not name:
            messagebox.showerror("Error", "Username cannot be empty.")
            return

        if length < 6:
            messagebox.showerror("Error", "Password must be at least 6 characters long.")
            return

        # Generate password
        components = [
            random.sample(upper, random.randint(1, max(1, length - 3))),
            random.sample(lower, random.randint(1, max(1, length - 3))),
            random.sample(chars, random.randint(1, max(1, length - 3))),
            random.sample(numbers, max(1, length - 3))
        ]
        password = [char for group in components for char in group]
        random.shuffle(password)
        self.n_generatedpassword.set("".join(password[:length]))

    def accept_fields(self):
        with sqlite3.connect("users.db") as db:
            cursor = db.cursor()
            find_user = "SELECT * FROM users WHERE Username = ?"
            cursor.execute(find_user, (self.n_username.get(),))

            if cursor.fetchone():
                messagebox.showerror("Error", "This username already exists! Please use another username.")
                return

            insert_query = "INSERT INTO users (Username, GeneratedPassword) VALUES (?, ?)"
            cursor.execute(insert_query, (self.n_username.get(), self.n_generatedpassword.get()))
            db.commit()
            messagebox.showinfo("Success!", "Password saved successfully.")

    def reset_fields(self):
        self.n_username.set("")
        self.n_passwordlen.set("")
        self.n_generatedpassword.set("")

if __name__ == "__main__":
    root = Tk()
    app = PasswordGeneratorApp(root)
    root.mainloop()
