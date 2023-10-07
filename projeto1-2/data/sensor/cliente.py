import socket
import sensor_pb2

# Endereço e porta do servidor UDP
UDP_SERVER_ADDRESS = ("127.0.0.1", 8080)

def solicitar_status():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        control_msg = lampada_pb2.LampadaControl()
        control_msg.control = "1"
        msg = control_msg.SerializeToString()
        s.sendto(msg, UDP_SERVER_ADDRESS)
        resposta, _ = s.recvfrom(1024)
        print(f"Status da lâmpada: {resposta.decode('utf-8')}")

def ligar_lampada():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.sendto(b"Ligar", UDP_SERVER_ADDRESS)
        print("Ligando a lâmpada...")

def desligar_lampada():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.sendto(b"Desligar", UDP_SERVER_ADDRESS)
        print("Desligando a lâmpada...")

if __name__ == "__main__":
    while True:
        print("Opções:")
        print("1. Solicitar status da lâmpada")
        print("2. Ligar a lâmpada")
        print("3. Desligar a lâmpada")
        print("4. Sair")

        escolha = input("Escolha uma opção (1/2/3/4): ")

        if escolha == "1":
            solicitar_status()
        elif escolha == "2":
            ligar_lampada()
        elif escolha == "3":
            desligar_lampada()
        elif escolha == "4":
            break
        else:
            print("Opção inválida. Por favor, escolha uma opção válida.")
