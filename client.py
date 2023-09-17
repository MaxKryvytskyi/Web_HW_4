import socket

def main():
    print("2")
    host = socket.gethostname()
    print("3")
    port = 5000
    print("4")

    client_socket = socket.socket()
    print("5")
    client_socket.connect((host, port))
    print("6")
    message = input("--> ")

    while message.lower().strip() != "exit":
        print("7")
        client_socket.send(message.encode())
        print("8")
        msg = client_socket.recv(1024).decode()
        print("9")
        print(f"Received message: {msg}")
        print("10")
        message = input("--> ")
        print("11")
    client_socket.close()
    print("12")


if __name__ == "__main__":
    print("1")
    main()