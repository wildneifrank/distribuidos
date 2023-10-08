import true_gateway as gtw

def init_client():
    print('Bem vindo ao Alexo Rabbit')
    
    while(True):
        print('Lista de objetos:')
        for i in range(len(obj)):
            print(i+1, '-', obj[i])
        acao = input('Digite o número do objeto que deseja manipular?\n')
        if acao == '1':
            print('Lista de ações:')
            print('1 - Saber a temperatura do sensor')
            act = input('Digite o número da ação que deseja tomar:')
            if act == '1':
                gtw.sensor_handle(act)
            else:
                print('opção inválida')
        elif acao == '2':
            print('Lista de ações:')
            for i in range(len(acoes_lp)):
                print(i+1, '-', acoes_lp[i])
            act = input('Digite o número da ação que deseja tomar:')
            if act == '1':
                gtw.lp_handle(act)
            elif act == '2':
                gtw.lp_handle(act)
            elif act == '3':
                gtw.lp_handle(act)
            else:
                print('opção inválida')
        elif acao == '3':
            print('Lista de ações:')
            for i in range(len(acoes_ac)):
                print(i+1, '-', acoes_ac[i])
            act = input('Digite o número da ação que deseja tomar:')
            if act == '1':
                gtw.ac_handle(act)
            elif act == '2':
                gtw.ac_handle(act)
            elif act == '3':
                gtw.ac_handle(act)
            elif act == '4':
                gtw.ac_handle(act)
            elif act == '5':
                gtw.ac_handle(act)
            else:
                print('opção inválida')

obj = [
    'Sensor de Temperatura',
    'Lampada',
    'Ar condicionado'
]
acoes_lp=[ 
    
    'Status da lampada',
    'Ligar',
    'Desligar a lampada'
]
acoes_ac = [
    'Ligar',
    'Desligar',
    'Status do ar-condicionado',
    'Aumentar temperatura',
    'Baixar temperatura'
]