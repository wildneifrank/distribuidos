from protoBuff import sensor_pb2
from protoBuff import MulticastMessage_pb2 as mumes
import MulticastReceiver as mrcv
import socket
import random
import threading
import time
import sys

class SensorController:
    def __init__(self):
        self.state = False
        self.temperature = random.uniform(20, 30)
        self.running = True  # Variável para controlar a execução da thread

    def get_Temp(self):
        value = self.sensor.temperature
        if random.random() > 0.5:
            self.temperature = value - random.random()
        else:
            self.temperature = value + random.random()

    def ligar(self):
        if self.state:
            print(f"O Sensor já está ligado.")
        else:
            self.state = True
            print(f"O Sensor agora está ligado.")

    def desligar(self):
        if self.state:
            self.state = False
            print("O Sensor agora está em standby.")
        else:
            print(f"O Sensor já está em standby.")

    def mostrar_estado(self):
        if self.state:
            print(f"\nTemperatura: {self.temperature:.2f} graus Celsius\n")
            print(f"coisa serializada: {self.SerializeToString()}")
        else:
            print("\nDesligado\n")

    def atualizar_temperatura(self):
        while self.running:
            if self.state:
                self.get_Temp()
                self.send_status()
            time.sleep(5)

    def send_status(self, sender_ip, sender_port):
        status = sensor_pb2.Sensor()
        while True:
            udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            status.temperature = self.temperature
            status.state = self.state

            msg = status.SerializeToString()
            udp_socket.sendto(msg, (sender_ip, sender_port))
            time.sleep(5)
            print('enviou')
            udp_socket.close()

def main(sender_ip, sender_port):
    senTemp_ip = "127.0.0.1"
    senTemp_port = 8004
    gateway_ip = sender_ip
    gateway_port = sender_port
    try: 
        # with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        #         s.connect((gateway_ip, gateway_port))
        #         mensagem_pb = mumes.MulticastMessage()
        #         mensagem_pb.ip = senTemp_ip  # Substitua pelo nome do remetente
        #         mensagem_pb.port = senTemp_port
        #         mensagem_pb.type = '1'  # Substitua pelo conteúdo da mensagem

        #         # Serializar a mensagem protobuf em bytes
        #         msg_serializada = mensagem_pb.SerializeToString()
        #         s.sendall(msg_serializada)
        #         print('enviou')
        #         s.close()

        

        # Inicialize o controlador
        controller = SensorController()

        # Inicie a thread para atualizar a temperatura e enviar para o gateway
        thread_atualizacao = threading.Thread(target=controller.atualizar_temperatura)
        thread_atualizacao.daemon = True  # Torna a thread um daemon para que ela termine com o programa principal
        thread_atualizacao.start()
        # Inicie a thread para atualizar a temperatura e enviar para o gateway
        udp_socket = threading.Thread(target=controller.send_status, args=(sender_ip, sender_port,))
        udp_socket.daemon = True  # Torna a thread um daemon para que ela termine com o programa principal
        udp_socket.start()
        while True:
            pass

    except KeyboardInterrupt:
        controller.running = False  # Sinalize para a thread de atualização que ela deve parar quando o usuário pressionar Ctrl+C
        udp_socket.close()


if __name__ == "__main__":
    gate = mrcv.multicast_receiver()
    main(gate[0],gate[1])
