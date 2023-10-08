import socket
import sensor_pb2  # Importe o módulo protobuf gerado para o Sensor
import sys

HOST = '127.0.0.1'  # Endereço IP do gateway
PORT = 8922        # Porta do gateway

def iniciar_gateway():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()

        print(f"Gateway ouvindo em {HOST}:{PORT}")

        conn, addr = s.accept()
        print(f"Conexão estabelecida com {addr}")

        while True:
            data = conn.recv(1024)  # Recebe os dados do sensor
            if not data:
                break

            # Desserializa os dados em uma mensagem protobuf
            temperatura_msg = sensor_pb2.Sensor()
            temperatura_msg.ParseFromString(data)

            # Acessa o campo de temperatura dentro da mensagem
            temperatura = temperatura_msg.temperature
            print(f"Temperatura recebida do sensor: {temperatura:.2f}ºC")

        print("Conexão encerrada")

if __name__ == "__main__":
    iniciar_gateway()
