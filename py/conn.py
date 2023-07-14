import socket
import threading
from outter import Outter
from conn_back import ExternBackgroundWorker
import _shared

# class ExternalConnections:
#     # Class USP: wiki.python.org/moin/UdpCommunication
#     class UDP:
#         def send(ip: str, port: int, msg: str):
#             Outter.out("sec", "Trying to send packet to destination")
#             byte_string = bytes(msg, 'utf-8')
#             sock = socket.socket(socket.AF_INET, # Internet
#                      socket.SOCK_DGRAM) # UDP
#             sock.sendto(byte_string, (ip, port))

#         def wait(ip: str, port: int):
#             sock = socket.socket(socket.AF_INET, # Internet
#                      socket.SOCK_DGRAM) # UDP
#             sock.bind((ip, port))
#             Outter.out("sec", "Beginning to wait for message:")
#             while True:
#                 data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
#                 Outter.out("sec", "received message: %s" % data)
#                 break

class ExternalConnections:
    class TCP:
        def send(ip: str, port: int, msg: str, local_port: int):
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_address = (ip, port)
            local_address = ('', local_port)

            try:
                # Bind the socket to the local address
                sock.bind(local_address)

                # Connect to the server
                sock.connect(server_address)

                # Send the message
                sock.sendall(msg.encode())
                Outter.out("sec", f"TCP message sent to {ip}:{port}")
            finally:
                sock.close()

        def wait(port: int, ip="0.0.0.0"):
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_address = (ip, port)
            data = None

            try:
                # Bind the socket to the server address
                sock.bind(server_address)

                # Listen for incoming connections
                sock.listen(1)
                Outter.out("sec", f"TCP server listening on {ip}:{port}")

                while True:
                    # Accept incoming connection
                    connection, client_address = sock.accept()
                    Outter.out("sec", f"Incoming connection from {client_address[0]}:{client_address[1]}")

                    # Receive and process the message
                    data = connection.recv(1024).decode()
                    Outter.out("sec", f"Received message: {data}")

                    # Close the connection
                    connection.close()
                    Outter.out("sec", "Connection closed.")

            finally:
                sock.close()
                Outter.out("sec", "Stopped")
                return data
            
    class ChitChat:
        
        def startChitChat(ip: str, port: int, local_port: int):
            listening_thread = ExternBackgroundWorker(port)
            _shared.ExternThread = listening_thread
            listening_thread.start()
            while True:
                msg = input(">>")
                if msg == "__END__":
                    _shared.ExternThread.stop_thread()
                    break
                ExternalConnections.TCP.send(ip, port, msg, local_port)