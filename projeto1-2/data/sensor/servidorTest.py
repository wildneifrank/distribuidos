import socket
import sensor_pb2  # Importe o módulo protobuf gerado para o Sensor

GATEWAY_HOST = '127.0.0.1'  # Endereço IP do gateway
GATEWAY_PORT = 8922         # Porta do gateway

def iniciar_gateway():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udp_socket:
        udp_socket.bind((GATEWAY_HOST, GATEWAY_PORT))

        sensorInfo, addr = udp_socket.recvfrom(1024)
        sensorInfo_msg = sensor_pb2.Sensor()
        sensorInfo_msg.ParseFromString(sensorInfo)

        print(f"Conectado ao {sensorInfo_msg.type} no Host {sensorInfo_msg.ip}:{sensorInfo_msg.port}")
        print(f"Gateway ouvindo em {GATEWAY_HOST}:{GATEWAY_PORT}")

        while True:
            data, addr = udp_socket.recvfrom(1024)  # Recebe os dados do sensor
            if not data:
                break

            # Desserializa os dados em uma mensagem protobuf
            temperatura_msg = sensor_pb2.Sensor()
            temperatura_msg.ParseFromString(data)

            # Acessa o campo de temperatura dentro da mensagem
            temperatura = temperatura_msg.temperature
            print(f"Temperatura recebida do sensor: {temperatura:.2f}ºC")

if __name__ == "__main__":
    iniciar_gateway()
