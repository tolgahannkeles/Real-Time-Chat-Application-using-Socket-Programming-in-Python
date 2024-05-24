import socket
import threading


def connect_to_server(host='127.0.0.1', port=8081):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    return client_socket

def disconnect_from_server(client_socket):
    try:
        client_socket.shutdown(socket.SHUT_RDWR)
        client_socket.close()  # Soketi kapat
    except Exception as e:
        print(f"Error during shutdown: {e}")

def send_message(client_socket, message):
    try:
        client_socket.sendall(message.encode('utf-8'))
    except Exception as e:
        print(f"Error sending message: {e}")

def receive_message(client_socket):
    try:
        message = client_socket.recv(1024).decode('utf-8')
        if not message:
            raise ConnectionError("Connection closed by the server.")
        return message
    except Exception as e:
        print(f"Error receiving message: {e}")
        raise