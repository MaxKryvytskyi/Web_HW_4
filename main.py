import pathlib
import urllib.parse
import mimetypes
import socket
import json
import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler 
from threading import Thread, Event , RLock

rlock = RLock()
tread_stop = Event()


BASE_DIR = pathlib.Path()
HOST = socket.gethostname()
SOCKET_PORT = 5000


def socet_body(body): # ++++
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket.sendto(body.encode('utf-8'),(HOST, SOCKET_PORT))
    client_socket.close()

class HTTPHandler(BaseHTTPRequestHandler): 
    def do_POST(self): # ++++
        body1 = self.rfile.read(int(self.headers["Content-Length"]))
        body = urllib.parse.unquote_plus(body1.decode())
        socet_body(body)

        self.send_response(302)
        self.send_header("Location", "/")
        self.end_headers()

    def do_GET(self): # ++++
        route = urllib.parse.urlparse(self.path)
        match route.path:
            case "/":
                self.send_html("index.html")
            
            case "/message.html":
                self.send_html("message.html")
            case _:
                file = BASE_DIR / route.path[1:]
                if file.exists():
                    self.send_static(file)
                else:
                    self.send_html("error.html", 404)

    def send_html(self, filename, status_code=200):
        self.send_response(status_code)
        self.send_header("Content-Type", "text/html")
        self.end_headers()
        with open(filename, "rb") as f:    
            self.wfile.write(f.read())

    def send_static(self, filename):
        self.send_response(200)
        mime_type, *rest = mimetypes.guess_type(filename)
        if mime_type: 
            self.send_header("Content-Type", mime_type)
        else:
            self.send_header("Content-Type", "text/plain")

        self.end_headers()
        with open(filename, "rb") as f:    
            self.wfile.write(f.read())

def run_HTTPServer(server=HTTPServer, handler=HTTPHandler):
    address = ("0.0.0.0", 5000)
    http_server = server(address, handler)
    try:
        http_server.serve_forever()
    except KeyboardInterrupt:
        http_server.server_close()


def run_server_socket():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #? socket.AF_INET, socket.SOCK_DGRAM
    server_socket.bind((HOST, SOCKET_PORT))
    conn, address = server_socket.recvfrom(1024)
    payload = conn.decode()
    save_data(payload)
    server_socket.close()

def save_data(payload):

    payload_data = {key: value for key, value in [el.split("=") for el in payload.split("&")]}
    new_data = {f"{datetime.datetime.now()}" : payload_data}
    try:
        with rlock:
            with open('data.json', 'r', encoding="utf-8") as json_file:
                existing_data = json.load(json_file)
    except err
    
    existing_data.update(new_data)

    with rlock:
        with open(BASE_DIR.joinpath("data.json"), "w", encoding="utf-8") as fd:
            json.dump(existing_data, fd, ensure_ascii=False, indent=4)
        

def main():
    http_s = Thread(target=run_HTTPServer)
    socket_s = Thread(target=run_server_socket)
    socket_s.start()
    http_s.start()
    print(socket_s.is_alive())
    print(http_s.is_alive())

if __name__ == "__main__":
    main()