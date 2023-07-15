import socket
import threading
from outter import Outter
# from runline import runline

class CustomBackgroundWorker(threading.Thread):
    def __init__(self, localport, command):
        super().__init__()
        self._stop_event = threading.Event()
        self.local_port = localport
        self.command = command

    def run(self):
        # Add your continuous thread logic here
        Outter.out("net", "Thread is running")

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = ("0.0.0.0", self.local_port)
        data = None

        try:
            # Bind the socket to the server address
            sock.bind(server_address)

            # Listen for incoming connections
            sock.listen(1)
            Outter.out("net", f"TCP server listening on 0.0.0.0:{self.local_port}")

            while not self._stop_event.is_set():
                # Accept incoming connection
                connection, client_address = sock.accept()
                Outter.out("net", f"Incoming connection from {client_address[0]}:{client_address[1]}")

                # Receive and process the message
                data = connection.recv(1024).decode()
                Outter.out("net", f"Received message: {data}")

                # Close the connection
                connection.close()
                Outter.out("net", "Connection closed.")

                # runline(self.command.replace('$WORKER_OUT', data))

        finally:
            sock.close()
            Outter.out("net", "Stopped")
                
    def stop_thread(self):
        self._stop_event.set()