import socket
import MulticastReceiver as mrcv
import MulticastSender as msnd
import threading
import csv
import User as usr
import pandas as pd
from protoBuff import lampada_pb2 as lames
from protoBuff import ArCondicionado_pb2 as armes
from protoBuff import  MulticastMessage_pb2 as mumes
from protoBuff import sensor_pb2 as semes
PORT = 8002


def tcpComunicationLamp(ip, port, op):
    host = ip  
    porta = port      

    lpctrl = lames.LampadaControl()
    lpctrl.control = op
    msg_srl = lpctrl.SerializeToString()

    cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    cliente_socket.connect((host, porta))

    cliente_socket.send(msg_srl)
    print('enviou')

    data = cliente_socket.recv(1024)
    lpstatus = lames.Lampada()
    print('recebeu')
    lpstatus.ParseFromString(data)
    print(f'Status da lampada: {lpstatus.status}')

    cliente_socket.close()

def tcpComunicationArCond(ip, port, op):
    host = ip  
    porta = port     

    arctrl = armes.Controle()
    arctrl.operacao = op
    msg_srl = arctrl.SerializeToString()

    cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cliente_socket.connect((host, porta))
    cliente_socket.send(msg_srl)

    arstatus = armes.attributes()
    data = cliente_socket.recv(1024)
    print('recebido')
    arstatus.ParseFromString(data)
    print(arstatus)
    if arstatus.state:
        print(f'Status do Ar Condicionado: Ligado em {arstatus.temp}ºC')
    else:
        print('Desligado')
    
    cliente_socket.close()


def multiRcv():
    #Configurações do servidor
    host = mrcv.get_active_interface_ip('wifi0') 
    porta = PORT   

    #Criar um socket TCP
    servidor_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor_socket.bind((host, porta))

    # Até 5 clientes em fila
    servidor_socket.listen(5)

    print(f"Servidor TCP está ouvindo em {host}:{porta}")

    while True:
        cliente_socket, endereco_cliente = servidor_socket.accept()
        print(f"Conexão estabelecida com {endereco_cliente}")

        mensagem_recebida = cliente_socket.recv(1024) 

        #Deserializa a mensagem protobuf recebida
        mensagem_pb = mumes.MulticastMessage()
        mensagem_pb.ParseFromString(mensagem_recebida)

        print(f'Mensagem recebida de {mensagem_pb.ip}:{mensagem_pb.port}')
        print(f'Tipo de mensagem: {mensagem_pb.type}')
        
        disp = (mensagem_pb.ip, mensagem_pb.port, mensagem_pb.type)
        cliente_socket.close()

        #Escrever os dados em um arquivo .csv
        nome_arquivo = 'dados.csv'

        with open(nome_arquivo, 'a', newline='') as arquivo_csv:
            escritor_csv = csv.writer(arquivo_csv)

            escritor_csv.writerow(disp)

        print(f"A tupla {disp} foi escrita no arquivo CSV '{nome_arquivo}'.")

def lp_handle(acao):
    caminho_arquivo = 'dados.csv'
    df = pd.read_csv(caminho_arquivo)
    print(df)
    
    print(df['type'].values[0])
    if 2 in df['type'].values:
        index = df.index[df['type'] == '2']
        print(index,'oi index')
        line = df.iloc[index]
        tcpComunicationArCond(line[0],line[1], acao)

    else:
        print(f'Não existe uma lampada conectada.')

def ac_handle(acao):
    caminho_arquivo = 'dados.csv'
    df = pd.read_csv(caminho_arquivo)
    if 3 in df['type'].values:
        index = df.index[df['type'] == '3']
        line = ['localhost', 8003]
        tcpComunicationArCond(line[0],line[1], acao) 

    else:
        print(f'Não existe um ar condicionado conectado.')

    
def sensor_rcv():
    host = mrcv.get_active_interface_ip('wifi0')
    porta = 5000       

    # Crie um socket UDP
    servidor_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    servidor_socket.bind((host, porta))

    print(f"Servidor UDP está ouvindo em {host}:{porta}")

    while True:
        mensagem, endereco_cliente = servidor_socket.recvfrom(1024)

        sensor_msg = semes.Sensor()
        sensor_msg.ParseFromString(mensagem)
        print(sensor_msg.temperature)

        # Arquivo de texto para armazenar temperaturas
        nome_arquivo = "temperatura.txt"
        with open(nome_arquivo, "w") as arquivo:
            arquivo.write(str(sensor_msg.temperature))

def sensor_handle(acao):
    nome_arquivo = "Temperatura.txt"
    dados_lidos = 0

    with open(nome_arquivo, "r") as arquivo:
            for linha in arquivo:
                dados_lidos = linha.strip()

    print('Temperatura é: ',dados_lidos)


if __name__ == "__main__":
    #Envia o multicast
    msnd.multicast_sender('0')

    #Nomeia labels do arquivo csv
    nome_arquivo = 'dados.csv'
    labels = ('ip', 'port', 'type')
    with open(nome_arquivo, 'w', newline='') as arquivo_csv:
            escritor_csv = csv.writer(arquivo_csv)

            escritor_csv.writerow(labels)

    mrcv_thread = threading.Thread(target=multiRcv)

    udp_thread = threading.Thread(target=sensor_rcv)
    udp_thread.start()
    
    usr.init_client()



    