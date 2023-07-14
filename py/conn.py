import socket

# class ExternalConnections:
#     # Class USP: wiki.python.org/moin/UdpCommunication
#     class UDP:
#         def send(ip: str, port: int, msg: str):
#             print("Trying to send packet to destination")
#             byte_string = bytes(msg, 'utf-8')
#             sock = socket.socket(socket.AF_INET, # Internet
#                      socket.SOCK_DGRAM) # UDP
#             sock.sendto(byte_string, (ip, port))

#         def wait(ip: str, port: int):
#             sock = socket.socket(socket.AF_INET, # Internet
#                      socket.SOCK_DGRAM) # UDP
#             sock.bind((ip, port))
#             print("Beginning to wait for message:")
#             while True:
#                 data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
#                 print("received message: %s" % data)
#                 break

class ExternalConnections:
    class TCP:
        def send(ip: str, port: int, msg: str):
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_address = (ip, port)

            try:
                # Connect to the server
                sock.connect(server_address)

                # Send the message
                sock.sendall(msg.encode())
                print(f"TCP message sent to {ip}:{port}")
            finally:
                sock.close()

        def wait(ip: str, port: int):
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_address = (ip, port)

            try:
                # Bind the socket to the server address
                sock.bind(server_address)

                # Listen for incoming connections
                sock.listen(1)
                print(f"TCP server listening on {ip}:{port}")

                while True:
                    # Accept incoming connection
                    connection, client_address = sock.accept()
                    print(f"Incoming connection from {client_address[0]}:{client_address[1]}")

                    # Receive and process the message
                    data = connection.recv(1024).decode()
                    print(f"Received message: {data}")

                    # Close the connection
                    connection.close()
                    print("Connection closed.")
                    
            finally:
                sock.close()
                print("Stopped")