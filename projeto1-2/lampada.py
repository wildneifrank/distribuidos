from protoBuff import lampada_pb2
from protoBuff import MulticastMessage_pb2 as mumes
import socket
import MulticastReceiver as mrcv

class Lampada:
    def __init__(self, IP, tipo):
        self.status = False
        self.IP = IP
        self.tipo = tipo

    def ligar(self):
        self.status = True
        print("Lâmpada ligada.")

    def desligar(self):
        self.status = False
        print("Lâmpada desligada.")

    def get_status(self):
        return self.status

def main(sender_ip):
    
    lampada_ip = '127.0.0.1' 
    lampada_tipo = "lampada"

    
    lampada = Lampada(lampada_ip, lampada_tipo)

    
    gateway_ip = sender_ip
    gateway_port = 8002  

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((gateway_ip, gateway_port))
            mensagem_pb = mumes.MulticastMessage()
            mensagem_pb.sender = lampada_ip  # Substitua pelo nome do remetente
            mensagem_pb.type = '2'  # Substitua pelo conteúdo da mensagem

            # Serializar a mensagem protobuf em bytes
            msg_serializada = mensagem_pb.SerializeToString()
            s.sendall(msg_serializada)

            while True:
                ## Aguardar uma mensagem do gateway
                data = s.recv(1024)
                print("Recebeu comando do servidor")
                if not data:
                    break  

                ## Interpretar a mensagem do gateway
                control_msg = lampada_pb2.LampadaControl()
                control_msg.ParseFromString(data)

                
                if control_msg == "1":
                    print("Pegar Status")
                    lampada.get_status()
                elif control_msg == "2":
                    lampada.ligar()
                elif control_msg == "3":
                    lampada.desligar()

                lstatus = lampada_pb2.Lampada()
                lstatus.status = lampada.get_status()
                print(type(lampada.get_status()))
                status_msg = lstatus.SerializeToString()
                s.sendall(status_msg)
                print("Status enviado")

    except Exception as e:
        print(f"Erro ao conectar ao gateway: {e}")


if __name__ == "__main__":
    
    multicast_group = '224.0.0.1'
    multicast_port = 5000
    interface_ip = mrcv.get_active_interface_ip("wifi0")


    receiver = mrcv.MulticastReceiver(multicast_group, multicast_port, interface_ip)
    sender_ip = receiver.receive_multicast_messages()

    # Para fechar os sockets quando terminar, você pode chamar os métodos 'close':
    receiver.close()
    main(sender_ip)
