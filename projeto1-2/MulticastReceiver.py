import socket

class MulticastReceiver:
    def __init__(self, multicast_group, multicast_port):
        self.multicast_group = multicast_group
        self.multicast_port = multicast_port

        # Crie um socket UDP multicast
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

        # Junte-se ao grupo multicast em todas as interfaces
        self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, socket.inet_aton(multicast_group) + socket.inet_aton('0.0.0.0'))

        # Associe o socket à porta do grupo multicast
        self.sock.bind(('0.0.0.0', multicast_port))

    def receive_messages(self):
        while True:
            # Receba mensagens do grupo multicast
            data, address = self.sock.recvfrom(1024)
            print(f"Recebido de {address}: {data.decode('utf-8')}")

if __name__ == "__main__":
    multicast_group = '224.0.0.1'
    multicast_port = 5000

    receiver = MulticastReceiver(multicast_group, multicast_port)
    receiver.receive_messages()
