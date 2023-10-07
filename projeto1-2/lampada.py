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
    
    lampada_ip = "127.0.0.1"  
    lampada_tipo = "lampada"

    
    lampada = Lampada(lampada_ip, lampada_tipo)

    
    gateway_ip = "127.0.0.1"  
    gateway_port = 8080  

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((gateway_ip, gateway_port))

            while True:
                ## Aguardar uma mensagem do gateway
                data = s.recv(1024)

                if not data:
                    break  

                ## Interpretar a mensagem do gateway
                control_msg = lampada_pb2.LampadaControl()
                control_msg.ParseFromString(data)

                
                if control_msg.control:
                    lampada.ligar()
                else:
                    lampada.desligar()

                
                status_msg = lampada.get_status().SerializeToString()
                s.sendall(status_msg)

    except Exception as e:
        print(f"Erro ao conectar ao gateway: {e}")

if __name__ == "__main__":
    main()
