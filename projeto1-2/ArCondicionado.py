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

    arcon_ip = "127.0.0.1"
    arcon_port = 8003
    gateway_ip = sender_ip
    gateway_port = sender_port 
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((gateway_ip, gateway_port))
            mensagem_pb = mumes.MulticastMessage()
            mensagem_pb.ip = arcon_ip  # Substitua pelo nome do remetente
            mensagem_pb.port = arcon_port
            mensagem_pb.type = '3'  # Substitua pelo conteúdo da mensagem

            # Serializar a mensagem protobuf em bytes
            msg_serializada = mensagem_pb.SerializeToString()
            s.sendall(msg_serializada)
            print('enviou')
            s.close()
            while True:
                # Configurações do servidor
                host = arcon_ip  # Endereço IP do servidor (use 'localhost' para conexões locais)
                porta = arcon_port   # Porta em que o servidor irá ouvir

                # Crie um socket TCP
                servidor_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

                # Vincule o socket ao endereço e porta do servidor
                servidor_socket.bind((host, porta))

                # Espere por conexões de clientes (até 5 clientes em fila)
                servidor_socket.listen(5)

                print(f"Servidor TCP está ouvindo em {host}:{porta}")

                while True:
                    # Aceite uma conexão de cliente
                    cliente_socket, endereco_cliente = servidor_socket.accept()

                    print(f"Conexão estabelecida com {endereco_cliente}")

                    # Envie uma mensagem de confirmação para o cliente
                    mensagem = "Conexão estabelecida com sucesso!"
                    print(mensagem)

                    ## Aguardar uma mensagem do gateway
                    data = cliente_socket.recv(1024)
                    print("Recebeu comando do servidor")
                    if not data:
                        break  

                    ## Interpretar a mensagem do gateway
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