import socket
from Sensor_pb2 import TemperatureMessage

# Configurações do Gateway
gateway_ip = '127.0.0.1'  # Endereço IP do Gateway
gateway_port = 5000       # Porta do Gateway
multicast_group = '224.0.0.1'
multicast_port = 5001

# Crie um socket UDP para identificação por multicast
multicast_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Adicione o Gateway ao grupo multicast
multicast_socket.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, socket.inet_aton(multicast_group) + socket.inet_aton(gateway_ip))

# Vincule o socket ao endereço e porta do Gateway
multicast_socket.bind((gateway_ip, multicast_port))

print(f"Gateway escutando em {gateway_ip}:{gateway_port}")

# Crie um socket UDP para receber dados do sensor
sensor_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sensor_socket.bind((gateway_ip, gateway_port))

print(f"Gateway esperando por mensagens do sensor")

while True:
    data, addr = multicast_socket.recvfrom(1024)  # Tamanho máximo da mensagem é 1024 bytes

    # Verifique se a mensagem é de identificação por multicast
    if addr[0] == gateway_ip and addr[1] == multicast_port:
        print(f"Recebida mensagem de identificação: {data.decode()}")

    else:
        # Desserialize a mensagem recebida do sensor de temperatura
        mensagem = TemperatureMessage()
        mensagem.ParseFromString(data)

        temperatura = mensagem.temperature

        print(f"Recebido dado de temperatura: {temperatura} °C do sensor")
