import lampada_pb2
import socket

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
        return lampada_pb2.LampadaStatus(ligada=self.status)

def main():
    # Defina o IP e o tipo da lâmpada
    lampada_ip = "127.0.0.1"  # Substitua pelo IP da lâmpada
    lampada_tipo = "lampada"

    # Crie uma instância da lâmpada
    lampada = Lampada(lampada_ip, lampada_tipo)

    # Estabeleça uma conexão TCP com o gateway
    gateway_ip = "127.0.0.1"  # Substitua pelo IP do gateway
    gateway_port = 8080  # Substitua pela porta do gateway

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((gateway_ip, gateway_port))

            while True:
                # Aguarde uma mensagem do gateway
                data = s.recv(1024)

                if not data:
                    break  # Encerre o loop se a conexão for encerrada pelo gateway

                # Interpretar a mensagem do gateway
                control_msg = lampada_pb2.LampadaControl()
                control_msg.ParseFromString(data)

                # Mudar o status da lâmpada de acordo com a mensagem do gateway
                if control_msg.control:
                    lampada.ligar()
                else:
                    lampada.desligar()

                # Responder com o status atual
                status_msg = lampada.get_status().SerializeToString()
                s.sendall(status_msg)

    except Exception as e:
        print(f"Erro ao conectar ao gateway: {e}")

if __name__ == "__main__":
    main()
