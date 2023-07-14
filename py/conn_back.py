import socket
import threading
from outter import Outter

class ExternBackgroundWorker(threading.Thread):
    def __init__(self, localport):
        super().__init__()
        self._stop_event = threading.Event()
        self.local_port = localport

    def run(self):
        while not self._stop_event.is_set():

            # Add your continuous thread logic here
            print("Thread is running...")

            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_address = ("0.0.0.0", self.local_port)
            data = None

            try:
                # Bind the socket to the server address
                sock.bind(server_address)

                # Listen for incoming connections
                sock.listen(1)
                Outter.out("sec", f"TCP server listening on 0.0.0.0:{self.local_port}")

                while True:
                    # Accept incoming connection
                    connection, client_address = sock.accept()
                    Outter.out("sec", f"Incoming connection from {client_address[0]}:{client_address[1]}")

                    # Receive and process the message
                    data = connection.recv(1024).decode()
                    Outter.out("sec", f"Received message: {data}")

                    # Send the mesage to the user
                    Outter.out("pri", f"{client_address[0]}: {data}")

                    # Close the connection
                    connection.close()
                    Outter.out("sec", "Connection closed.")

            finally:
                sock.close()
                Outter.out("sec", "Stopped")




    def stop_thread(self):
        self._stop_event.set()