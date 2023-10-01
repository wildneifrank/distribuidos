import socket
import threading

# Configurações do servidor
HOST = '127.0.0.1'  # Endereço IP do servidor
PORT = 8922         # Porta a ser usada pelo servidor

# Lista de clientes conectados
clients = []

# Função para enviar mensagens para todos os clientes
def broadcast(message, client_socket):
    for client in clients:
        if client != client_socket:
            try:
                client.send(message)
            except:
                # Se a mensagem não puder ser enviada, desconecta o cliente
                client.close()
                clients.remove(client)

# Função para lidar com a conexão de um cliente
def handle_client(client_socket):
    while True:
        try:
            message = client_socket.recv(1024)
            if not message:
                break
            broadcast(message, client_socket)
        except:
            # Se não for possível receber a mensagem, desconecta o cliente
            break

    # Remove o cliente da lista e fecha a conexão
    clients.remove(client_socket)
    client_socket.close()

# Configuração do servidor
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(5)  # Aceita até 5 conexões simultâneas

print(f"Servidor aguardando conexões em {HOST}:{PORT}...")

# Loop principal para aceitar conexões de clientes
while True:
    client_socket, addr = server.accept()
    print(f"Nova conexão de {addr}")
    
    # Adiciona o cliente à lista
    clients.append(client_socket)
    
    # Inicia uma thread para lidar com o cliente
    client_thread = threading.Thread(target=handle_client, args=(client_socket,))
    client_thread.start()
