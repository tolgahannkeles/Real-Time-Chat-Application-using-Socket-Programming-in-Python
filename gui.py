import tkinter as tk
from tkinter import scrolledtext
from tkinter import simpledialog, messagebox
import client


class ChatClientUI:
    def __init__(self):
        # Create the main window
        self.root = tk.Tk()
        self.root.geometry("500x450")
        self.root.title("COMP308 Final Project Chat Client")
        self.root.resizable(False, False)
        self.client = client.ClientClass()
        self.text_box = scrolledtext.ScrolledText(self.root)  # text_box is now an attribute of the class
        self.text_box.config(state=tk.DISABLED)
        self.text_box.pack()

    def create_message_send_box(self):
        # Create a message box
        def add_placeholder(entry, placeholder):
            # Add placeholder text to the entry
            entry.insert(0, placeholder)
            entry.config(fg='grey')

            # Bind the functions to the entry
            def on_focus_in(event):
                if entry.get() == placeholder:
                    entry.delete(0, tk.END)
                    entry.config(fg='black')

            # Add this function to clear the placeholder text when the entry is focused
            def on_focus_out(event):
                if entry.get() == '':
                    entry.insert(0, placeholder)
                    entry.config(fg='grey')

            # Add these bindings to the entry
            entry.bind("<FocusIn>", on_focus_in)
            entry.bind("<FocusOut>", on_focus_out)

        # Create a message box
        message_field = tk.Entry(self.root)
        message_field.pack(side=tk.LEFT, expand=True, fill='both', padx=10, pady=10)
        add_placeholder(message_field, 'Enter your message here...')
        # Create a submit button
        button = tk.Button(self.root, text="Submit",
                           command=lambda: self.send_message(message_field.get(), message_field=message_field))
        button.pack(side=tk.LEFT, padx=10, pady=10)

    def create_menu(self):
        # Create a menu bar
        menu_bar = tk.Menu(self.root)
        self.root.config(menu=menu_bar)
        file_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Connection", menu=file_menu)
        # Add the connect and disconnect commands to the menu
        file_menu.add_command(label="Connect", command=self.on_connect_click)
        file_menu.add_command(label="Disconnect", command=self.on_disconnect_click)

    def ask_nick(self):
        # Ask the user for a nick
        while True:
            # Ask the user for a nick with a dialog box
            nick = simpledialog.askstring("Nick", "Please enter your nick:", parent=self.root)
            if nick:  # If the user enters a nick
                return nick
            elif nick is None:  # If the user clicks the cancel button
                return None
            else:  # If the user clicks the OK button without entering a nick
                self.show_warning("Nick cannot be empty. Please enter your nick.")

    def send_message(self, text, message_field):
        # Send the message to the server
        if text.strip():
            try:
                self.client.send_message_to_server(text)
                message_field.delete(0, tk.END)
            except Exception as e:
                self.show_warning(f"You need to connect to the server first: {e}")

    def on_message_received(self, message):
        # Display the message in the text box
        self.text_box.config(state=tk.NORMAL)
        self.text_box.insert(tk.END, f"{message}\n")
        self.text_box.config(state=tk.DISABLED)

    def on_connect_click(self):
        # Connect to the server
        nick = self.ask_nick()
        if not nick:  # If the user clicks the cancel button
            return
        try:
            self.client.connect(nick, on_message_received=self.on_message_received)
        except Exception as e:
            self.show_error(f"Cannot connect to server: {e}")

    def on_disconnect_click(self):
        # Disconnect from the server
        try:
            self.client.disconnect()
        except Exception as e:
            self.show_error(f"Cannot disconnect from server: {e}")

    @staticmethod
    def show_warning(message):
        # Show an error message
        messagebox.showwarning("Warning", message)

    @staticmethod
    def show_error(message):
        # Show an error message
        messagebox.showerror("Error", message)

    def main(self):
        self.create_menu()
        self.create_message_send_box()
        self.root.mainloop()


if __name__ == "__main__":
    ui = ChatClientUI()
    ui.main()
