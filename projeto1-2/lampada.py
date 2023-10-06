import lampada_pb2

class Lampada:
    def __init__(self):
        self.status = False

    def ligar(self):
        self.status = True

    def desligar(self):
        self.status = False

    def get_status(self):
        return lampada_pb2.LampadaStatus(ligada=self.status)
