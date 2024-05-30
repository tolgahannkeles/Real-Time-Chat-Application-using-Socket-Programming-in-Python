import socket
import threading


class Server:
    def __init__(self, host="127.0.0.1", port=8081, listener_limit=3, splitting_char="~"):
        # Initialize the server class
        self.HOST = host  # Host IP address to listen for incoming connections
        self.PORT = port  # Port number to listen for incoming connections
        self.LISTENER_LIMIT = listener_limit  # Maximum number of clients that can connect to the server
        self.splitting_char = splitting_char  # Splitting character to separate the username and message
        self.active_clients = []  # List to store the active clients

    def send_message_to_all(self, message):
        # Send a message to all clients
        for user in self.active_clients:  # Iterate through the active clients
            self.send_message_to_a_client(client=user[1], message=message)  # Send the message to the client

    def listen_for_messages(self, client, username):  # Listen for messages from the client
        while True:
            try:
                message = client.recv(2048).decode('utf-8')  # Receive the message from the client
                if message != '':  # If the message is not empty
                    final_message = username + self.splitting_char + message
                    self.send_message_to_all(final_message)  # Send the message to all clients
                else:
                    print(f"Received message from the client {username} is empty")
                    break
            except ConnectionResetError:
                print(f"Connection with {username} was forcibly closed.")
                self.active_clients.remove((username, client))
                self.send_message_to_all(f"Server{self.splitting_char}{username} has left the chat.")
                break
            except Exception as e:
                print(f"An error occurred: {e}")
                break

    @staticmethod
    def send_message_to_a_client(client, message):
        # Send a message to a client
        client.sendall(message.encode())  # Send the message to the client

    def client_handler(self, client):
        # Handle the client connection
        while True:
            username = client.recv(2048).decode('utf-8')  # Receive the username from the client

            if username != '':  # If the username is not empty
                self.active_clients.append((username, client))  # Add the client to the active clients list
                self.send_message_to_all(f"Server{self.splitting_char}{username} has joined to chat.")
                break
            else:
                print("Client username is null")

        threading.Thread(target=self.listen_for_messages,
                         args=(client, username,)).start()  # Start a new thread to listen for messages from the client

    def main(self):
        # Creating server socket
        # AF_INET: when you use ipv4, select this type
        # SOCK_STREAM: when you use TCP, select this one
        # SOCK_DGRAM: when you use UDP, select this one
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            server_socket.bind((self.HOST, self.PORT))  # Bind the host and port to the server socket
            print(f"Server is running on {self.HOST}:{self.PORT}")
        except Exception as e:
            print(f"Cannot bind the host and port to the server socket: {e}")
            return

        server_socket.listen(self.LISTENER_LIMIT)  # Listen for incoming connections

        while True:
            client, address = server_socket.accept()  # Accept the incoming connection
            threading.Thread(target=self.client_handler,
                             args=(client,)).start()  # Start a new thread to handle the client connection


if __name__ == "__main__":
    server = Server()
    server.main()
