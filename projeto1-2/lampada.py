from protoBuff import lampada_pb2
from protoBuff import MulticastMessage_pb2 as mumes
import socket
import MulticastReceiver as mrcv
import MulticastSender as msnd

class Lampada:
    def __init__(self):
        self.status = False

    def ligar(self):
        self.status = True
        print("Lâmpada ligada.")

    def desligar(self):
        self.status = False
        print("Lâmpada desligada.")

    def get_status(self):
        return self.status

def main(sender_ip, sender_port):
    lampada_ip = '127.0.0.1' 
    lampada_port = 5000

    lampada = Lampada()

    gateway_ip = sender_ip
    gateway_port = sender_port 

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((gateway_ip, gateway_port))
            mensagem_pb = mumes.MulticastMessage()
            mensagem_pb.ip = lampada_ip 
            mensagem_pb.port = lampada_port
            mensagem_pb.type = '2'  

            msg_serializada = mensagem_pb.SerializeToString()
            s.sendall(msg_serializada)
            print('enviou')
            s.close()

            while True:
                host = lampada_ip  
                porta = lampada_port  

                servidor_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

                servidor_socket.bind((host, porta))

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

                    control_msg = lampada_pb2.LampadaControl()
                    control_msg.ParseFromString(data)

                    if control_msg.control == "1":
                        print("Pegar Status")
                        lampada.get_status()
                    elif control_msg.control == "2":
                        print('ligando')
                        lampada.ligar()
                    elif control_msg.control == "3":
                        print('desligando')
                        lampada.desligar()

                    lstatus = lampada_pb2.Lampada()
                    lstatus.status = lampada.get_status()
                    status_msg = lstatus.SerializeToString()
                    cliente_socket.send(status_msg)
                    print(lstatus.status)
                    print("Status enviado")

                    cliente_socket.close()

                

    except Exception as e:
        print(f"Erro ao conectar ao gateway: {e}")

if __name__ == "__main__":
    gate = mrcv.multicast_receiver()
    main(gate[0], gate[1])
