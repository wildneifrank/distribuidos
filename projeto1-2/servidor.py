import grpc
from concurrent import futures
from lampada import Lampada
import lampada_pb2
import lampada_pb2_grpc

class LampadaService(lampada_pb2_grpc.LampadaServiceServicer):
    def __init__(self):
        self.lampada = Lampada()

    def GetStatus(self, request, context):
        return self.lampada.get_status()

    def Control(self, request, context):
        if request.ligar:
            self.lampada.ligar()
        elif request.desligar:
            self.lampada.desligar()
        return self.lampada.get_status()

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    lampada_pb2_grpc.add_LampadaServiceServicer_to_server(LampadaService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
