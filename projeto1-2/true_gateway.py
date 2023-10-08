import socket
import MulticastReceiver as mrcv
import MulticastSender as msnd
import threading
import csv



def multiRcv():
    while True:
        disp = mrcv.multicast_receiver()

        # Nome do arquivo CSV onde você deseja escrever os dados
        nome_arquivo = 'dados.csv'

        # Abra o arquivo CSV para escrita
        with open(nome_arquivo, 'w', newline='') as arquivo_csv:
            # Crie um objeto escritor CSV
            escritor_csv = csv.writer(arquivo_csv)

            # Escreva a tupla no arquivo CSV
            escritor_csv.writerow(disp)

        print(f"A tupla {disp} foi escrita no arquivo CSV '{nome_arquivo}'.")





if __name__ == "__main__":
    msnd.multicast_sender()

    mrcv_thread = threading.Thread(target=multiRcv)
    mrcv_thread.start()



    