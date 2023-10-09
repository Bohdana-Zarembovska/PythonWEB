import socket

HOST = "127.0.0.1"
PORT = 11111

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))
while True:
    message = input("Enter something to send (type 'CLOSE' to exit): ")

    if message == "CLOSE":
        client_socket.send(message.encode())
        break
    
    client_socket.send(message.encode())
    print("Message sent")

    echo_message = client_socket.recv(1024)

    print(f"[Echo message] - {echo_message.decode()}")
    print("\n___________________________\n")

client_socket.close()