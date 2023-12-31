import socket
import subprocess
from protoBuff import MulticastMessage_pb2 as MulticastMessage
import sys  

class MulticastReceiver:
    def __init__(self, multicast_group, multicast_port, interface_ip):
        self.multicast_group = multicast_group
        self.multicast_port = multicast_port
        self.interface_ip = interface_ip

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.interface_ip, self.multicast_port))

        mreq = socket.inet_aton(self.multicast_group) + socket.inet_aton(self.interface_ip)
        self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

    def receive_multicast_messages(self):
        while True:
            data, _ = self.sock.recvfrom(1024)

            message = MulticastMessage.MulticastMessage()
            message.ParseFromString(data)
            print(message)

            print(f"De: {message.ip}\nMensagem: {message.type}\n")

            return message.ip, message.port, message.type, message.udpport

    def close(self):
        self.sock.close()

def get_active_interface_ip(interface_name):
    try:
        output = subprocess.check_output(["ifconfig", interface_name]).decode("utf-8")
        lines = output.split("\n")
        for line in lines:
            if "inet " in line:
                parts = line.split()
                return parts[1]  
    except Exception as e:
        print(f"Erro ao obter a interface IP: {e}")
        return None

def multicast_receiver(multicast_group, multicast_port):
    receiver = MulticastReceiver(multicast_group, multicast_port, interface_ip)
    ip, port, type, udpport = receiver.receive_multicast_messages()
    receiver.close()
    return (ip, port, type, udpport)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python3 MulticastReceiver.py <multicast_port>")
        sys.exit(1)

    multicast_port = int(sys.argv[1])
    multicast_group = '224.0.0.1'  
    interface_ip = get_active_interface_ip("eth0") 

    while True:
        receiver = multicast_receiver(multicast_group, multicast_port)
        sender_ip, sender_port, message_type, sender_udpport = receiver
        