import socket
import struct
import time
from protoBuff import MulticastMessage_pb2 as mumes
from protoBuff import SensorMessage_pb2 as senmes
import threading
import MulticastReceiver as mrcv

def multicast_sender():
    # Configurações do multicast
    multicast_group = '224.0.0.1'
    multicast_port = 5000

    # Crie um socket UDP para multicast
    multicast_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

    # Configurar o socket para permitir que outros programas usem a mesma porta
    multicast_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Junte-se ao grupo multicast
    multicast_socket.bind(('', multicast_port))
    mreq = struct.pack('4sL', socket.inet_aton(multicast_group), socket.INADDR_ANY)
    multicast_socket.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

    print(f"Escutando mensagens do grupo {multicast_group}:{multicast_port}")
    
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    interface_ip = s.getsockname()[0]
    s.close()

    try:
        message = mumes.MulticastMessage()
        message.sender = interface_ip
        message.type = "Este dispositivo está online"

        # Serialize a mensagem protobuf em bytes
        message_bytes = message.SerializeToString()

            # Envie a mensagem serializada como um pacote UDP multicast
        multicast_socket.sendto(message_bytes, (multicast_group, multicast_port))

        
    except KeyboardInterrupt:
        pass
    finally:
        # Espere por um curto período antes de enviar novamente (pode ajustar isso conforme necessário)
            
        multicast_socket.close()

def multicast_receiver():
    server_ip = '192.168.1.245'
    server_port = 6000
    # Crie um socket TCP
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Vincular o socket ao endereço e porta do servidor
    sock.bind((server_ip, server_port))

    # Espere por conexões de clientes
    sock.listen(5)

    print(f"Servidor TCP escutando em {server_ip}:{server_port}")

    while True:
        conn, addr = sock.accept()
        print(f"Conexão estabelecida com {addr}")

        data = conn.recv(1024)  # Tamanho máximo da mensagem é 1024 bytes
        if data:
            # Parse da mensagem protobuf
            message = mumes.MulticastMessage()
            message.ParseFromString(data)

            sender = message.sender
            type = message.type
            print(f"Recebido de {sender}: {type}")
            #sensor
            if(type == '0'):
                print('sensor')
                sensor_thread = threading.Thread(target=sensor_handle(sender))
                sensor_thread.start()
                sensor_thread.join()

            #atuador
            elif(type == '1'):
                print('atuador')
            #ar-condicionado
            elif(type=='2'):
                print('ar-condicionado')


        conn.close()

############################# tratamentos de objetos #####################################

#Sensor
def sensor_handle(sender):
    server_ip = '192.168.1.245'
    server_port = 6001
    # Crie um socket TCP
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Vincular o socket ao endereço e porta do servidor
    sock.bind((server_ip, server_port))

    # Espere por conexões de clientes
    sock.listen(1)

    print(f"Servidor TCP escutando em {server_ip}:{server_port}")
    objetos[sender] = None

    while True:
        conn, addr = sock.accept()
        data = senmes.SensorMessage()
        data.ParseFromString(conn.recv(1024))
        objetos[sender] = data.valor
        print(f"Conexão estabelecida com {objetos}")
        
    return 0

#Atuador
def atuador_handle(sender):
    server_ip = '192.168.1.245'
    server_port = 6001
    # Crie um socket TCP
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Vincular o socket ao endereço e porta do servidor
    sock.bind((server_ip, server_port))

    # Espere por conexões de clientes
    sock.listen(1)

    print(f"Servidor TCP escutando em {server_ip}:{server_port}")
    objetos[sender] = None

    while True:
        conn, addr = sock.accept()
        data = senmes.SensorMessage()
        data.ParseFromString(conn.recv(1024))
        objetos[sender] = data.valor
        print(f"Conexão estabelecida com {objetos}")
        
    return 0

#Ar-condicionado
def ac_handle(sender):
    server_ip = '192.168.1.245'
    server_port = 6001
    # Crie um socket TCP
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Vincular o socket ao endereço e porta do servidor
    sock.bind((server_ip, server_port))

    # Espere por conexões de clientes
    sock.listen(1)

    print(f"Servidor TCP escutando em {server_ip}:{server_port}")
    objetos[sender] = None

    while True:
        conn, addr = sock.accept()
        data = senmes.SensorMessage()
        data.ParseFromString(conn.recv(1024))
        objetos[sender] = data.valor
        print(f"Conexão estabelecida com {objetos}")
        
    return 0



if __name__ == "__main__":
    # Crie uma thread para executar a função multicast_sender
    multicast_sender()

    objetos = {}

    multicast_thread_receiver = threading.Thread(target=multicast_receiver)

    # Inicie a thread
    multicast_thread_receiver.start()

    # Aguarde a thread terminar (você pode remover esta linha se desejar que o programa principal termine imediatamente)
    multicast_thread_receiver.join()

    
