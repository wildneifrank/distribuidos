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
    # Configurações do servidor
    host = ip  # Endereço IP ou nome de host do servidor
    porta = port       # Porta do servidor

    # Mensagem que você deseja enviar
    lpctrl = lames.LampadaControl()
    lpctrl.control = op
    msg_srl = lpctrl.SerializeToString()

    # Crie um socket TCP
    cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Conecte-se ao servidor
    cliente_socket.connect((host, porta))

    # Envie a mensagem para o servidor
    cliente_socket.send(msg_srl)

    # Aguarde a resposta do servidor (opcional)
    

    data = cliente_socket.recv(1024)
    lpstatus = lames.Lampada()
    lpstatus.ParseFromString(data)
    print(f'Status da lampada: {lpstatus.status}')

    # Feche o socket do cliente
    cliente_socket.close()

def tcpComunicationArCond(ip, port, op):
    # Configurações do servidor
    host = ip  # Endereço IP ou nome de host do servidor
    porta = port       # Porta do servidor

    arctrl = armes.Controle()
    arctrl.operacao = op
    msg_srl = arctrl.SerializeToString()

    cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cliente_socket.connect((host, porta))
    cliente_socket.send(msg_srl)

    arstatus = armes.attributes()
    data = cliente_socket.recv(1024)
    arstatus.ParseFromString(data)
    print(arstatus)
    if arstatus.state:
        print(f'Status do Ar Condicionado: Ligado em {arstatus.temp}ºC')
    else:
        print('Desligado')
    
    cliente_socket.close()


def multiRcv():
    
    # Configurações do servidor
    host = mrcv.get_active_interface_ip('wifi0')  # Endereço IP do servidor (use 'localhost' para conexões locais)
    porta = PORT     # Porta em que o servidor irá ouvir

    # Crie um socket TCP
    servidor_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Vincule o socket ao endereço e porta do servidor
    servidor_socket.bind((host, porta))

    # Espere por conexões de clientes (até 5 clientes em fila)
    servidor_socket.listen(5)

    while True:
        # Aceite uma conexão de cliente
        cliente_socket, endereco_cliente = servidor_socket.accept()

        # Receba a mensagem enviada pelo cliente
        mensagem_recebida = cliente_socket.recv(1024)  # Ajuste o tamanho do buffer conforme necessário

        # Deserializar a mensagem protobuf recebida
        mensagem_pb = mumes.MulticastMessage()
        mensagem_pb.ParseFromString(mensagem_recebida)
        
        # Aqui você pode adicionar a lógica para responder à mensagem, se necessário
        disp = (mensagem_pb.ip, mensagem_pb.port, mensagem_pb.type)
        # Feche a conexão com o cliente
        cliente_socket.close()


        # Nome do arquivo CSV onde você deseja escrever os dados
        nome_arquivo = 'dados.csv'

        # Abra o arquivo CSV para escrita
        with open(nome_arquivo, 'a', newline='') as arquivo_csv:
            # Crie um objeto escritor CSV
            escritor_csv = csv.writer(arquivo_csv)

            # Escreva a tupla no arquivo CSV
            escritor_csv.writerow(disp)

def lp_handle(acao):
    caminho_arquivo = 'dados.csv'
    df = pd.read_csv(caminho_arquivo)
    
    print(df['type'].values[0])
    if 2 in df['type'].values:
        index = df.index[df['type'] == 2][0]
        line = df.iloc[index]
        tcpComunicationLamp(line['ip'], line['port'], acao)

    else:
        print(f'Não existe uma lampada conectada.')

def ac_handle(acao):
    caminho_arquivo = 'dados.csv'
    df = pd.read_csv(caminho_arquivo)
    if 3 in df['type'].values:
        index = df.index[df['type'] == 3][0]
        line = df.iloc[index]
        tcpComunicationArCond(line['ip'], line['port'], acao) # mudar pra arc

    else:
        print(f'Não existe um ar condicionado conectado.')

    
def sensor_rcv():
    # Configurações do servidor udp
    host = mrcv.get_active_interface_ip('wifi0')# Endereço IP do servidor
    porta = 5000       # Porta do servidor

    # Crie um socket UDP
    servidor_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Vincule o socket ao endereço e à porta do servidor
    servidor_socket.bind((host, porta))

    while True:
        # Receba uma mensagem do cliente e o endereço do cliente
        mensagem, endereco_cliente = servidor_socket.recvfrom(1024)
        # Dados que você deseja salvar
        sensor_msg = semes.Sensor()
        sensor_msg.ParseFromString(mensagem)
        # Nome do arquivo de texto
        nome_arquivo = "temperatura.txt"

        # Abrir o arquivo em modo de escrita
        with open(nome_arquivo, "w") as arquivo:
            arquivo.write(str(sensor_msg.temperature))

def sensor_handle(acao):
    # Nome do arquivo de texto
    nome_arquivo = "Temperatura.txt"

    # Lista para armazenar os dados lidos do arquivo
    dados_lidos = 0

    # Abrir o arquivo em modo de leitura
    with open(nome_arquivo, "r") as arquivo:
            for linha in arquivo:
            # Remova a quebra de linha (\n) no final de cada linha e adicione à lista
                dados_lidos = linha.strip()

    # Exiba os dados lidos
    print('Temperatura é: ',dados_lidos)





if __name__ == "__main__":
    #envia o multicast
    msnd.multicast_sender('0')

    #nomeia labels do arquivo csv
    nome_arquivo = 'dados.csv'
    labels = ('ip', 'port', 'type')
    with open(nome_arquivo, 'w', newline='') as arquivo_csv:
            # Crie um objeto escritor CSV
            escritor_csv = csv.writer(arquivo_csv)

            # Escreva a tupla no arquivo CSV
            escritor_csv.writerow(labels)

    # thread para receber infos dos dispositivos
    mrcv_thread = threading.Thread(target=multiRcv)
    mrcv_thread.start()

    udp_thread = threading.Thread(target=sensor_rcv)
    udp_thread.start()
    
    #receber comandos do usuario
    usr.init_client()



    