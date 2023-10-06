import socket
import lampada_pb2

def handle_lampada_connection(client_socket, lampada):
    try:
        while True:
            data = client_socket.recv(1024)
            if not data:
                break

            # Interpretar a mensagem recebida do cliente
            control_msg = lampada_pb2.LampadaControl()
            control_msg.ParseFromString(data)

            # Lidar com o comando do cliente
            if control_msg.control:
                lampada.ligar()
            else:
                lampada.desligar()

            # Responder com o status atual da lâmpada
            status_msg = lampada.get_status().SerializeToString()
            client_socket.sendall(status_msg)
    except Exception as e:
        print(f"Erro na conexão com a lâmpada: {e}")
    finally:
        client_socket.close()

def main():
    # Defina o IP e a porta do gateway
    gateway_ip = "127.0.0.1"  # Substitua pelo IP do gateway
    gateway_port = 8080  # Substitua pela porta do gateway

    # Crie uma instância da lâmpada para controle
    lampada = lampada_pb2.Lampada()

    # Inicie o servidor do gateway
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((gateway_ip, gateway_port))
        server_socket.listen(5)
        print(f"Gateway escutando em {gateway_ip}:{gateway_port}")

        while True:
            client_socket, _ = server_socket.accept()
            print(f"Conexão estabelecida com um cliente")
            
            # Manipule a conexão da lâmpada em uma thread ou processo separado
            handle_lampada_connection(client_socket, lampada)

if __name__ == "__main__":
    main()
