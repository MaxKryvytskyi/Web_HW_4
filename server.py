import socket

def main():
    print("22")
    host = socket.gethostname()
    print("23")
    port = 5000
    print("24")

    server_socket = socket.socket()
    print("25")
    server_socket.bind((host, port))
    print("26")
    server_socket.listen()
    print("27")

    conn, address = server_socket.accept()
    print("28")

    print(f"Connection from: {address}")
    print("29")
    while True:
        print("30")
        msg = conn.recv(100).decode()
        print("31")
        if not msg:
            print("32")
            break
        print("33")
        print(f"Received message: {msg}")
        print("34")
        message = input("--> ")
        print("35")
        conn.send(message.encode())
        print("36")
    print("37")
    conn.close()
    print("38")
    server_socket.close()


if __name__ == "__main__":
    print("21")
    main()