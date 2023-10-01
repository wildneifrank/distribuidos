import socket
from protoBuff import MulticastMessage

class MulticastSender:
    def __init__(self, multicast_group, multicast_port):
        self.multicast_group = multicast_group
        self.multicast_port = multicast_port

        interfaces = socket.getaddrinfo(socket.gethostname(), None)
        self.interface_ip = interfaces[3][4][0]

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

class MulticastReceiver:
    def __init__(self, multicast_group, multicast_port):
        self.multicast_group = multicast_group
        self.multicast_port = multicast_port

        interfaces = socket.getaddrinfo(socket.gethostname(), None)
        self.interface_ip = interfaces[3][4][0]

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

    def close(self):
        self.sock.close()

if __name__ == "__main__":
    multicast_group = '224.0.0.1'
    multicast_port = 5000

    sender = MulticastSender(multicast_group, multicast_port)
    sender.send_multicast_message('Enviador', 'Esta é uma mensagem de teste')

    receiver = MulticastReceiver(multicast_group, multicast_port)
    receiver.receive_multicast_messages()
