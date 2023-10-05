import socket
import time
import random
from Sensor_pb2 import TemperatureMessage

# Configurações do sensor
sensor_ip = '127.0.0.1'  # Endereço IP do sensor
sensor_port = 12345      # Porta do sensor
gateway_ip = '127.0.0.1' # Endereço IP do Gateway
gateway_port = 5000      # Porta do Gateway
multicast_group = '224.0.0.1'
multicast_port = 5002

# Crie um socket UDP
sensor_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Função para gerar valores de temperatura simulados
inicial_temperature = random.uniform(25,30)

def generate_temperature(temperature):
    if(random.random() > 0.5):
        return temperature - random.random()
    else:
        return temperature + random.random()

# Mensagem de identificação
identificacao = f"Tipo: Sensor de Temperatura, IP: {sensor_ip}, Porta: {sensor_port}"

# Envie a mensagem de identificação por multicast
multicast_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
multicast_socket.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)
multicast_socket.sendto(identificacao.encode(), (multicast_group, multicast_port))
multicast_socket.close()

while True:
    inicial_temperature = generate_temperature(inicial_temperature)

    # Crie uma mensagem TemperatureMessage
    mensagem = TemperatureMessage()
    mensagem.temperature = inicial_temperature

    # Serialize a mensagem em bytes
    mensagem_bytes = mensagem.SerializeToString()

    # Envie a mensagem serializada para o Gateway
    sensor_socket.sendto(mensagem_bytes, (gateway_ip, gateway_port))

    # print(f"Dados de temperatura enviados para o Gateway: {mensagem}")

    # Aguarde 3 segundos antes de enviar o próximo valor
    time.sleep(3)
