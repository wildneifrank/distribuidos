import socket
import struct
import time
from protoBuff import MulticastMessage_pb2 as mumes
from protoBuff import SensorMessage_pb2 as senmes
from protoBuff import ArCondicionado_pb2 as armes
from protoBuff import lampada_pb2 as lames
import MulticastReceiver as mrcv
import MulticastSender as msnd
import threading
import User as usr
global acao
acao = ''
senTemp = usr.SensorTemp()
arcon = usr.ArCon()
lamp = usr.Lampada()

acao_lock = threading.Lock()



def obj_comunication(conn,addr):
    try:
        data = conn.recv(1024)  # Tamanho máximo da mensagem é 1024 bytes
        if data:
            # Parse da mensagem protobuf
            message = mumes.MulticastMessage()
            message.ParseFromString(data)
            sender = message.sender
            type = message.type
            print(f"Recebido de {sender}: {type}")
            #cliente
            if(type == '0'):
                print('user')
            #sensor
            elif(type == '1'):
                print('sensor')
                sensor_handle(sender, conn, addr)

            #atuador
            elif(type == '2'):
                print('atuador')
                lamp_handle(sender, conn, addr)
            #ar-condicionado
            elif(type=='3'):
                print('ar-condicionado')
        print('chegou')
    except:
        print('close')
        conn.close()
        obj_sock.remove((conn,addr))
        
    

    

############################# tratamentos de objetos #####################################

#Sensor
def sensor_handle(sender, conn, addr):
    try:
        while True:
            data = conn.recv(1024)
            message = senmes.SensorMessage()
            message.ParseFromString(data)
            usr.senTemp.temperatura = message.valor
            if(message.valor == ''):
                obj_sock.remove(conn)
                conn.close()
                break
    
    except:        
        obj_sock.remove((conn,addr))
        conn.close()
        
    return 0

#ALampada
def lamp_handle(sender, conn, addr):
    while True:
        msg_ctrl = lames.LampadaControl()
        time.sleep(3)
        print(acao)
        if acao == '2':
            while acao == '2':  
                print('lmap')
            msg_ctrl.control = '1'

            # Codifique a mensagem em bytes
            msg_bytes = lames.SerializeToString(msg_ctrl)
            conn.sendall(msg_bytes)
            msg_ctt = lames.Lampada()
            msg_ctt.ParseFromString(conn.recv(1024))
            print(msg_ctt.status)

    return 0

#Ar-condicionado
# def ac_handle(sender):
#     server_ip = '192.168.1.245'
#     server_port = 6000
#     # Crie um socket TCP
#     sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#     # Vincular o socket ao endereço e porta do servidor
#     sock.bind((server_ip, server_port))

#     # Espere por conexões de clientes
#     sock.listen(1)

#     print(f"Servidor TCP escutando em {server_ip}:{server_port}")
#     objetos[sender] = None

#     while True:
#         conn, addr = sock.accept()
#         data = senmes.SensorMessage()
#         data.ParseFromString(conn.recv(1024))
#         objetos[sender] = data.valor
#         print(f"Conexão estabelecida com {objetos}")
        
#     return 0

def init_client():
    print('Bem vindo ao Alexo Rabbit')
    
    while(True):
        print('Lista de ações:')
        for i in range(len(acoes)):
            print(i+1, '-', acoes[i])
        
            acao = input('Digite o número da ação que deseja tomar?\n')
            if acao == '1':
                print('A tempeatura do sensor é:', senTemp.temperatura)
            elif acao == '2':
                print('O status da lampada é', lamp.status)
            elif acao == '3':
                print('')
            elif acao == '4':
                print('')
            elif acao == '5':
                print('')
            elif acao == '6':
                print('')
            elif acao == '7':
                print('')

acoes=[ 
    'Saber a temperatura do sensor',
    'Status da lampada',
    'Ligar/Desligar a lampada',
    'Temperatura do ar-condicionado',
    'Status do ar-condicionado',
    'Aumentar temperatura',
    'Baixar temperatura'
]


if __name__ == "__main__":
    # Crie uma thread para executar a função multicast_sender

    msnd.multicast_sender('0')

    objetos = {}
    obj_sock = []
    server_ip = mrcv.get_active_interface_ip('wifi0')
    print(server_ip)
    server_port = 8002
    # Crie um socket TCP
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Vincular o socket ao endereço e porta do servidor
    sock.bind((server_ip, server_port))

    # Espere por conexões de clientes
    sock.listen(5)

    client_thread = threading.Thread(target=init_client)
    client_thread.start()

    while(True):
        conn, addr = sock.accept()
        print(f"Escutando mensagens de {addr}")
        obj_sock.append((conn,addr))
        

        obj_thread = threading.Thread(target=obj_comunication, args=(conn,addr))
        obj_thread.start()
        # Inicie a thread
        print('foi')

    
