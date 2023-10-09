from protoBuff import ArCondicionado_pb2
import MulticastReceiver as mrcv
import socket
from protoBuff import MulticastMessage_pb2 as mumes

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
        
        return self.ar_condicionado.state, self.ar_condicionado.temp

def main(sender_ip, sender_port):
    
    controller = ArCondicionadoController()

    arcon_ip = "127.0.0.1"
    arcon_port = 8003
    gateway_ip = sender_ip
    gateway_port = sender_port 
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((gateway_ip, gateway_port))
            mensagem_pb = mumes.MulticastMessage()
            mensagem_pb.ip = arcon_ip  
            mensagem_pb.port = arcon_port
            mensagem_pb.type = '3' 

            # Serializar a mensagem protobuf em bytes
            msg_serializada = mensagem_pb.SerializeToString()
            s.sendall(msg_serializada)
            print('enviou')
            s.close()
            while True:
                # Configurações do servidor
                host = arcon_ip  
                porta = arcon_port   

                # Crie um socket TCP
                servidor_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                servidor_socket.bind((host, porta))

                # Até 5 clientes em fila
                servidor_socket.listen(5)

                print(f"Servidor TCP está ouvindo em {host}:{porta}")

                while True:
                    cliente_socket, endereco_cliente = servidor_socket.accept()

                    print(f"Conexão estabelecida com {endereco_cliente}")

                    mensagem = "Conexão estabelecida com sucesso!"
                    print(mensagem)

                    data = cliente_socket.recv(1024)
                    print("Recebeu comando do servidor")
                    if not data:
                        break  

                    control_msg = ArCondicionado_pb2.Controle()
                    control_msg.ParseFromString(data)

                    if control_msg.operacao == "1":
                        controller.ligar()
                    elif control_msg.operacao == "2":
                        controller.desligar()
                    elif control_msg.operacao == "3":
                        controller.mostrar_estado()
                    elif control_msg.operacao == "4":
                        controller.aumentar_temperatura()
                    elif control_msg.operacao == "5":
                        controller.diminuir_temperatura()
                    else:
                        print("Não foi possível realizar a ação")
                        continue

                    acstatus = ArCondicionado_pb2.attributes()
                    acstatus.state, acstatus.temp = controller.mostrar_estado()
                    status_msg = acstatus.SerializeToString()
                    cliente_socket.send(status_msg)
                    print('state: ',acstatus.state,'temp: ', acstatus.temp)
                    print("Status enviado")

                    cliente_socket.close()

if __name__ == '__main__':
    gate = mrcv.multicast_receiver()
    main(gate[0],gate[1])