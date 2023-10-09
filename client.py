import socket

HOST = "127.0.0.1"
PORT = 11111

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

message = input("Enter something to send : ")

client_socket.send(message.encode())
print("Message sent")

print("\n___________________________\n")

client_socket.close()