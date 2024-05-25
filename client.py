import socket
import threading


class ClientClass:
    def __init__(self, host="127.0.0.1", port=8081, splitting_char="~"):
        self.HOST = host
        self.PORT = port
        self.splitting_char = splitting_char
        self.client = None
        self.username = None
        self.onMessageReceived=None
        self.connected = False

    def _listen_for_messages_from_server(self, callback):
        while self.connected:
            try:
                response = self.client.recv(2048).decode('utf-8')
                if response != '':
                    username = response.split(self.splitting_char)[0]
                    message = response.split(self.splitting_char)[1]
                    callback(f"{username}: {message}")
                    print(f"{username}: {message}")
                else:
                    print("Received response from server is empty.")
            except ConnectionAbortedError:
                print("Connection was aborted.")
                self.connected = False
                break
            except Exception as e:
                print(f"An error occurred: {e}")
                self.connected = False
                break

    def _communicate_to_server(self, username, onMessageReceived):
        self.client.sendall(username.encode())
        threading.Thread(target=self._listen_for_messages_from_server, args=(onMessageReceived,)).start()

    def send_message_to_server(self, message):
        if self.client is not None:
            if message != '':
                coded_message = self.username + self.splitting_char + message
                try:
                    self.client.sendall(message.encode())
                except:
                    raise Exception("Message cannot be sent.")
            else:
                raise Exception("Message cannot be sent.")
        else:
            raise Exception("Client object is none.")

    def connect(self, username, onMessageReceived):
        if self.connected:
            print("Already connected to the server.")
            return

        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.onMessageReceived = onMessageReceived
        if username != '':
            self.username = username
            try:
                self.client.connect((self.HOST, self.PORT))
                self.connected = True
                print("Successfully connected to server")
                self._communicate_to_server(username, onMessageReceived)

            except Exception as e:
                print(f"Client cannot connect to server {self.HOST}:{self.PORT}")
                print(f"Error: {e}")
                return
        else:
            raise Exception("Username cannot be empty!")

    def disconnect(self):
        if self.client:
            self.client.close()
            self.client = None
            self.connected = False
            print("Disconnected from server")
