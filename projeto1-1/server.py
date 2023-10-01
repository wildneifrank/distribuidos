import socket
import threading
import time

# Configurações do servidor
HOST = '127.0.0.1'  # Endereço IP do servidor
PORT = 8922         # Porta a ser usada pelo servidor

# Lista de clientes conectados
clients = []
names = []


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
    # Leitura do nome do usuário após a conexão
    user = client_socket.recv(1024).decode('utf-8')
    
    # Verificação se o nome de usuário já está em uso

    condition = True
    if user in names:        
        client_socket.send("code:0".encode('utf-8'))
        client_socket.close()
        condition = False
    else:
        names.append(user)
        bemvin = 'Bem vindo ' + user
        entrou = 'O usuario '+user+' entrou!!!'
        broadcast(entrou.encode('utf-8'), client_socket)
        client_socket.send(bemvin.encode('utf-8'))
        
    while condition:
        try:
            message = client_socket.recv(1024)
            print(message.decode('utf-8'))
            if not message:
                break
            if(message.decode('utf-8') == 'oi'):
                print('deu certo')
            broadcast(message, client_socket)
        except:
            # Se não for possível receber a mensagem, desconecta o cliente
            break

    # Remove o cliente da lista e fecha a conexão
    names.remove(user)
    clients.remove(client_socket)
    client_socket.close()

# Configuração do servidor
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(4)  # Aceita até 4 conexões simultâneas

print(f"Servidor aguardando conexões em {HOST}:{PORT}...")

# Loop principal para aceitar conexões de clientes
while True:
    client_socket, addr = server.accept()
    
    # Adiciona o cliente à lista
    clients.append(client_socket)
    
    # Inicia uma thread para lidar com o cliente
    client_thread = threading.Thread(target=handle_client, args=(client_socket,))
    client_thread.start()
    print(f"Nova conexão de {addr}")
