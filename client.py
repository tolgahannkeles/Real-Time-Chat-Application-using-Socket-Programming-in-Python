import socket
import threading


class ClientClass:
    def __init__(self, host="127.0.0.1", port=8081, splitting_char="~"):
        # Initialize the client class
        self.HOST = host
        self.PORT = port
        self.splitting_char = splitting_char
        self.client = None
        self.username = None
        self.on_message_received = None
        self.connected = False

    def _listen_for_messages_from_server(self, callback):
        # Listen for messages from the server
        while self.connected:
            # Receive the message from the server
            try:
                response = self.client.recv(2048).decode('utf-8')  # Receive the message from the server
                if response != '':  # If the response is not empty
                    username = response.split(self.splitting_char)[0]
                    message = response.split(self.splitting_char)[1]
                    callback(f"{username}: {message}")  # Call the callback function
                else:  # If the response is empty
                    print("Received response from server is empty.")
            except ConnectionAbortedError:  # If the connection was aborted
                print("Connection was aborted.")
                self.connected = False  # Set the connected variable to False
                break
            except Exception as e:  # If an error occurred
                print(f"An error occurred: {e}")
                self.connected = False
                break

    def _communicate_to_server(self, username, on_message_received):
        # Communicate with the server
        self.client.sendall(username.encode())  # Send the username to the server
        threading.Thread(target=self._listen_for_messages_from_server, args=(
            on_message_received,)).start()  # Start a new thread to listen for messages from the server

    def send_message_to_server(self, message):
        # Send a message to the server
        if self.client is not None:  # If the client object is not None
            if message != '':
                self.client.sendall(message.encode())
            else:
                raise Exception("Message cannot be sent.")
        else:
            raise Exception("Client object is none.")

    def connect(self, username, on_message_received):
        # Connect to the server
        if self.connected:
            raise Exception("Client is already connected.")  # Raise an exception if the client is already connected

        # Create a new client socket
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.on_message_received = on_message_received
        if username != '':  # If the username is not empty
            self.username = username
            try:
                # Connect to the server
                self.client.connect((self.HOST, self.PORT))
                self.connected = True
                print("Successfully connected to server")
                self._communicate_to_server(username, on_message_received)  # Communicate with the server
            except Exception as e:
                raise Exception(f"Client cannot connect to server {self.HOST}:{self.PORT}: {e}")
        else:
            raise Exception("Username cannot be empty!")

    def disconnect(self):
        # Disconnect from the server
        if self.client:
            self.client.close()
            self.client = None
            self.connected = False
            print("Disconnected from server")
        else:
            raise Exception("Client object is None.")
