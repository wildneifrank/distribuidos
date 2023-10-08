class SensorTemp:
    def __init__(self):
        self.temperatura = None
class ArCon:
    def __init__(self):
        self.temperatura = None
        self.status = 'Desligado'
class Lampada:
    def __init__(self):
        self.status = 'Desligado'
import gateway as gtw


senTemp = SensorTemp()
arcon = ArCon()
lamp = Lampada()


def init_client(acao):
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