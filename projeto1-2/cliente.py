import grpc
import lampada_pb2
import lampada_pb2_grpc

def main():
    # Conecte-se ao servidor gRPC
    channel = grpc.insecure_channel('localhost:50051')
    stub = lampada_pb2_grpc.LampadaServiceStub(channel)

    # Obtenha o status inicial da lâmpada
    status = stub.GetStatus(lampada_pb2.LampadaStatus())
    print(f'Status inicial da lâmpada: {"Ligada" if status.ligada else "Desligada"}')

    # Ligue a lâmpada
    print(f'Cliente apertou em Ligar')
    stub.Control(lampada_pb2.LampadaControl(ligar=True))
    status = stub.GetStatus(lampada_pb2.LampadaStatus())
    print(f'Estado da Lâmpada: {"Ligada" if status.ligada else "Desligada"}')

    # Desligue a lâmpada
    print(f'Cliente apertou em Desligar')
    stub.Control(lampada_pb2.LampadaControl(desligar=True))
    status = stub.GetStatus(lampada_pb2.LampadaStatus())
    print(f'Estado da Lâmpada: {"Ligada" if status.ligada else "Desligada"}')

if __name__ == '__main__':
    main()
