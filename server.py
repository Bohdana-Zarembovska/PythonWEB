import socket
from datetime import datetime
import time

HOST = "127.0.0.1"
PORT = 11111

def printMessage(message: bytes):
    print("\n___________________________\n")
    print(f"\t[Message] - {message.decode()}")
    print(f"\t[Time] - {datetime.now()}")

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.bind((HOST, PORT))

server_socket.listen(1)

connection, client_address = server_socket.accept()
print(f"[Accepted from {client_address}]")

message = bytes()

message = connection.recv(1024)
if not message:
    print("[Receive error]: empty message")

printMessage(message)

connection.close()