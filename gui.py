import tkinter as tk
from tkinter import scrolledtext
from tkinter import simpledialog
import threading
import client


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


def create_menu(root, nick_var):
    menu_bar = tk.Menu(root)
    root.config(menu=menu_bar)

    file_menu = tk.Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="Chat", menu=file_menu)

    file_menu.add_command(label="Connect", command=on_connect_click)
    file_menu.add_command(label="Disconnect", command=on_disconnect_click)
    file_menu.add_command(label="Change nickname", command=lambda: on_change_nick_click(root, nick_var))


def on_change_nick_click(root, nick_var):
    nick = ask_nick(root)
    if nick:
        nick_var.set(nick)


def ask_nick(root):
    nick = simpledialog.askstring("Nick", "Please enter your nick:")
    if nick:
        print(f"Nick: {nick}")
        return nick
    else:
        root.destroy()


def on_connect_click():
    global client_socket, receive_thread
    print("Connect clicked")
    if not client_socket:  # Only connect if no existing socket
        client_socket = client.connect_to_server()
        receive_thread = threading.Thread(target=receive_messages)
        receive_thread.daemon = True
        receive_thread.start()

def on_disconnect_click():
    global client_socket, receive_thread
    print("Disconnect clicked")
    if client_socket:
        client.disconnect_from_server(client_socket)
        client_socket = None  # Set to None after disconnect

def create_message_send_box(root, text_box, nick_var):
    message_field = tk.Entry(root)
    message_field.pack(side=tk.LEFT, expand=True, fill='both', padx=10, pady=10)
    add_placeholder(message_field, 'Enter your message here...')

    button = tk.Button(root, text="Submit",
                       command=lambda: send_message(nick_var.get(), message_field.get(), text_box=text_box,
                                                    message_field=message_field))
    button.pack(side=tk.LEFT, padx=10, pady=10)


def send_message(nick, text, text_box, message_field):
    print(f"Send button clicked. Message: {text} from {nick}")
    if text.strip():
        client.send_message(client_socket, f"{nick}: {text}")
        text_box.insert(tk.END, f"{nick}: {text}\n")
        message_field.delete(0, tk.END)


def receive_messages():
    global client_socket
    while client_socket:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                raise ConnectionError("Connection closed by the server.")
            text_box.insert(tk.END, f"{message}\n")
        except ConnectionError:
            print("Connection closed by the server.")
            break
        except Exception as e:
            print(f"Error receiving message: {e}")
            break
def main():
    global text_box, client_socket
    client_socket = None

    root = tk.Tk()
    root.withdraw()  # Hide the root window
    nick = ask_nick(root)
    if not nick:
        return
    # If the nick was provided, show the main window
    root.deiconify()
    root.title("COMP308 Final Project Chat Client")

    nick_var = tk.StringVar(value=nick)
    create_menu(root, nick_var)

    text_box = scrolledtext.ScrolledText(root)
    text_box.pack()

    create_message_send_box(root, text_box, nick_var)

    root.mainloop()


if __name__ == "__main__":
    main()
