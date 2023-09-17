import pathlib
import urllib.parse
import mimetypes
import socket
import json
import datetime
import logging
from http.server import HTTPServer, BaseHTTPRequestHandler 
from threading import Thread, Event , RLock

rlock = RLock()
event_stop = Event()

BASE_DIR = pathlib.Path()
HOST = socket.gethostname()
HOST_0 = "0.0.0.0"
SOCKET_PORT = 5000
HTTP_PORT = 3000
BUFER_1024 = 1024
STATUS_200 = 200
STATUS_404 = 404
STATUS_302 = 302

def sending_in_socket(body):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket.sendto(body.encode(),(HOST, SOCKET_PORT))
    client_socket.close()

class HTTPHandler(BaseHTTPRequestHandler): 
    def do_POST(self): 
        body1 = self.rfile.read(int(self.headers["Content-Length"]))
        body = urllib.parse.unquote_plus(body1.decode())

        sending_in_socket(body)

        self.send_response(STATUS_302)
        self.send_header("Location", "/")
        self.end_headers()

    def do_GET(self): 
        route = urllib.parse.urlparse(self.path)
        match route.path:
            case "/":
                self.send_html("HTML/index.html")
            
            case "/message.html":
                self.send_html("HTML/message.html")
            case _:
                file = BASE_DIR / route.path[1:]
                if file.exists():
                    self.send_static(file)
                else:
                    self.send_html("HTML/error.html", STATUS_404)

    def send_html(self, filename, status_code=STATUS_200):
        self.send_response(status_code)
        self.send_header("Content-Type", "text/html")
        self.end_headers()
        with open(filename, "rb") as f:    
            self.wfile.write(f.read())

    def send_static(self, filename):
        self.send_response(STATUS_200)
        mime_type, *_ = mimetypes.guess_type(filename)
        if mime_type: 
            self.send_header("Content-Type", mime_type)
        else:
            self.send_header("Content-Type", "text/plain")

        self.end_headers()
        with open(filename, "rb") as f:    
            self.wfile.write(f.read())

def run_HTTPServer(server=HTTPServer, handler=HTTPHandler):
    logging.info("Starts HTTP Server")
    address = (HOST_0, HTTP_PORT)
    http_server = server(address, handler)
    try:
        http_server.serve_forever()
    except KeyboardInterrupt:
        logging.info("Stops HTTP Server")
        http_server.server_close()


def run_server_socket():
    logging.info("Starts Socket Server")
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
    server_socket.bind((HOST, SOCKET_PORT))
    try:
        while not event_stop.is_set():
            conn, address = server_socket.recvfrom(BUFER_1024)
            payload = conn.decode()
            logging.info(f"{address}")
            if not payload:
                break
            save_data(payload)
        
    except KeyboardInterrupt:
        pass
    finally:
        logging.info("Stop Socket Server")
        server_socket.close()

def save_data(payload):
    logging.info("Start Saves")

    with rlock:
        with open(BASE_DIR.joinpath("data/storage/data.json"), "r", encoding="utf-8") as json_file:
            try:
                data = json.load(json_file)
            except json.decoder.JSONDecodeError:
                data = {}
            except FileNotFoundError:
                data = {}

    payload_data = {key: value for key, value in [el.split("=") for el in payload.split("&")]}
    new_data = {f"{datetime.datetime.now()}" : payload_data}
    data.update(new_data)

    with rlock:
        with open(BASE_DIR.joinpath("data/storage/data.json"), "w", encoding="utf-8") as fd:
            json.dump(data, fd, ensure_ascii=False, indent=4)
        

def main():
    http_s = Thread(target=run_HTTPServer)
    socket_s = Thread(target=run_server_socket)
    socket_s.start()
    http_s.start()
    event_stop.wait()
    socket_s.join()
    http_s.join()

if __name__ == "__main__":
    logging.basicConfig(
    format='%(asctime)s %(message)s',
    level=logging.INFO,
        handlers=[
        logging.FileHandler("program.log"),
        logging.StreamHandler()
    ])
    main()