import socket

class ExternalConnections:
    # Class USP: wiki.python.org/moin/UdpCommunication
    class UDP:
        def send(ip: str, port: int, msg: str):
            print("Trying to send packet to destination")
            byte_string = bytes(msg, 'utf-8')
            sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
            sock.sendto(byte_string, (ip, port))

        def wait(ip: str, port: int):
            sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
            sock.bind((ip, port))
            print("Beginning to wait for message:")
            while True:
                data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
                print("received message: %s" % data)
                break