import socket
import lampada_pb2

def handle_lampada_connection(client_socket, lampadapb):
    try:
        while True:
            control_msg = input('Digite um número ')

            if control_msg == "1":
                print("Pegar Status")
                lampadapb.control = '1'
                
            elif control_msg == "2":
                print("Ligando a lâmpada")
                lampadapb.control = '2'

            elif control_msg == "3":
                print("Desligando lâmpada")
                lampadapb.control = '3'

            # Responder com o status atual da lâmpada
            status_msg = lampadapb.SerializeToString()
            client_socket.sendall(status_msg)
            lstatus = lampada_pb2.Lampada()
            print("...")
            data = client_socket.recv(1024)
            print("Recebeu status do objeto")
            lstatus.ParseFromString(data)
            print(lstatus.status)

    except Exception as e:
        print(f"Erro na conexão com a lâmpada: {e}")
    finally:
        client_socket.close()

def main():
    # Defina o IP e a porta do gateway
    gateway_ip = "127.0.0.1"  # Substitua pelo IP do gateway
    gateway_port = 8080  # Substitua pela porta do gateway

    # Crie uma instância da lâmpada para controle
    lampadapb = lampada_pb2.LampadaControl()

    # Inicie o servidor do gateway
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((gateway_ip, gateway_port))
        server_socket.listen(5)
        print(f"Gateway escutando em {gateway_ip}:{gateway_port}")

        while True:
            client_socket, _ = server_socket.accept()
            print(f"Conexão estabelecida com um cliente")
            
            # Manipule a conexão da lâmpada em uma thread ou processo separado
            handle_lampada_connection(client_socket, lampadapb)

if __name__ == "__main__":
    main()
