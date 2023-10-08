import sensor_pb2
import sys
sys.path.append('../../')
import MulticastReceiver as mrcv
import socket
import random
import threading
import time

class ArCondicionadoController:
    def __init__(self):
        self.sensor = sensor_pb2.Sensor()
        self.sensor.state = False
        self.sensor.temperature = random.uniform(20, 30)

    def getTemp(self):
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

    def aumentar_temperatura(self):
        if self.sensor.state and self.sensor.temperature < 27:
            self.sensor.temperature += 1
            print(f"Temperatura aumentada para {self.sensor.temperature}ºC")
        elif self.sensor.temperature >= 27:
            print(f"Temperatura está no máximo de {self.sensor.temperature}ºC")
        else:
            print("O Sensor está desligado. Não é possível aumentar a temperatura.")

    def diminuir_temperatura(self):
        if self.sensor.state and self.sensor.temperature > 16:
            self.sensor.temperature -= 1
            print(f"Temperatura diminuída para {self.sensor.temperature}ºC")
        elif self.sensor.temperature <= 16:
            print(f"Temperatura está no mínimo de {self.sensor.temperature}ºC")
        else:
            print("O Sensor está desligado. Não é possível diminuir a temperatura.")

    def mostrar_estado(self):
        if self.sensor.state:
            print(f"\nTemperatura: {self.sensor.temperature} graus Celsius\n")
            print(f"coisa serializada: {self.sensor.SerializeToString()}")
        else:
            print("\nDesligado\n")

    def atualizar_temperatura(self):
        while True:
            self.getTemp()
            self.enviar_status_para_gateway()
            time.sleep(5)

    def enviar_status_para_gateway(self):
        status = sensor_pb2.Sensor()
        status.temperature = self.sensor.temperature

        msg = status.SerializeToString()
        s.sendall(msg)


controller = ArCondicionadoController()

HOST = "127.0.0.1"
PORT = 8922
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

# Inicie a thread para atualizar a temperatura e enviar para o gateway
thread_atualizacao = threading.Thread(target=controller.atualizar_temperatura)
thread_atualizacao.start()

while True:
    msg = s.recv(1024).decode('utf-8')
    if msg == 'exit':
        break
    if msg == "ligar":
        controller.ligar()
    elif msg == "desligar":
        controller.desligar()
    elif msg == "sair":
        break
    else:
        print("Não foi possível realizar a ação")
        continue
    s.sendall(controller.sensor.SerializeToString())

s.close()
exit()
