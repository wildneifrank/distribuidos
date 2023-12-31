import socket
import threading
# Configurações do servidor
HOST = '127.0.0.1'  
PORT = 8922         

clients = []
names = []


def broadcast(message, client_socket):
    for client in clients:
        if client != client_socket:
            try:
                client.send(message)
            except:
                client.close()
                clients.remove(client)

def handle_client(client_socket):
    if(len(clients)<=2):
        user = client_socket.recv(1024).decode('utf-8')
    else:
        client_socket.send("Sala cheia.".encode('utf-8'))
        clients.remove(client_socket)
        client_socket.close()

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
            if(message.decode('utf-8').strip() == '/usuarios'):
                client_socket.send('Usuarios conectados:'.encode('utf-8'))
                for name in names:
                    print(name,'\n')
                    client_socket.send(name.encode('utf-8'))
            elif(message.decode('utf-8').strip() == '/nick'):
                #mudar o nick
                client_socket.send('Digite o novo nick: '.encode('utf-8'))
                new_user = client_socket.recv(1024).decode('utf-8').strip()
                if not(new_user in names):
                    names.remove(user)
                    names.append(new_user)
                    print('nomes',names)
                    user = new_user
                else:
                    client_socket.send('Falha ao trocar de nick. Nick já escolhido.'.encode('utf-8'))

            elif(message.decode('utf-8').strip() == '/sair'):
                saida = user + ' saiu da sala.'
                broadcast(saida, client_socket)
                client_socket.send('Até a próxima'.encode('utf-8'))
                names.remove(user)
                clients.remove(client_socket)
                client_socket.close()
            else:
                message = user+': '+message.decode('utf-8').strip()
                broadcast(message.encode('utf-8'), client_socket)
        except:
            break

    names.remove(user)
    clients.remove(client_socket)
    client_socket.close()

# Configuração do servidor
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(4)  

print(f"Servidor aguardando conexões em {HOST}:{PORT}...")

while True:
    client_socket, addr = server.accept()

    clients.append(client_socket)
    client_thread = threading.Thread(target=handle_client, args=(client_socket,))
    client_thread.start()
    print(f"Nova conexão de {addr}")
