import socket
import MulticastReceiver as mrcv
import MulticastSender as msnd
import threading
import csv
import User as usr
import pandas as pd
from protoBuff import lampada_pb2 as lames
from protoBuff import ArCondicionado_pb2 as armes


def tcpComunicationLamp(ip, port, op):
    # Configurações do servidor
    host = ip  # Endereço IP ou nome de host do servidor
    porta = port       # Porta do servidor

    # Mensagem que você deseja enviar
    lpctrl = lames.LampadaControl()
    lpctrl.control = op
    msg_srl = lpctrl.SerializeToString

    # Crie um socket TCP
    cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Conecte-se ao servidor
    cliente_socket.connect((host, porta))

    # Envie a mensagem para o servidor
    cliente_socket.send(msg_srl)

    # Aguarde a resposta do servidor (opcional)
    lpstatus = lames.Lampada()

    data = cliente_socket.recv(1024)
    lpstatus.ParseFromString(data)
    print(f'Status da lampada: {lpstatus.status}')

    # Feche o socket do cliente
    cliente_socket.close()

def tcpComunicationArCond(ip, port, op):
    # Configurações do servidor
    host = ip  # Endereço IP ou nome de host do servidor
    porta = port       # Porta do servidor

    arctrl = armes.ArCondicionado()
    arctrl.op = op
    msg_srl = arctrl.SerializeToString

    cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cliente_socket.connect((host, porta))
    cliente_socket.send(msg_srl)

    arstatus = armes.ArCondicionado()
    data = cliente_socket.recv(1024)
    arstatus.ParseFromString(data)
    if arstatus.state:
        print(f'Status do Ar Condicionado: Ligado em {arstatus.temp}ºC')
    else:
        print('Desligado')
    
    cliente_socket.close()


def multiRcv():
    while True:
        disp = mrcv.multicast_receiver()

        # Nome do arquivo CSV onde você deseja escrever os dados
        nome_arquivo = 'dados.csv'

        # Abra o arquivo CSV para escrita
        with open(nome_arquivo, 'a', newline='') as arquivo_csv:
            # Crie um objeto escritor CSV
            escritor_csv = csv.writer(arquivo_csv)

            # Escreva a tupla no arquivo CSV
            escritor_csv.writerow(disp)

        print(f"A tupla {disp} foi escrita no arquivo CSV '{nome_arquivo}'.")

def lp_handle(acao):
    caminho_arquivo = 'dados.csv'
    df = pd.read_csv(caminho_arquivo)
    if '1' in df['type'].values:
        index = df.index[df['type'] == '2']
        line = df.iloc[index]
        tcpComunicationLamp(line[0],line[1], acao)

    else:
        print(f'Não existe uma lampada conectada.')

def ac_handle(acao):
    caminho_arquivo = 'dados.csv'
    df = pd.read_csv(caminho_arquivo)
    if '3' in df['type'].values:
        index = df.index[df['type'] == '3']
        line = df.iloc[index]
        tcpComunicationLamp(line[0],line[1], acao) # mudar pra arc

    else:
        print(f'Não existe um ar condicionado conectado.')

    




if __name__ == "__main__":
    #envia o multicast
    msnd.multicast_sender()

    #nomeia labels do arquivo csv
    nome_arquivo = 'dados.csv'
    labels = ('ip', 'port', 'type')
    with open(nome_arquivo, 'a', newline='') as arquivo_csv:
            # Crie um objeto escritor CSV
            escritor_csv = csv.writer(arquivo_csv)

            # Escreva a tupla no arquivo CSV
            escritor_csv.writerow(labels)

    # thread para receber infos dos dispositivos
    mrcv_thread = threading.Thread(target=multiRcv)
    mrcv_thread.start()
    
    #receber comandos do usuario
    usr.init_client()



    