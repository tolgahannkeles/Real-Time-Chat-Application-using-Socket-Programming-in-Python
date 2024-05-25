import threading
import tkinter as tk
from tkinter import scrolledtext
from tkinter import simpledialog, messagebox
import client


class ChatClientUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("500x450")
        self.root.title("COMP308 Final Project Chat Client")
        self.root.resizable(False, False)
        self.client = client2.ClientClass()
        self.text_box = scrolledtext.ScrolledText(self.root)  # text_box is now an attribute of the class
        self.text_box.config(state=tk.DISABLED)
        self.text_box.pack()

    def create_message_send_box(self, text_box):
        def add_placeholder(entry, placeholder):
            entry.insert(0, placeholder)
            entry.config(fg='grey')

            def on_focus_in(event):
                if entry.get() == placeholder:
                    entry.delete(0, tk.END)
                    entry.config(fg='black')

            def on_focus_out(event):
                if entry.get() == '':
                    entry.insert(0, placeholder)
                    entry.config(fg='grey')

            entry.bind("<FocusIn>", on_focus_in)
            entry.bind("<FocusOut>", on_focus_out)

        message_field = tk.Entry(self.root)
        message_field.pack(side=tk.LEFT, expand=True, fill='both', padx=10, pady=10)
        add_placeholder(message_field, 'Enter your message here...')

        button = tk.Button(self.root, text="Submit",
                           command=lambda: self.send_message(message_field.get(),message_field=message_field))
        button.pack(side=tk.LEFT, padx=10, pady=10)

    def create_menu(self):
        menu_bar = tk.Menu(self.root)
        self.root.config(menu=menu_bar)
        file_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Chat", menu=file_menu)
        file_menu.add_command(label="Connect", command=self.on_connect_click)
        file_menu.add_command(label="Disconnect", command=self.on_disconnect_click)

    def ask_nick(self):
        while True:
            nick = simpledialog.askstring("Nick", "Please enter your nick:", parent=self.root)
            if nick:
                return nick
            elif nick is None:  # Cancel veya çarpı tuşuna basıldığında None döner
                return None
            else:
                messagebox.showwarning("Warning", "Nick cannot be empty. Please enter your nick.")

    def send_message(self, text, message_field):
        if text.strip():
            try:
                self.client.send_message_to_server(text)
                message_field.delete(0, tk.END)
            except:
                pass

    def on_connect_click(self):
        nick = self.ask_nick()
        if not nick:
            return
        try:
            self.client.connect(nick, onMessageReceived=self.onMessageReceived)
        except Exception as e:
            print(f"Cannot connect to server: {e}")

    def onMessageReceived(self, message):
        print("nesaaaaaaaa + " + message)
        self.text_box.config(state=tk.NORMAL)
        self.text_box.insert(tk.END, f"{message}\n")
        self.text_box.config(state=tk.DISABLED)

    def on_disconnect_click(self):
        try:
            self.client.disconnect()
        except Exception as e:
            print(f"Cannot disconnect from server: {e}")

    def main(self):
        self.create_menu()
        self.create_message_send_box(self.text_box)  # Add this line
        #text_box = scrolledtext.ScrolledText(self.root)
        #text_box.config(state=tk.DISABLED)
        #text_box.pack()

        self.root.mainloop()


if __name__ == "__main__":
    ui = ChatClientUI()
    ui.main()
