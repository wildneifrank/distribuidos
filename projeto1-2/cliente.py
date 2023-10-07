import socket
import lampada_pb2

def solicitar_status():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(("127.0.0.1", 8080))
        control_msg = lampada_pb2.LampadaControl()
        control_msg.control = "1"
        msg = control_msg.SerializeToString()
        s.sendall(msg)
        resposta = s.recv(1024)
        print(f"Status da lâmpada: {resposta.decode('utf-8')}")

def ligar_lampada():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(("127.0.0.1", 8080))
        s.sendall(b"Ligar")
        print("Ligando a lâmpada...")

def desligar_lampada():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(("127.0.0.1", 8080))
        s.sendall(b"Desligar")
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
