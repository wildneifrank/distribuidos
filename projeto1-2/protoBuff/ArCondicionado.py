import ArCondicionado_pb2
import MulticastReceiver as mrcv
import socket

class ArCondicionadoController:
    def __init__(self):
        self.ar_condicionado = ArCondicionado_pb2.attributes()
        self.ar_condicionado.state = False;
        self.ar_condicionado.temp = 20;

    def ligar(self):
        if self.ar_condicionado.state:
             print(f"Ar Condicionado já está ligado.")
        else:
            self.ar_condicionado.state = True
            print(f"Ar Condicionado agora está ligado.")

    def desligar(self):
        if self.ar_condicionado.state:
             self.ar_condicionado.state = False
             print("Ar Condicionado agora está em standby.")
        else:
            print(f"Ar Condicionado já está em standby.")

    def aumentar_temperatura(self):
        if self.ar_condicionado.state and self.ar_condicionado.temp < 27:
            self.ar_condicionado.temp += 1
            print(f"Temperatura aumentada para {self.ar_condicionado.temp}ºC")
        elif self.ar_condicionado.temp >= 27:
            print(f"Temperatura está no máximo de {self.ar_condicionado.temp}ºC")
        else:
            print("Ar Condicionado está desligado. Não é possível aumentar a temperatura.")

    def diminuir_temperatura(self):
        if self.ar_condicionado.state and self.ar_condicionado.temp > 16:
            self.ar_condicionado.temp -= 1
            print(f"Temperatura diminuida para {self.ar_condicionado.temp}ºC")
        elif self.ar_condicionado.temp <= 16:
            print(f"Temperatura está no mínimo de {self.ar_condicionado.temp}ºC")
        else:
            print("O Ar Condicionado está desligado. Não é possível diminuir a temperatura.")

    def mostrar_estado(self):
        if self.ar_condicionado.state:
            print(f"\nTemperatura: {self.ar_condicionado.temp} graus Celsius\n")
            print(f"coisa serializada: {self.ar_condicionado.SerializeToString()}")
        else:
            print("\nDesligado\n")    

controller = ArCondicionadoController()

""" multicast_group = '224.0.0.1'
multicast_port = 5000
interface_ip = mrcv.get_active_interface_ip("Ethernet Ethernet") #ip do objeto
interface_ip = '127.0.0.1'

print(f'{multicast_group} - {multicast_port} - {interface_ip}')
receiver = mrcv.MulticastReceiver(multicast_group, multicast_port, interface_ip)
sender_ip = receiver.receive_multicast_messages()

    # Para fechar os sockets quando terminar, você pode chamar os métodos 'close':
receiver.close() """

"""Lança o MultiCast pra dizer q ta ligado aqui <<"""

HOST = "127.0.0.1"
PORT = 8002
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
while True:
    msg = s.recv(1024).decode('utf-8')
    if msg == 'exit':
        break
    if msg == "ligar":
        controller.ligar()
    elif msg == "desligar":
        controller.desligar()
    elif msg == "+":
        controller.aumentar_temperatura()
    elif msg == "-":
        controller.diminuir_temperatura()
    elif msg == "sair":
        break
    else:
        print("Não foi possível realizar a ação")
        continue
    s.sendall(controller.ar_condicionado.SerializeToString())
s.close()
exit()