import socket
import threading
import tkinter as tk
from tkinter import scrolledtext

def receive_messages(client_socket, text_box):
    while True:
        data = client_socket.recv(1024)
        if not data:
            break
        message = data.decode('utf-8')
        text_box.insert(tk.END, f"{message}\n")

def send_message(client_socket, user_field, entry_field, text_box):
    message = entry_field.get()
    user = user_field.get()
    message = f"{user}: {message}"
    client_socket.sendall(message.encode('utf-8'))
    text_box.insert(tk.END, f"{message}\n")
    entry_field.delete(0, tk.END)

def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = '127.0.0.1'
    port = 8081
    client_socket.connect((host, port))

    root = tk.Tk()
    root.title("Chat Client")

    text_box = scrolledtext.ScrolledText(root)
    text_box.pack()

    entry_field = tk.Entry(root)
    entry_field.pack(side=tk.LEFT)

    user_field = tk.Entry(root)
    user_field.pack(side=tk.LEFT)

    send_button = tk.Button(root, text="Send",
                            command=lambda: send_message(client_socket, user_field, entry_field, text_box))
    send_button.pack(side=tk.RIGHT)

    receive_thread = threading.Thread(target=receive_messages, args=(client_socket, text_box))
    receive_thread.start()

    root.mainloop()

if __name__ == "__main__":
    main()