import sensor_pb2
import socket
import random
import threading
import time
import sys

class SensorController:
    def __init__(self):
        self.sensor = sensor_pb2.Sensor()
        self.sensor.type = "Sensor"
        self.sensor.state = False
        self.sensor.temperature = random.uniform(20, 30)
        self.sensor.ip = "127.0.0.2"
        self.sensor.port = 1234
        self.running = True  # Variável para controlar a execução da thread
        sensorInfo = self.sensor.SerializeToString()
        udp_socket.sendto(sensorInfo, (GATEWAY_HOST, GATEWAY_PORT))

    def get_Temp(self):
        value = self.sensor.temperature
        if random.random() > 0.5:
            self.sensor.temperature = value - random.random()
        else:
            self.sensor.temperature = value + random.random()

    def ligar(self):
        if self.sensor.state:
            print(f"O Sensor já está ligado.")
        else:
            self.sensor.state = True
            print(f"O Sensor agora está ligado.")

    def desligar(self):
        if self.sensor.state:
            self.sensor.state = False
            print("O Sensor agora está em standby.")
        else:
            print(f"O Sensor já está em standby.")

    def mostrar_estado(self):
        if self.sensor.state:
            print(f"\nTemperatura: {self.sensor.temperature:.2f} graus Celsius\n")
            print(f"coisa serializada: {self.sensor.SerializeToString()}")
        else:
            print("\nDesligado\n")

    def atualizar_temperatura(self):
        while self.running:
            if self.sensor.state:
                self.get_Temp()
                self.send_status()
            time.sleep(5)

    def send_status(self):
        status = sensor_pb2.Sensor()
        status.temperature = self.sensor.temperature

        msg = status.SerializeToString()
        udp_socket.sendto(msg, (GATEWAY_HOST, GATEWAY_PORT))

GATEWAY_HOST = "127.0.0.1"  # Endereço IP do gateway
GATEWAY_PORT = 8922         # Porta do gateway

udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Inicialize o controlador
controller = SensorController()

# Inicie a thread para atualizar a temperatura e enviar para o gateway
thread_atualizacao = threading.Thread(target=controller.atualizar_temperatura)
thread_atualizacao.daemon = True  # Torna a thread um daemon para que ela termine com o programa principal
thread_atualizacao.start()

try:
    while True:
        msg = input("Digite uma ação (ligar/desligar/sair): ")
        if msg == 'sair':
            controller.running = False  # Sinalize para a thread de atualização que ela deve parar
            udp_socket.close()
            sys.exit(0)
        elif msg == "ligar":
            controller.ligar()
        elif msg == "desligar":
            controller.desligar()
        else:
            print("Ação inválida. Digite 'ligar', 'desligar' ou 'sair'.")

except KeyboardInterrupt:
    controller.running = False  # Sinalize para a thread de atualização que ela deve parar quando o usuário pressionar Ctrl+C
    udp_socket.close()
