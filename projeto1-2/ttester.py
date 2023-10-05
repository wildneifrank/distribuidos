import socket
import threading

# Função para lidar com soquete UDP
def udp_handler():
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_host = '127.0.0.1'
    udp_port = 12345
    udp_addr = (udp_host, udp_port)
    udp_socket.bind(udp_addr)
    
    while True:
        data, addr = udp_socket.recvfrom(1024)
        print(f'Recebido via UDP: {data.decode()} de {addr}')

# Função para lidar com soquete TCP
def tcp_handler():
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_host = '127.0.0.1'
    tcp_port = 54321
    tcp_addr = (tcp_host, tcp_port)
    tcp_socket.bind(tcp_addr)
    tcp_socket.listen(5)
    
    while True:
        client_socket, client_addr = tcp_socket.accept()
        print(f'Conexão TCP de {client_addr}')
        data = client_socket.recv(1024)
        print(f'Dados TCP recebidos: {data.decode()}')
        client_socket.close()

# Criar threads para os manipuladores UDP e TCP
udp_thread = threading.Thread(target=udp_handler)
tcp_thread = threading.Thread(target=tcp_handler)

# Iniciar as threads
udp_thread.start()
tcp_thread.start()

# Aguardar até que as threads terminem (você pode adicionar lógica de encerramento apropriada)
udp_thread.join()
tcp_thread.join()
