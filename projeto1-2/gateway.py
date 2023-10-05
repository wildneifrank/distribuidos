import socket
import netifaces
import subprocess
from protoBuff import MulticastMessage_pb2 as MulticastMessage

class MulticastSender:
    def __init__(self, multicast_group, multicast_port, interface_ip):
        self.multicast_group = multicast_group
        self.multicast_port = multicast_port
        self.interface_ip = interface_ip

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, socket.inet_aton(multicast_group) + socket.inet_aton(self.interface_ip))

    def send_multicast_message(self, sender, content):
        message = MulticastMessage.MulticastMessage()
        message.sender = sender
        message.content = content

        message_bytes = message.SerializeToString()

        self.sock.sendto(message_bytes, (self.multicast_group, self.multicast_port))

    def close(self):
        self.sock.close()

def get_active_interface_ip(interface_name):
    try:
        output = subprocess.check_output(["ifconfig", interface_name]).decode("utf-8")
        lines = output.split("\n")
        for line in lines:
            if "inet " in line:
                parts = line.split()
                return parts[1]  # O endereço IPv4 está na segunda parte
    except Exception as e:
        print(f"Erro ao obter a interface IP: {e}")
        return None

if __name__ == "__main__":
    multicast_group = '224.0.0.1'
    multicast_port = 5000
    interface_ip = get_active_interface_ip("wifi0")

    sender = MulticastSender(multicast_group, multicast_port, interface_ip)
    sender.send_multicast_message(interface_ip, 'Esta é uma mensagem de teste do Matheus')
    sender.close()