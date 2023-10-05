import socket
import netifaces
import subprocess
from protoBuff import MulticastMessage_pb2 as MulticastMessage

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

            # Desserializar a mensagem usando o mesmo módulo gerado
            message = MulticastMessage.MulticastMessage()
            message.ParseFromString(data)

            print(f"De: {message.sender}\nMensagem: {message.content}\n")

            return message.sender

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
    interface_ip = get_active_interface_ip("eno1")

    while(True):
        receiver = MulticastReceiver(multicast_group, multicast_port, interface_ip)
        sender_ip = receiver.receive_multicast_messages()

    # Para fechar os sockets quando terminar, você pode chamar os métodos 'close':
    receiver.close()

        
