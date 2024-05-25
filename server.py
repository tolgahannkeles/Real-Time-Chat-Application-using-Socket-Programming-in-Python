import socket
import threading

HOST = "127.0.0.1"
PORT = 8081
LISTENER_LIMIT = 3
active_clients = []  # list of all connected clients
splitting_char = "~"


# Function to send a message to all clients
def send_message_to_all(message):
    for user in active_clients:
        send_message_to_a_client(client=user[1], message=message)


# Function to listen for any coming messages from a client
def listen_for_messages(client, username):
    while True:
        try:
            message = client.recv(2048).decode('utf-8')
            if message != '':
                final_message = username + splitting_char + message
                print(f"[{username}] {message}")
                send_message_to_all(final_message)
            else:
                print(f"received message from the client {username} is empty")
                break  # Add this line to break the loop when an empty message is received
        except ConnectionResetError:
            print(f"Connection with {username} was forcibly closed.")
            active_clients.remove((username, client))
            break
        except Exception as e:
            print(f"An error occurred: {e}")
            break

def send_message_to_a_client(client, message):
    client.sendall(message.encode())


# Function to handle clients
def client_handler(client):
    # Loop to take the username
    while True:
        username = client.recv(2048).decode('utf-8')

        if username != '':
            active_clients.append((username, client))
            send_message_to_all(f"Server{splitting_char}{username} has joined to chat.")
            break
        else:
            print("Client username is null")

    threading.Thread(target=listen_for_messages, args=(client, username,)).start()


def main():
    # Creating server socket
    # AF_INET: when you use ipv4, select this type
    # SOCK_STREAM: when you use TCP, select this one
    # SOCK_DGRAM: when you use UDP, select this one
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Provide the server with an address in the form of host IP, port number
        server_socket.bind((HOST, PORT))
        print(f"Server is running on {HOST}:{PORT}")
    except:
        print(f"Unable to bind host:{HOST} port:{PORT}")

    server_socket.listen(LISTENER_LIMIT)

    # this while loop will keep listening to client connections
    while True:
        # accepts any connection request
        client, address = server_socket.accept()
        print(f"Successfully connected to the client {address[0]}:{address[1]}")

        # Creating a thread for each client to handle it
        threading.Thread(target=client_handler, args=(client,)).start()


if __name__ == "__main__":
    main()
